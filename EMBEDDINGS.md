# 🔢 Búsqueda Semántica con Embeddings

## ✅ Actualización Implementada

El sistema ahora usa **embeddings de Cohere** para búsqueda semántica en lugar de búsqueda simple. Esto mejora DRÁSTICAMENTE la calidad de los candidatos antes del Rerank.

## 🎯 ¿Qué son los Embeddings?

Los embeddings son representaciones numéricas (vectores) de texto que capturan su **significado semántico**.

### Ejemplo:
```
"¿Cuál es el plazo para apelar?" 
→ [0.234, -0.891, 0.456, ..., 0.123]  (1024 dimensiones)

"El plazo de apelación es de 10 días"
→ [0.221, -0.875, 0.443, ..., 0.119]  (1024 dimensiones)

"Receta de pizza napolitana"
→ [-0.567, 0.234, -0.891, ..., -0.445]  (1024 dimensiones)
```

Los primeros dos vectores son **muy similares** (tema legal, apelaciones).
El tercero es **muy diferente** (tema cocina).

## 🔄 Flujo Actualizado

### ANTES (Búsqueda Simple):
```
Usuario: "¿Cuál es el plazo para apelar?"
    ↓
[Paso 1] Retorna TODOS los documentos (sin filtro real)
    ↓
[Paso 2] Rerank ordena documentos
    ↓
[Paso 3] Genera respuesta
```

### AHORA (Búsqueda Semántica):
```
Usuario: "¿Cuál es el plazo para apelar?"
    ↓
[Paso 1a] Genera embedding de la query
[Paso 1b] Calcula similaridad con todos los documentos
[Paso 1c] Retorna TOP 20 más similares semánticamente
    ↓
[Paso 2] Rerank afina el orden de esos 20
    ↓
[Paso 3] Genera respuesta con TOP 5 finales
```

## 🧮 Similaridad Coseno

La similaridad entre dos vectores se calcula con el **cosine similarity**:

```python
similarity = cos(θ) = (A · B) / (||A|| × ||B||)
```

- **1.0**: Vectores idénticos (máxima similaridad)
- **0.0**: Vectores perpendiculares (sin relación)
- **-1.0**: Vectores opuestos

### Ejemplo Real:
```python
query_embedding = [0.5, 0.8, 0.2]
doc1_embedding  = [0.6, 0.7, 0.3]  # Similaridad: 0.95 ✅ MUY SIMILAR
doc2_embedding  = [0.1, 0.2, 0.9]  # Similaridad: 0.42 ⚠️ POCO SIMILAR
```

## 🔧 Implementación Técnica

### 1. Al cargar documentos:
```python
# Se generan embeddings de TODOS los documentos
response = client.embed(
    texts=[doc1.content, doc2.content, ...],
    model="embed-multilingual-v3.0",
    input_type="search_document"  # ← Importante: tipo documento
)

# Se almacenan como matriz NumPy
document_embeddings = np.array(response.embeddings.float)
# Shape: (num_documentos, 1024)
```

### 2. Al hacer una query:
```python
# Generar embedding de la query
query_response = client.embed(
    texts=[query],
    model="embed-multilingual-v3.0",
    input_type="search_query"  # ← Importante: tipo query
)
query_embedding = np.array(query_response.embeddings.float[0])
# Shape: (1024,)

# Calcular similaridades
similarities = cosine_similarity(query_embedding, document_embeddings)
# Shape: (num_documentos,)

# Obtener top N
top_indices = np.argsort(similarities)[::-1][:20]
candidates = [documents[i] for i in top_indices]
```

## 🎓 Modelo de Embeddings

**`embed-multilingual-v3.0`** (usado en el proyecto):
- ✅ **1024 dimensiones**
- ✅ **100+ idiomas** (excelente para español)
- ✅ Optimizado para búsqueda semántica
- ✅ Alta calidad en contenido jurídico

Alternativas:
- `embed-english-v3.0`: Solo inglés (más rápido)
- `embed-multilingual-light-v3.0`: Más rápido, menos preciso

## 📊 Ventajas de Embeddings sobre Búsqueda Simple

| Aspecto | Búsqueda Simple | Embeddings |
|---------|----------------|------------|
| **Sinónimos** | ❌ No detecta | ✅ "plazo" = "término" |
| **Contexto** | ❌ Ignora | ✅ Entiende tema |
| **Multilingüe** | ❌ Limitado | ✅ Excelente |
| **Typos** | ❌ Falla | ✅ Tolera errores |
| **Semántica** | ❌ No | ✅ Captura significado |

### Ejemplo Práctico:

**Query**: "¿Cuánto tiempo tengo para impugnar una resolución?"

**Búsqueda Simple**: 
- Buscaría palabras: "tiempo", "impugnar", "resolución"
- Podría NO encontrar documentos que usen "plazo", "apelar", "sentencia"

**Embeddings**:
- Entiende que "impugnar" ≈ "apelar"
- Entiende que "tiempo" ≈ "plazo"
- Entiende que "resolución" ≈ "sentencia"
- ✅ Encuentra documentos relevantes aunque usen palabras diferentes

## 💰 Impacto en Costos

### Costos Adicionales:
- **Generar embeddings al cargar**: ~$0.0001 por documento
- **Embedding de query**: ~$0.0001 por consulta

Para 100 documentos:
- Carga inicial: ~$0.01 (una sola vez)
- Por consulta: ~$0.0001 (insignificante)

**Total por consulta completa**:
- Embeddings: $0.0001
- Rerank: $0.002
- Generation: $0.02
- **Total**: ~$0.022 (prácticamente igual que antes)

## 🧪 Cómo Probar la Mejora

### Test Comparativo:

```python
# Ejecutar con embeddings (actual)
python main.py

# Observar los scores de similaridad en Paso 1:
#   → #1 - Score: 0.8523 - plazos_legales.md  ✅ Alta relevancia
#   → #2 - Score: 0.7234 - recursos_judiciales.md
```

Notarás que:
1. **Los candidatos son más relevantes** desde el Paso 1
2. **Rerank tiene mejor material** para ordenar
3. **La respuesta final es más precisa**

## 🔍 Ver los Embeddings en Acción

Agrega este código en `ejemplos_avanzados.py`:

```python
def ejemplo_visualizar_embeddings():
    """Ver cómo funcionan los embeddings"""
    from rag_system import LegalRAGSystem
    import numpy as np
    
    rag = LegalRAGSystem(api_key=os.getenv("COHERE_API_KEY"))
    rag.load_documents_from_folder("data/legal_docs")
    
    # Consultas de prueba
    queries = [
        "¿Cuál es el plazo para apelar?",
        "¿Qué es un recurso de casación?",
        "Receta de pizza napolitana"  # ← NO relevante
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        
        # Generar embedding de query
        query_emb = rag.client.embed(
            texts=[query],
            model="embed-multilingual-v3.0",
            input_type="search_query"
        ).embeddings.float[0]
        
        # Calcular similaridades
        sims = rag._cosine_similarity(
            np.array(query_emb), 
            rag.document_embeddings
        )
        
        # Mostrar resultados
        for i, doc in enumerate(rag.documents):
            print(f"  {doc.metadata['source']}: {sims[i]:.4f}")
```

## 📚 Próximos Pasos

Para optimizar aún más:

1. **Cachear embeddings**:
   ```python
   # Guardar embeddings en disco
   np.save('doc_embeddings.npy', document_embeddings)
   
   # Cargar en vez de regenerar
   document_embeddings = np.load('doc_embeddings.npy')
   ```

2. **Usar base de datos vectorial** (ChromaDB, Pinecone):
   - Almacenamiento persistente
   - Búsqueda optimizada
   - Escalable a millones de documentos

3. **Chunking + Embeddings**:
   - Dividir documentos largos en chunks
   - Cada chunk tiene su embedding
   - Mayor precisión en la búsqueda

## 🎯 Resumen

✅ **Implementado**: Búsqueda semántica con `embed-multilingual-v3.0`
✅ **Ventaja**: Encuentra documentos relevantes por significado, no solo por palabras
✅ **Costo**: Prácticamente igual (~$0.0001 adicional)
✅ **Calidad**: MUCHO mejor que búsqueda simple
✅ **Listo**: Ya funciona en el sistema, solo ejecuta `python main.py`

¡Ahora tienes un sistema RAG de producción con búsqueda semántica! 🚀
