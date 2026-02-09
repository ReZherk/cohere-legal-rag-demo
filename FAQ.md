# FAQ y Troubleshooting 🔧

## Preguntas Frecuentes

### ¿Cuánto cuesta usar Cohere?

Cohere ofrece un plan gratuito con créditos limitados:
- **Trial**: $5 en créditos gratis
- **Rerank**: ~$0.002 por 1000 documentos
- **Command R+**: ~$3 por 1M tokens de entrada, ~$15 por 1M tokens de salida

**Estimación para este demo**: ~$0.01-0.05 por consulta completa

### ¿Qué modelo usar: Command R o Command R+?

| Característica | Command R | Command R+ |
|---------------|-----------|------------|
| **Velocidad** | Más rápido | Más lento |
| **Calidad** | Buena | Excelente |
| **Costo** | Más barato | Más caro |
| **Uso recomendado** | Desarrollo/testing | Producción |

### ¿Cuántos documentos pasar a Rerank?

**Recomendaciones**:
- Candidatos iniciales: 10-50 documentos
- Top K después de Rerank: 3-5 documentos
- Más documentos = mayor costo y latencia

### ¿Cómo mejorar la calidad de las respuestas?

1. **Mejora tus documentos**:
   - Contenido claro y estructurado
   - Sin redundancia
   - Chunks de tamaño adecuado (300-600 palabras)

2. **Ajusta parámetros**:
   - Aumenta `top_k` si las respuestas son vagas
   - Reduce `temperature` para respuestas más precisas
   - Mejora el prompt del sistema

3. **Usa búsqueda semántica**:
   - Reemplaza búsqueda simple con embeddings
   - Usa ChromaDB o similar

### ¿Puedo usar otros idiomas?

Sí, Cohere soporta:
- **Rerank v3.5**: 100+ idiomas incluido español
- **Command R+**: Multilingüe (español, inglés, francés, etc.)
- **Embed v3**: Embeddings multilingües

### ¿Cómo evito alucinaciones?

1. Usa temperatura baja (0.1-0.3)
2. Instrucciones claras: "Responde SOLO con info del contexto"
3. Implementa validación de respuestas
4. Usa Citation mode en producción:

```python
response = client.chat(
    model="command-r-plus",
    message=prompt,
    temperature=0.2,
    documents=[{"text": doc} for doc in context_docs],
    citation_quality="accurate"  # Fuerza citas
)
```

## Troubleshooting

### Error: "Invalid API Key"

**Solución**:
```bash
# Verifica que .env existe
ls -la .env

# Verifica el contenido (sin espacios extra)
cat .env

# Formato correcto:
COHERE_API_KEY=tu-key-sin-comillas-ni-espacios

# Re-cargar
source .env  # Linux/Mac
```

### Error: "Rate limit exceeded"

**Causa**: Excediste el límite de requests gratuito

**Solución**:
1. Espera 1 hora (límite por hora)
2. Agrega delay entre requests:
```python
import time
time.sleep(1)  # Espera 1 segundo entre consultas
```
3. Implementa caché para evitar requests duplicados

### Error: "Document too long"

**Causa**: El contexto excede el límite del modelo

**Solución**:
```python
# Limitar tamaño de documentos
MAX_CONTEXT_LENGTH = 4000  # caracteres

context = "\n\n".join([
    doc['content'][:1000]  # Truncar cada doc
    for doc in context_docs
])[:MAX_CONTEXT_LENGTH]
```

### Las respuestas son irrelevantes

**Diagnóstico**:
```python
# Imprime scores de Rerank
for doc in reranked_docs:
    print(f"Score: {doc['score']}")

# Si todos los scores son < 0.3, el problema es la búsqueda inicial
```

**Soluciones**:
1. Agrega más documentos relevantes
2. Mejora la búsqueda inicial (usa embeddings)
3. Verifica que tus documentos contienen la info necesaria

### Python 3.12 no encuentra el módulo

**Error**:
```
ModuleNotFoundError: No module named 'cohere'
```

**Solución**:
```bash
# Verifica que estás en el venv
which python  # Debe mostrar ruta al venv

# Reinstala
pip install -r requirements.txt

# Verifica instalación
pip list | grep cohere
```

### El programa se cuelga

**Causas comunes**:
1. Red lenta/timeout
2. Documentos muy grandes
3. Muchos documentos a procesar

**Solución**:
```python
# Agregar timeouts
import cohere

client = cohere.Client(
    api_key=api_key,
    timeout=30  # 30 segundos
)

# O usar async
import asyncio

async def query_async(query):
    # Implementación async
    pass
```

### ImportError con utils

**Error**:
```
ImportError: cannot import name 'DocumentLoader'
```

**Solución**:
```bash
# Asegúrate de que __init__.py existe
ls utils/__init__.py

# Ejecuta desde la raíz del proyecto
cd cohere-legal-rag-demo
python main.py

# No desde subdirectorios
```

### Respuestas en inglés cuando quiero español

**Solución**:
```python
prompt = f"""Eres un asistente legal experto. Responde EN ESPAÑOL a la consulta.

IMPORTANTE: Tu respuesta DEBE ser en español.

CONTEXTO:
{context}

CONSULTA:
{query}

RESPUESTA (EN ESPAÑOL):"""
```

## Depuración Avanzada

### Ver requests completos
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Ahora verás todos los requests HTTP
```

### Medir tiempos
```python
import time

start = time.time()
resultado = rag.query(query)
print(f"Tiempo total: {time.time() - start:.2f}s")
```

### Guardar logs de debugging
```python
import json
from datetime import datetime

def log_query(query, resultado):
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'query': query,
        'answer': resultado['answer'],
        'num_docs': len(resultado['context_docs']),
        'top_scores': [d['score'] for d in resultado['context_docs'][:3]]
    }
    
    with open('query_log.json', 'a') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
```

## Optimización de Costos

### Estrategias

1. **Caché agresivo**:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def query_cached(query_hash, top_k):
    return rag.query(query_hash, top_k)
```

2. **Reduce top_k**:
```python
# Más barato
resultado = rag.query(query, top_k=3)  # vs top_k=10
```

3. **Usa Command R en desarrollo**:
```python
# Desarrollo
rag_dev = LegalRAGSystem(api_key, model="command-r")

# Producción
rag_prod = LegalRAGSystem(api_key, model="command-r-plus")
```

4. **Batch queries**:
```python
# Procesa múltiples consultas en una sesión
# para amortizar overhead
```

## Contacto y Recursos

- **Cohere Discord**: https://discord.gg/cohere
- **Documentación**: https://docs.cohere.com
- **Status Page**: https://status.cohere.com
- **GitHub Issues**: Tu repositorio
