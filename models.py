"""
Modelos Pydantic para respuestas estructuradas del sistema RAG Legal
"""
from typing import Literal
from pydantic import BaseModel, Field


class DocumentSource(BaseModel):
    """Representa una fuente documental citada en la respuesta"""
    nombre: str = Field(description="Nombre del documento fuente")
    relevancia: float = Field(description="Puntuación de relevancia del documento (0-1)", ge=0, le=1)


class LegalAnswerSimple(BaseModel):
    """Respuesta estructurada del asistente legal (sin referencias anidadas para compatibilidad con Cohere)"""
    respuesta: str = Field(description="Respuesta completa a la consulta legal del usuario")
    fuentes_nombres: list[str] = Field(
        description="Lista de nombres de documentos citados como fuente",
        default_factory=list
    )
    fuentes_relevancias: list[float] = Field(
        description="Lista de puntuaciones de relevancia correspondientes a cada fuente (0-1)",
        default_factory=list
    )
    confianza: Literal["alta", "media", "baja"] = Field(
        description="Nivel de confianza en la respuesta basado en la calidad del contexto disponible"
    )


# Alias para compatibilidad
LegalAnswer = LegalAnswerSimple

