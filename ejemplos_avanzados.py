"""
Ejemplo avanzado: Uso programático del sistema RAG

Este script muestra cómo integrar el sistema RAG en tus propios proyectos
"""
import os
from dotenv import load_dotenv
from rag_system import LegalRAGSystem
import json


def ejemplo_basico():
    """Ejemplo más simple de uso"""
    print("\n" + "="*60)
    print("EJEMPLO 1: Uso básico")
    print("="*60)
    
    load_dotenv()
    
    # Inicializar
    rag = LegalRAGSystem(api_key=os.getenv("COHERE_API_KEY"))
    
    # Cargar documentos
    rag.load_documents_from_folder("data/legal_docs")
    
    # Consultar
    resultado = rag.query("¿Cuál es el plazo para apelar?")
    
    print(resultado['answer'])


def ejemplo_con_analisis():
    """Ejemplo con análisis de documentos recuperados"""
    print("\n" + "="*60)
    print("EJEMPLO 2: Análisis de documentos recuperados")
    print("="*60)
    
    load_dotenv()
    
    rag = LegalRAGSystem(api_key=os.getenv("COHERE_API_KEY"))
    rag.load_documents_from_folder("data/legal_docs")
    
    resultado = rag.query(
        query="¿Qué tipos de recursos judiciales existen?",
        top_k=3,
        initial_candidates=10
    )
    
    # Analizar contexto usado
    print("\n📊 ANÁLISIS DE DOCUMENTOS RECUPERADOS:")
    print("-" * 60)
    for doc in resultado['context_docs']:
        print(f"Rank #{doc['rank']}")
        print(f"Relevancia: {doc['score']:.4f}")
        print(f"Preview: {doc['content'][:150]}...")
        print("-" * 60)
    
    print("\n💡 RESPUESTA GENERADA:")
    print(resultado['answer'])


def ejemplo_multiples_consultas():
    """Ejemplo procesando múltiples consultas"""
    print("\n" + "="*60)
    print("EJEMPLO 3: Procesamiento batch de consultas")
    print("="*60)
    
    load_dotenv()
    
    rag = LegalRAGSystem(api_key=os.getenv("COHERE_API_KEY"))
    rag.load_documents_from_folder("data/legal_docs")
    
    consultas = [
        "¿Qué es la cosa juzgada?",
        "¿Cuándo procede el recurso de queja?",
        "¿Qué es el efecto devolutivo de la apelación?"
    ]
    
    resultados = []
    for consulta in consultas:
        print(f"\n🔍 Procesando: {consulta}")
        resultado = rag.query(consulta, top_k=2)
        resultados.append({
            'consulta': consulta,
            'respuesta': resultado['answer'],
            'num_docs': len(resultado['context_docs'])
        })
        print("✅ Completado")
    
    # Guardar resultados
    with open('resultados_batch.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    print("\n💾 Resultados guardados en: resultados_batch.json")


def ejemplo_comparacion_modelos():
    """Ejemplo comparando command-r vs command-r-plus"""
    print("\n" + "="*60)
    print("EJEMPLO 4: Comparación de modelos")
    print("="*60)
    
    load_dotenv()
    api_key = os.getenv("COHERE_API_KEY")
    
    consulta = "Explica brevemente qué es un recurso de casación"
    
    # Command R
    print("\n🤖 Usando Command R:")
    rag_r = LegalRAGSystem(api_key=api_key, model="command-r")
    rag_r.load_documents_from_folder("data/legal_docs")
    resultado_r = rag_r.query(consulta, top_k=2)
    print(resultado_r['answer'])
    
    # Command R+
    print("\n🤖 Usando Command R+:")
    rag_plus = LegalRAGSystem(api_key=api_key, model="command-r-plus")
    rag_plus.load_documents_from_folder("data/legal_docs")
    resultado_plus = rag_plus.query(consulta, top_k=2)
    print(resultado_plus['answer'])


if __name__ == "__main__":
    print("🎓 EJEMPLOS AVANZADOS DEL SISTEMA RAG")
    print("Nota: Estos ejemplos consumen API credits. Usa con moderación.")
    
    print("\n¿Qué ejemplo deseas ejecutar?")
    print("1. Uso básico")
    print("2. Análisis de documentos recuperados")
    print("3. Procesamiento batch")
    print("4. Comparación de modelos")
    print("5. Ejecutar todos")
    
    opcion = input("\nSelecciona (1-5): ").strip()
    
    ejemplos = {
        '1': ejemplo_basico,
        '2': ejemplo_con_analisis,
        '3': ejemplo_multiples_consultas,
        '4': ejemplo_comparacion_modelos,
    }
    
    if opcion == '5':
        for func in ejemplos.values():
            func()
    elif opcion in ejemplos:
        ejemplos[opcion]()
    else:
        print("❌ Opción no válida")
