# Cohere Legal RAG Demo

🎯 **Proyecto de aprendizaje**: Sistema RAG (Retrieval-Augmented Generation) con Cohere Rerank para consultas sobre contenido jurídico.

## 📋 ¿Qué hace este proyecto?

Este proyecto demuestra cómo usar **Cohere** para construir un sistema RAG que:

1. **Carga** documentos jurídicos en formato Markdown
2. **Recupera** documentos potencialmente relevantes basados en la consulta del usuario
3. **Reordena** (Rerank) los documentos usando la API de Cohere para identificar los más relevantes
4. **Genera** una respuesta contextualizada usando el modelo Command R+ de Cohere

## 🏗️ Arquitectura

```
Usuario: "¿Cuál es el plazo para apelar?"
    ↓
[Paso 1] Búsqueda Semántica con Embeddings → Recupera 20 documentos más similares
    ↓
[Paso 2] Cohere Rerank → Ordena y selecciona TOP 5 más relevantes
    ↓
[Paso 3] Cohere Command R+ → Genera respuesta con contexto enriquecido
    ↓
Respuesta final al usuario
```

### 🔢 Tecnologías Clave:
- **Embeddings**: `embed-multilingual-v3.0` para búsqueda semántica
- **Rerank**: `rerank-v3.5` para refinamiento de resultados
- **Generación**: `command-r-plus` para respuestas contextualizadas

## 🚀 Instalación

### Requisitos
- Python 3.12+
- API Key de Cohere (obtén una gratis en [cohere.com](https://cohere.com))
- NumPy (para cálculos de similaridad)

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/cohere-legal-rag-demo.git
cd cohere-legal-rag-demo
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar API Key**
```bash
cp .env.example .env
# Edita .env y agrega tu COHERE_API_KEY
```

## 📖 Uso

### Ejecutar el demo básico

```bash
python main.py
```

### Hacer consultas personalizadas

```python
from rag_system import LegalRAGSystem

# Inicializar sistema
rag = LegalRAGSystem(api_key="tu-api-key")

# Cargar documentos
rag.load_documents_from_folder("data/legal_docs")

# Hacer consulta
respuesta = rag.query(
    query="¿Cuál es el plazo para apelar una sentencia?",
    top_k=5
)

print(respuesta)
```

## 📁 Estructura del Proyecto

```
cohere-legal-rag-demo/
├── README.md
├── requirements.txt
├── .env.example
├── main.py                 # Script principal de demostración
├── rag_system.py           # Clase principal del sistema RAG
├── data/
│   └── legal_docs/         # Documentos jurídicos de ejemplo (Markdown)
│       ├── codigo_procesal.md
│       ├── plazos_legales.md
│       └── recursos_judiciales.md
└── utils/
    └── document_loader.py  # Utilidades para cargar documentos
```

## 🎓 Conceptos Clave

### ¿Qué son los Embeddings?
Los embeddings son representaciones vectoriales (numéricas) de texto que capturan su significado semántico. El sistema usa `embed-multilingual-v3.0` de Cohere para convertir documentos y consultas en vectores de 1024 dimensiones, permitiendo búsqueda por significado en lugar de solo por palabras clave.

**Ventaja**: Encuentra "plazo para apelar" incluso si el documento dice "término de apelación".

### ¿Qué es Rerank?
Cohere Rerank es un modelo especializado que toma una consulta y una lista de documentos, y los **reordena** según su relevancia semántica. Es mucho más preciso que búsquedas por palabras clave y complementa perfectamente la búsqueda inicial por embeddings.

### ¿Por qué usar RAG?
- **Contexto actualizado**: El LLM usa información específica de tus documentos
- **Menos alucinaciones**: Respuestas basadas en datos reales
- **Dominio específico**: Ideal para contenido jurídico, médico, técnico, etc.
- **Búsqueda semántica**: Entiende el significado, no solo palabras exactas

## 🔧 Configuración Avanzada

Puedes ajustar parámetros en `rag_system.py`:

```python
# Número de documentos a recuperar inicialmente
initial_candidates = 20

# Top K documentos después de Rerank
top_k = 5

# Modelo de generación
model = "command-r-plus"  # o "command-r"
```

## 🧪 Próximos Pasos

Este es un proyecto de **aprendizaje**. Para tu proyecto final más grande:

- [ ] Integrar base de datos vectorial (ChromaDB, Pinecot, Weaviate)
- [ ] Agregar embeddings para búsqueda semántica inicial
- [ ] Implementar chunking inteligente de documentos largos
- [ ] Añadir caché de respuestas
- [ ] Crear API REST con FastAPI
- [ ] Interfaz web con Streamlit

## 📚 Recursos

- [Cohere Documentation](https://docs.cohere.com)
- [Cohere Rerank Guide](https://docs.cohere.com/docs/reranking)
- [Cohere Embeddings Guide](https://docs.cohere.com/docs/embeddings)
- [RAG Best Practices](https://docs.cohere.com/docs/retrieval-augmented-generation-rag)
- [EMBEDDINGS.md](./EMBEDDINGS.md) - Guía detallada sobre búsqueda semántica en este proyecto

## 📄 Licencia

MIT License - Proyecto educativo
