"""
Sistema RAG con Cohere Rerank para consultas legales

Este módulo implementa el flujo completo:
1. Búsqueda semántica con embeddings de Cohere
2. Rerank con Cohere para ordenar por relevancia
3. Generación de respuesta con Command R+ usando contexto
"""
import cohere
import numpy as np
from typing import List, Dict, Optional
from utils.document_loader import Document, DocumentLoader


class LegalRAGSystem:
    """
    Sistema completo de RAG para consultas legales con búsqueda semántica
    """
    
    def __init__(self, api_key: str, model: str = "command-r-plus", embed_model: str = "embed-multilingual-v3.0"):
        """
        Inicializa el sistema RAG
        
        Args:
            api_key: API key de Cohere
            model: Modelo a usar para generación (command-r-plus o command-r)
            embed_model: Modelo de embeddings (embed-multilingual-v3.0 recomendado para español)
        """
        self.client = cohere.Client(api_key)
        self.model = model
        self.embed_model = embed_model
        self.documents: List[Document] = []
        self.document_embeddings: Optional[np.ndarray] = None
        
    def load_documents_from_folder(self, folder_path: str):
        """
        Carga documentos desde una carpeta y genera sus embeddings
        
        Args:
            folder_path: Ruta a la carpeta con archivos .md
        """
        print(f"\n📂 Cargando documentos desde: {folder_path}")
        self.documents = DocumentLoader.load_from_folder(folder_path)
        print(f"✅ Total de documentos cargados: {len(self.documents)}")
        
        if self.documents:
            self._generate_embeddings()
    
    def _generate_embeddings(self):
        """
        Genera embeddings para todos los documentos cargados
        """
        print(f"\n🔢 Generando embeddings con {self.embed_model}...")
        
        # Extraer textos de los documentos
        texts = [doc.content for doc in self.documents]
        
        # Generar embeddings con Cohere
        response = self.client.embed(
            texts=texts,
            model=self.embed_model,
            input_type="search_document",  # Tipo para documentos (no queries)
            embedding_types=["float"]
        )
        
        # Convertir a numpy array para cálculos eficientes
        self.document_embeddings = np.array(response.embeddings.float)
        
        print(f"✅ Embeddings generados: {self.document_embeddings.shape}")
        print(f"   → {len(self.documents)} documentos × {self.document_embeddings.shape[1]} dimensiones\n")
        
    def _semantic_search(self, query: str, top_n: int = 20) -> List[Document]:
        """
        PASO 1: Búsqueda semántica usando embeddings de Cohere
        
        Args:
            query: Consulta del usuario
            top_n: Número de documentos a retornar
            
        Returns:
            Lista de documentos candidatos ordenados por similaridad
        """
        print(f"🔍 [Paso 1] Búsqueda semántica con embeddings...")
        
        if self.document_embeddings is None:
            print("   ⚠️  No hay embeddings generados. Usa load_documents_from_folder() primero.")
            return []
        
        # Generar embedding de la query
        query_response = self.client.embed(
            texts=[query],
            model=self.embed_model,
            input_type="search_query",  # Tipo para queries (no documentos)
            embedding_types=["float"]
        )
        query_embedding = np.array(query_response.embeddings.float[0])
        
        # Calcular similaridad coseno con todos los documentos
        similarities = self._cosine_similarity(query_embedding, self.document_embeddings)
        
        # Obtener índices de los top N documentos más similares
        top_indices = np.argsort(similarities)[::-1][:top_n]
        
        # Crear lista de candidatos con sus scores
        candidates = []
        for idx in top_indices:
            doc = self.documents[idx]
            score = similarities[idx]
            # Agregar score como metadata temporal
            doc.similarity_score = score
            candidates.append(doc)
            
        print(f"   → Top {len(candidates)} candidatos por similaridad:")
        for i, doc in enumerate(candidates[:5], 1):  # Mostrar top 5
            print(f"      #{i} - Score: {doc.similarity_score:.4f} - {doc.metadata['source']}")
        
        return candidates
    
    @staticmethod
    def _cosine_similarity(query_embedding: np.ndarray, doc_embeddings: np.ndarray) -> np.ndarray:
        """
        Calcula similaridad coseno entre query y documentos
        
        Args:
            query_embedding: Embedding de la query (1D array)
            doc_embeddings: Embeddings de documentos (2D array)
            
        Returns:
            Array de similaridades
        """
        # Normalizar vectores
        query_norm = query_embedding / np.linalg.norm(query_embedding)
        doc_norms = doc_embeddings / np.linalg.norm(doc_embeddings, axis=1, keepdims=True)
        
        # Calcular producto punto (cosine similarity)
        similarities = np.dot(doc_norms, query_norm)
        
        return similarities
    
    def _rerank_documents(self, query: str, documents: List[Document], top_k: int = 5) -> List[Dict]:
        """
        PASO 2: Reordena documentos usando Cohere Rerank
        
        Args:
            query: Consulta del usuario
            documents: Lista de documentos a reordenar
            top_k: Número de documentos top a retornar
            
        Returns:
            Lista de documentos reordenados con scores
        """
        print(f"\n🎯 [Paso 2] Reranking con Cohere...")
        
        # Preparar documentos para Rerank
        docs_text = [doc.content for doc in documents]
        
        # Llamar a Cohere Rerank
        rerank_response = self.client.rerank(
            model="rerank-v3.5",  # Modelo de rerank de Cohere
            query=query,
            documents=docs_text,
            top_n=top_k,
            return_documents=True
        )
        
        # Procesar resultados
        reranked_docs = []
        for idx, result in enumerate(rerank_response.results):
            reranked_docs.append({
                'content': result.document.text,
                'score': result.relevance_score,
                'original_index': result.index,
                'rank': idx + 1
            })
            print(f"   #{idx+1} - Score: {result.relevance_score:.4f} - Fuente: {documents[result.index].metadata['source']}")
        
        return reranked_docs
    
    def _generate_response(self, query: str, context_docs: List[Dict]) -> str:
        """
        PASO 3: Genera respuesta usando Command R+ con contexto
        
        Args:
            query: Consulta del usuario
            context_docs: Documentos con contexto relevante
            
        Returns:
            Respuesta generada
        """
        print(f"\n🤖 [Paso 3] Generando respuesta con {self.model}...")
        
        # Construir contexto desde los documentos
        context = "\n\n---\n\n".join([
            f"DOCUMENTO {doc['rank']} (Relevancia: {doc['score']:.2f}):\n{doc['content']}"
            for doc in context_docs
        ])
        
        # Prompt para el modelo
        prompt = f"""Eres un asistente legal experto. Responde a la consulta del usuario basándote ÚNICAMENTE en el contexto proporcionado.

CONTEXTO:
{context}

CONSULTA DEL USUARIO:
{query}

INSTRUCCIONES:
- Responde de forma clara y precisa
- Cita los documentos relevantes cuando sea apropiado
- Si el contexto no contiene información suficiente, indícalo
- Usa un lenguaje profesional pero accesible

RESPUESTA:"""
        
        # Generar respuesta
        response = self.client.chat(
            model=self.model,
            message=prompt,
            temperature=0.3,  # Baja temperatura para respuestas más precisas
        )
        
        return response.text
    
    def query(self, query: str, top_k: int = 5, initial_candidates: int = 20) -> Dict:
        """
        Método principal: procesa una consulta completa
        
        Args:
            query: Pregunta del usuario
            top_k: Número de documentos top después de rerank
            initial_candidates: Número de candidatos iniciales (búsqueda semántica)
            
        Returns:
            Diccionario con respuesta y metadatos
        """
        print(f"\n{'='*60}")
        print(f"CONSULTA: {query}")
        print(f"{'='*60}")
        
        # Validar que hay documentos cargados
        if not self.documents:
            return {
                'answer': "❌ No hay documentos cargados. Usa load_documents_from_folder() primero.",
                'context_docs': [],
                'query': query
            }
        
        # Validar que hay embeddings generados
        if self.document_embeddings is None:
            return {
                'answer': "❌ No hay embeddings generados. Los documentos deben cargarse con load_documents_from_folder().",
                'context_docs': [],
                'query': query
            }
        
        # PASO 1: Búsqueda semántica con embeddings
        candidates = self._semantic_search(query, top_n=initial_candidates)
        
        # PASO 2: Rerank
        reranked_docs = self._rerank_documents(query, candidates, top_k=top_k)
        
        # PASO 3: Generar respuesta
        answer = self._generate_response(query, reranked_docs)
        
        print(f"\n{'='*60}")
        print("RESPUESTA FINAL:")
        print(f"{'='*60}\n")
        
        return {
            'answer': answer,
            'context_docs': reranked_docs,
            'query': query
        }
