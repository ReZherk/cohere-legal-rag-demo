# 🎉 Proyecto Creado: cohere-legal-rag-demo

## ✅ Lo que se ha generado

He creado un **proyecto completo y funcional** de RAG (Retrieval-Augmented Generation) con Cohere que implementa exactamente el flujo que solicitaste:

```
Usuario: "¿Cuál es el plazo para apelar?"
    ↓
[Paso 1] Búsqueda Semántica con Embeddings → Recupera 20 documentos más similares
    ↓
[Paso 2] RERANK con Cohere → Ordena y obtiene TOP 5 más relevantes
    ↓
[Paso 3] Pasa esos TOP 5 al LLM de Cohere (Command R+)
    ↓
LLM genera respuesta con mejor contexto
```

### 🔢 Tecnología de Búsqueda:
**✅ AHORA USA EMBEDDINGS** - No es búsqueda simple, sino búsqueda semántica con:
- **Modelo**: `embed-multilingual-v3.0` de Cohere
- **Dimensiones**: 1024 valores numéricos por documento
- **Ventaja**: Encuentra documentos por **significado**, no solo por palabras
- **Ejemplo**: Encuentra "plazo para apelar" aunque diga "término de apelación"

## 📁 Estructura del Proyecto

```
cohere-legal-rag-demo/
├── README.md                      # Documentación principal
├── EMBEDDINGS.md                  # 🔥 Guía sobre búsqueda semántica
├── FAQ.md                         # Preguntas frecuentes y troubleshooting
├── PROXIMOS_PASOS.md              # Guía para escalar a producción
├── requirements.txt               # Dependencias Python
├── .env.example                   # Plantilla de configuración
├── .gitignore                     # Archivos a ignorar en Git
│
├── main.py                        # 🚀 Script principal - EMPIEZA AQUÍ
├── rag_system.py                  # Sistema RAG completo
├── ejemplos_avanzados.py          # Ejemplos de uso avanzado
├── visualizar_embeddings.py       # 🔢 Visualización de embeddings
├── test_rag.py                    # Tests del sistema
│
├── utils/
│   ├── __init__.py
│   └── document_loader.py         # Carga documentos Markdown
│
└── data/
    └── legal_docs/                # 📚 Documentos jurídicos de ejemplo
        ├── plazos_legales.md
        ├── recursos_judiciales.md
        └── codigo_procesal.md
```

## 🎯 Archivos Clave

### 1. **rag_system.py** - El Corazón del Sistema
Contiene la clase `LegalRAGSystem` con los 3 pasos:
- `_semantic_search()`: Búsqueda semántica con embeddings
- `_rerank_documents()`: Rerank con Cohere (API rerank-v3.5)
- `_generate_response()`: Generación con Command R+

### 2. **main.py** - Demo Interactivo
Script listo para ejecutar con:
- Demo automática (2 consultas predefinidas)
- Modo interactivo (haz tus propias consultas)

### 3. **ejemplos_avanzados.py** - Uso Programático
4 ejemplos diferentes de cómo usar el sistema en código:
- Uso básico
- Análisis de documentos recuperados
- Procesamiento batch
- Comparación de modelos

### 4. **data/legal_docs/** - Contenido Jurídico
3 documentos Markdown de ejemplo sobre:
- Plazos legales (apelaciones, contestaciones, etc.)
- Recursos judiciales (casación, reposición, queja)
- Código procesal (extractos relevantes)

## 🚀 Cómo Empezar

### Paso 1: Configurar el entorno
```bash
cd cohere-legal-rag-demo

# Crear entorno virtual
python3.12 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 2: Configurar API Key
```bash
# Copiar plantilla
cp .env.example .env

# Editar .env y agregar tu API key de Cohere
# COHERE_API_KEY=tu-key-real-aqui
```

Obtén tu API key gratis en: https://dashboard.cohere.com/api-keys

### Paso 3: Ejecutar el demo
```bash
python main.py
```

## 💡 Ejemplos de Uso

### Uso Básico
```python
from rag_system import LegalRAGSystem

# Inicializar
rag = LegalRAGSystem(api_key="tu-api-key")

# Cargar documentos
rag.load_documents_from_folder("data/legal_docs")

# Consultar
resultado = rag.query("¿Cuál es el plazo para apelar?")
print(resultado['answer'])
```

### Acceder a Documentos Usados
```python
resultado = rag.query("¿Qué es un recurso de casación?")

# Ver documentos que se usaron
for doc in resultado['context_docs']:
    print(f"Relevancia: {doc['score']:.4f}")
    print(f"Contenido: {doc['content'][:200]}...")
```

## 📚 Documentación Adicional

1. **README.md**: Guía completa del proyecto
2. **EMBEDDINGS.md**: 🔥 **NUEVO** - Guía detallada sobre búsqueda semántica con embeddings
3. **FAQ.md**: Solución a problemas comunes
4. **PROXIMOS_PASOS.md**: Cómo escalar a producción (embeddings, caché, API, etc.)

## 🎓 Conceptos Implementados

### ✅ Búsqueda Semántica con Embeddings
- Usa el modelo `embed-multilingual-v3.0`
- Convierte documentos y queries en vectores de 1024 dimensiones
- Búsqueda por similaridad coseno
- **Mucho más preciso** que búsqueda por palabras clave

### ✅ Rerank de Cohere
- Usa el modelo `rerank-v3.5`
- Reordena documentos por relevancia semántica
- Complementa perfectamente la búsqueda por embeddings
- Refinamiento final de los candidatos

### ✅ Generación con Command R+
- Modelo `command-r-plus` optimizado para RAG
- Soporte multilingüe (español excelente)
- Generación basada en contexto provisto

### ✅ Carga de Documentos Markdown
- Utilidad para cargar archivos .md
- Generación automática de embeddings al cargar
- Metadatos (fuente, ruta, tipo)
- Preparado para chunking de documentos largos

## 🧪 Testing

Ejecuta los tests para verificar que todo funciona:

```bash
python test_rag.py
```

Tests incluidos:
- ✅ Estructura del proyecto
- ✅ Carga de documentos
- ✅ Configuración de API key
- ✅ Inicialización del sistema
- ✅ Query de prueba (opcional, consume créditos)

## 🚀 Próximos Pasos para Producción

Para tu proyecto grande con contenido jurídico real:

1. **✅ Embeddings** (YA IMPLEMENTADO)
   - ✅ Ya usa `embed-multilingual-v3.0` de Cohere
   - ⏭️ Opcional: Cachear embeddings en disco
   - ⏭️ Opcional: Usar base de datos vectorial (ChromaDB, Pinecone, Weaviate)

2. **Chunking Inteligente**
   - Dividir documentos largos en chunks
   - LangChain RecursiveCharacterTextSplitter

3. **API REST**
   - Exponer como servicio con FastAPI
   - Documentación automática con Swagger

4. **Interfaz Web**
   - Streamlit para prototipo rápido
   - React + API para producción

5. **Optimización de Costos**
   - Implementar caché de respuestas
   - Usar Command R en desarrollo
   - Monitorear uso de tokens
   - React + API para producción

5. **Optimización de Costos**
   - Implementar caché de respuestas
   - Usar Command R en desarrollo
   - Monitorear uso de tokens

Todo esto está explicado en detalle en **PROXIMOS_PASOS.md**

## 📊 Estimación de Costos

Para este proyecto de aprendizaje:
- **Rerank**: ~$0.001 por consulta (20 documentos)
- **Command R+**: ~$0.02 por consulta
- **Total**: ~$0.02-0.03 por consulta completa

El plan gratuito de Cohere te da $5 en créditos = ~200 consultas

## ⚠️ Notas Importantes

1. **No subir .env a Git**: Ya está en .gitignore
2. **Python 3.12**: El código usa type hints modernos
3. **Búsqueda Simple**: Por ahora es básica, en producción usa embeddings
4. **Documentos de Ejemplo**: Reemplázalos con tus documentos jurídicos reales

## 🎯 Nombre del Repositorio

Sugerencias:
- `cohere-legal-rag-demo` ✅ (usado en este proyecto)
- `legal-ai-assistant`
- `cohere-rerank-starter`
- `juridical-rag-system`

## 📞 Soporte

- **Cohere Docs**: https://docs.cohere.com
- **Cohere Discord**: https://discord.gg/cohere
- **Este README**: Lee la documentación incluida

## 🎉 ¡Ya Está Listo!

El proyecto está completamente funcional. Solo necesitas:
1. Instalar dependencias
2. Agregar tu API key
3. Ejecutar `python main.py`

**¡Disfruta aprendiendo sobre RAG con Cohere!** 🚀
