"""
Visualización de Embeddings y Similaridad

Este script muestra cómo funcionan los embeddings y la similaridad semántica
"""
import os
from dotenv import load_dotenv
from rag_system import LegalRAGSystem
import numpy as np


def visualizar_similaridades():
    """
    Muestra la similaridad entre diferentes queries y documentos
    """
    print("=" * 70)
    print("🔍 VISUALIZACIÓN DE EMBEDDINGS Y SIMILARIDAD SEMÁNTICA")
    print("=" * 70)
    
    load_dotenv()
    api_key = os.getenv("COHERE_API_KEY")
    
    if not api_key or api_key == "tu-api-key-aqui":
        print("\n❌ ERROR: Configura tu COHERE_API_KEY en el archivo .env")
        return
    
    # Inicializar sistema
    print("\n📦 Inicializando sistema y generando embeddings...")
    rag = LegalRAGSystem(api_key=api_key)
    rag.load_documents_from_folder("data/legal_docs")
    
    # Queries de prueba
    queries = [
        "¿Cuál es el plazo para apelar una sentencia?",
        "¿Qué es un recurso de casación?",
        "Explícame cómo se cuentan los plazos procesales",
        "¿Cómo hacer una pizza napolitana?",  # ← NO relevante (control)
    ]
    
    print("\n" + "=" * 70)
    print("📊 ANÁLISIS DE SIMILARIDAD PARA DIFERENTES CONSULTAS")
    print("=" * 70)
    
    for query_idx, query in enumerate(queries, 1):
        print(f"\n{'─' * 70}")
        print(f"QUERY #{query_idx}: {query}")
        print(f"{'─' * 70}")
        
        # Generar embedding de la query
        query_response = rag.client.embed(
            texts=[query],
            model=rag.embed_model,
            input_type="search_query",
            embedding_types=["float"]
        )
        query_embedding = np.array(query_response.embeddings.float[0])
        
        # Calcular similaridades con todos los documentos
        similarities = rag._cosine_similarity(query_embedding, rag.document_embeddings)
        
        # Ordenar por similaridad
        sorted_indices = np.argsort(similarities)[::-1]
        
        # Mostrar resultados
        print("\n📈 Similaridad con cada documento:")
        for rank, idx in enumerate(sorted_indices, 1):
            doc = rag.documents[idx]
            score = similarities[idx]
            
            # Visualización con barras
            bar_length = int(score * 50)  # Barra de hasta 50 caracteres
            bar = "█" * bar_length + "░" * (50 - bar_length)
            
            # Emoji según relevancia
            if score > 0.7:
                emoji = "🟢"
                label = "ALTA"
            elif score > 0.4:
                emoji = "🟡"
                label = "MEDIA"
            else:
                emoji = "🔴"
                label = "BAJA"
            
            print(f"  {emoji} #{rank} - {doc.metadata['source']:25s} | {bar} | {score:.4f} ({label})")
        
        # Determinar relevancia general
        max_sim = np.max(similarities)
        if max_sim > 0.7:
            conclusion = "✅ Hay documentos MUY relevantes para esta consulta"
        elif max_sim > 0.4:
            conclusion = "⚠️  Hay documentos relacionados, pero no altamente relevantes"
        else:
            conclusion = "❌ NO hay documentos relevantes (como era de esperar)"
        
        print(f"\n  💡 {conclusion}")


def comparar_queries_similares():
    """
    Compara queries que son semánticamente similares pero con palabras diferentes
    """
    print("\n\n" + "=" * 70)
    print("🔬 COMPARACIÓN DE QUERIES SEMÁNTICAMENTE SIMILARES")
    print("=" * 70)
    
    load_dotenv()
    api_key = os.getenv("COHERE_API_KEY")
    
    rag = LegalRAGSystem(api_key=api_key)
    
    # Pares de queries semánticamente similares
    query_pairs = [
        (
            "¿Cuál es el plazo para apelar?",
            "¿Cuánto tiempo tengo para impugnar una sentencia?"
        ),
        (
            "¿Qué es un recurso de casación?",
            "Explícame qué significa recurso de casación"
        ),
    ]
    
    print("\nGenerando embeddings de queries...\n")
    
    for idx, (query1, query2) in enumerate(query_pairs, 1):
        print(f"{'─' * 70}")
        print(f"PAR #{idx}:")
        print(f"  Query A: {query1}")
        print(f"  Query B: {query2}")
        
        # Generar embeddings
        response = rag.client.embed(
            texts=[query1, query2],
            model=rag.embed_model,
            input_type="search_query",
            embedding_types=["float"]
        )
        
        emb1 = np.array(response.embeddings.float[0])
        emb2 = np.array(response.embeddings.float[1])
        
        # Calcular similaridad entre las queries
        # Normalizar
        emb1_norm = emb1 / np.linalg.norm(emb1)
        emb2_norm = emb2 / np.linalg.norm(emb2)
        
        # Similaridad
        similarity = np.dot(emb1_norm, emb2_norm)
        
        # Visualizar
        bar_length = int(similarity * 50)
        bar = "█" * bar_length + "░" * (50 - bar_length)
        
        print(f"\n  Similaridad: {bar} {similarity:.4f}")
        
        if similarity > 0.9:
            print(f"  💚 Prácticamente idénticas semánticamente")
        elif similarity > 0.7:
            print(f"  💛 Muy similares (mismo tema)")
        else:
            print(f"  🧡 Relacionadas pero diferentes enfoques")
        
        print()


def mostrar_dimensiones_embedding():
    """
    Muestra información sobre las dimensiones de los embeddings
    """
    print("\n\n" + "=" * 70)
    print("📐 INFORMACIÓN SOBRE DIMENSIONES DE EMBEDDINGS")
    print("=" * 70)
    
    load_dotenv()
    api_key = os.getenv("COHERE_API_KEY")
    
    rag = LegalRAGSystem(api_key=api_key)
    
    # Generar embedding de ejemplo
    response = rag.client.embed(
        texts=["Ejemplo de texto"],
        model=rag.embed_model,
        input_type="search_query",
        embedding_types=["float"]
    )
    
    embedding = np.array(response.embeddings.float[0])
    
    print(f"\n📊 Modelo: {rag.embed_model}")
    print(f"📏 Dimensiones: {len(embedding)}")
    print(f"📈 Rango de valores: [{embedding.min():.4f}, {embedding.max():.4f}]")
    print(f"📉 Valor promedio: {embedding.mean():.4f}")
    print(f"📐 Norma (magnitud): {np.linalg.norm(embedding):.4f}")
    
    print("\n💡 Primeros 10 valores del embedding:")
    print(f"   {embedding[:10]}")
    
    print("\n📚 Explicación:")
    print("  - Cada documento y query se convierte en un vector de 1024 números")
    print("  - Estos números capturan el 'significado' del texto")
    print("  - Textos similares tendrán vectores similares")
    print("  - La similaridad se mide con cosine similarity")


def main():
    """
    Función principal
    """
    print("\n🎓 HERRAMIENTA DE VISUALIZACIÓN DE EMBEDDINGS")
    print("\nElige una opción:")
    print("1. Visualizar similaridades de diferentes queries")
    print("2. Comparar queries semánticamente similares")
    print("3. Mostrar información sobre dimensiones")
    print("4. Ejecutar todo")
    
    opcion = input("\nSelecciona (1-4): ").strip()
    
    if opcion == "1":
        visualizar_similaridades()
    elif opcion == "2":
        comparar_queries_similares()
    elif opcion == "3":
        mostrar_dimensiones_embedding()
    elif opcion == "4":
        visualizar_similaridades()
        comparar_queries_similares()
        mostrar_dimensiones_embedding()
    else:
        print("❌ Opción no válida")
    
    print("\n\n" + "=" * 70)
    print("✅ VISUALIZACIÓN COMPLETADA")
    print("=" * 70)
    print("\n💡 Para entender más sobre embeddings, lee EMBEDDINGS.md")


if __name__ == "__main__":
    main()
