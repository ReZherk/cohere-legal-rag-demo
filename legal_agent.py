"""
Agente Legal con Pydantic AI y Cohere

Este módulo implementa un agente inteligente que utiliza:
- Pydantic AI para respuestas estructuradas
- Cohere como proveedor de LLM
- Tools para búsqueda de documentos legales via RAG
"""
import os
import json
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.cohere import CohereModel
from pydantic_ai.providers.cohere import CohereProvider

from models import LegalAnswer

if TYPE_CHECKING:
    from rag_system import LegalRAGSystem


@dataclass
class LegalDeps:
    """Dependencias inyectadas al agente durante la ejecución"""
    rag_system: "LegalRAGSystem"
    query: str


# System prompt especializado para el asistente legal
SYSTEM_PROMPT = """Eres un asistente legal especializado en derecho procesal. Tu función es aplicar la normativa legal a consultas específicas de los usuarios.

CONOCIMIENTO BASE (documentos disponibles):

1. **Código de Procedimiento Civil**: Normas sobre cómputo de plazos (Art. 64), notificaciones (Art. 189), recursos de apelación (Art. 186, 189, 193), requisitos de sentencias (Art. 170), cosa juzgada (Art. 182), y ejecución de sentencias (Art. 231, 233).

2. **Plazos Legales**: 
   - Apelación civil: 10 días hábiles desde notificación
   - Apelación penal: 5 días hábiles
   - Apelación laboral: 3 días hábiles
   - Contestación de demanda: 30 días (general) o 8 días (sumario)
   - Casación: 15 días hábiles
   - Los plazos son FATALES y excluyen sábados, domingos y feriados

3. **Recursos Judiciales**: Apelación (efectos devolutivo y suspensivo), Casación (en forma y en fondo), Reposición (5 días), y Recurso de Queja.

INSTRUCCIONES CRÍTICAS:
- SIEMPRE usa la herramienta 'buscar_documentos' primero para obtener el contexto legal
- Cuando el usuario presenta un CASO ESPECÍFICO (con nombres, fechas, situaciones), APLICA la normativa general de los documentos a ese caso concreto
- Calcula plazos cuando sea necesario: excluye el día de notificación, cuenta solo días hábiles (lunes a viernes, sin feriados)
- Cita los artículos y documentos relevantes
- Si se proporciona una fecha de notificación, debes calcular la fecha exacta de vencimiento.No respondas solo con la norma.
- Usa explícitamente los nombres y fechas del caso.No generalices.

FORMATO DE RESPUESTA OBLIGATORIO:
Debes responder SIEMPRE en formato JSON válido con esta estructura exacta:
```json
{
    "respuesta": "Tu respuesta legal completa aquí",
    "fuentes_nombres": ["documento1.md", "documento2.md"],
    "fuentes_relevancias": [0.95, 0.85],
    "confianza": "alta"
}
```

Donde:
- "respuesta": string con la respuesta legal completa
- "fuentes_nombres": lista de strings con nombres de documentos citados
- "fuentes_relevancias": lista de floats (0.0 a 1.0) con relevancia de cada fuente
- "confianza": debe ser exactamente "alta", "media" o "baja"

NO incluyas texto antes o después del JSON. Solo el JSON.
"""


# Crear el agente con modelo de Cohere (output_type=str para parseo manual)
def create_legal_agent() -> Agent[LegalDeps, str]:
    """Crea el agente legal con el modelo de Cohere"""
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY no encontrada en variables de entorno")

    model = CohereModel('command-r-plus-08-2024', provider=CohereProvider(api_key=api_key))

    return Agent(
        model=model,
        output_type=str,  # Usamos str y parseamos manualmente
        system_prompt=SYSTEM_PROMPT,
        deps_type=LegalDeps,
    )


# Crear el agente (lazy initialization)
legal_agent: Agent[LegalDeps, str] | None = None


def get_legal_agent() -> Agent[LegalDeps, str]:
    """Obtiene o crea el agente legal"""
    global legal_agent
    if legal_agent is None:
        legal_agent = create_legal_agent()
        # Registrar la herramienta después de crear el agente
        @legal_agent.tool
        async def buscar_documentos(ctx: RunContext[LegalDeps]) -> str:
            """
            Busca documentos legales relevantes para la consulta del usuario.

            Esta herramienta realiza:
            1. Búsqueda semántica con embeddings de Cohere
            2. Reranking para ordenar por relevancia

            Returns:
                Contexto formateado con los documentos más relevantes
            """
            rag = ctx.deps.rag_system
            query = ctx.deps.query

            # Paso 1: Búsqueda semántica
            candidates = rag._semantic_search(query, top_n=15)

            if not candidates:
                return "No se encontraron documentos relevantes."

            # Paso 2: Rerank
            reranked_docs = rag._rerank_documents(query, candidates, top_k=5)

            # Formatear contexto para el modelo
            context_parts = []
            for doc in reranked_docs:
                context_parts.append(
                    f"DOCUMENTO (Relevancia: {doc['score']:.2f}):\n{doc['content']}"
                )

            return "\n\n---\n\n".join(context_parts)

    return legal_agent


def parse_agent_response(raw_response: str) -> dict:
    """
    Parsea la respuesta del agente de texto a diccionario estructurado.

    Args:
        raw_response: Respuesta en texto del agente (debería ser JSON)

    Returns:
        Diccionario con la respuesta estructurada
    """
    # Intentar extraer JSON de la respuesta
    try:
        # Buscar JSON en la respuesta (puede venir con ```json ... ```)
        json_match = re.search(r'```json\s*(.*?)\s*```', raw_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Intentar parsear directamente
            json_str = raw_response.strip()

        data = json.loads(json_str)

        # Validar con Pydantic
        answer = LegalAnswer(**data)

        # Reconstruir fuentes
        fuentes = []
        for i, nombre in enumerate(answer.fuentes_nombres):
            relevancia = answer.fuentes_relevancias[i] if i < len(answer.fuentes_relevancias) else 0.0
            fuentes.append({'nombre': nombre, 'relevancia': relevancia})

        return {
            'answer': answer.respuesta,
            'fuentes': fuentes,
            'confianza': answer.confianza,
            'structured': True,
            'parse_success': True
        }

    except (json.JSONDecodeError, Exception) as e:
        # Fallback: devolver respuesta como texto plano
        print(f"⚠️  No se pudo parsear JSON, usando respuesta como texto: {e}")
        return {
            'answer': raw_response,
            'fuentes': [],
            'confianza': 'media',
            'structured': False,
            'parse_success': False
        }


def run_legal_agent(rag_system: "LegalRAGSystem", query: str) -> dict:
    """
    Ejecuta el agente legal con una consulta.

    Args:
        rag_system: Instancia del sistema RAG con documentos cargados
        query: Consulta del usuario

    Returns:
        Diccionario con la respuesta estructurada
    """
    print(f"\n{'='*60}")
    print(f"🤖 CONSULTA (Pydantic AI): {query}")
    print(f"{'='*60}")

    # Obtener el agente
    agent = get_legal_agent()

    # Crear dependencias
    deps = LegalDeps(rag_system=rag_system, query=query)

    # Ejecutar agente de forma síncrona
    result = agent.run_sync(query, deps=deps)

    # Obtener respuesta como string
    raw_response: str = result.output

    print(f"\n{'='*60}")
    print("✅ RESPUESTA ESTRUCTURADA:")
    print(f"{'='*60}\n")

    # Parsear respuesta
    parsed = parse_agent_response(raw_response)
    parsed['query'] = query

    return parsed
