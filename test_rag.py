"""
Tests básicos para el sistema RAG

Ejecuta: python test_rag.py
"""
import os
from dotenv import load_dotenv
from rag_system import LegalRAGSystem
from utils.document_loader import DocumentLoader


def test_cargar_documentos():
    """Test: Verificar que los documentos se cargan correctamente"""
    print("\n🧪 Test 1: Carga de documentos")
    
    try:
        docs = DocumentLoader.load_from_folder("data/legal_docs")
        assert len(docs) > 0, "No se cargaron documentos"
        print(f"   ✅ Cargados {len(docs)} documentos")
        
        # Verificar que tienen contenido
        for doc in docs:
            assert len(doc.content) > 0, f"Documento vacío: {doc.metadata['source']}"
        print(f"   ✅ Todos los documentos tienen contenido")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_api_key():
    """Test: Verificar que la API key está configurada"""
    print("\n🧪 Test 2: Configuración de API key")
    
    load_dotenv()
    api_key = os.getenv("COHERE_API_KEY")
    
    if not api_key:
        print("   ❌ COHERE_API_KEY no encontrada")
        print("   💡 Copia .env.example a .env y agrega tu API key")
        return False
    
    if api_key == "tu-api-key-aqui":
        print("   ❌ API key no configurada (todavía es el placeholder)")
        return False
    
    if len(api_key) < 20:
        print("   ⚠️  API key parece inválida (muy corta)")
        return False
    
    print("   ✅ API key configurada")
    return True


def test_inicializacion_rag():
    """Test: Verificar que el sistema RAG se inicializa correctamente"""
    print("\n🧪 Test 3: Inicialización del sistema")
    
    load_dotenv()
    api_key = os.getenv("COHERE_API_KEY")
    
    if not api_key or api_key == "tu-api-key-aqui":
        print("   ⏭️  Saltando (API key no configurada)")
        return None
    
    try:
        rag = LegalRAGSystem(api_key=api_key)
        print("   ✅ Sistema RAG inicializado")
        
        rag.load_documents_from_folder("data/legal_docs")
        assert len(rag.documents) > 0, "No se cargaron documentos"
        print(f"   ✅ Documentos cargados: {len(rag.documents)}")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_query_simple():
    """Test: Verificar que una query simple funciona"""
    print("\n🧪 Test 4: Query de prueba (consume API credits)")
    
    load_dotenv()
    api_key = os.getenv("COHERE_API_KEY")
    
    if not api_key or api_key == "tu-api-key-aqui":
        print("   ⏭️  Saltando (API key no configurada)")
        return None
    
    respuesta = input("   ⚠️  Este test consume créditos de API. ¿Continuar? (s/n): ")
    if respuesta.lower() != 's':
        print("   ⏭️  Test saltado por el usuario")
        return None
    
    try:
        rag = LegalRAGSystem(api_key=api_key, model="command-r")  # Más barato
        rag.load_documents_from_folder("data/legal_docs")
        
        print("   🔄 Ejecutando query...")
        resultado = rag.query(
            "¿Cuál es el plazo para apelar?",
            top_k=2,
            initial_candidates=5
        )
        
        assert 'answer' in resultado, "Respuesta sin campo 'answer'"
        assert len(resultado['answer']) > 0, "Respuesta vacía"
        assert len(resultado['context_docs']) > 0, "Sin documentos de contexto"
        
        print("   ✅ Query ejecutada exitosamente")
        print(f"   📊 Documentos usados: {len(resultado['context_docs'])}")
        print(f"   📝 Respuesta: {resultado['answer'][:100]}...")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_estructura_proyecto():
    """Test: Verificar que todos los archivos necesarios existen"""
    print("\n🧪 Test 5: Estructura del proyecto")
    
    archivos_necesarios = [
        "README.md",
        "requirements.txt",
        ".env.example",
        "main.py",
        "rag_system.py",
        "utils/document_loader.py",
        "utils/__init__.py",
        "data/legal_docs"
    ]
    
    todos_ok = True
    for archivo in archivos_necesarios:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} no encontrado")
            todos_ok = False
    
    return todos_ok


def main():
    """Ejecuta todos los tests"""
    print("=" * 60)
    print("🧪 SUITE DE TESTS - Sistema RAG Legal")
    print("=" * 60)
    
    resultados = {
        "Estructura del proyecto": test_estructura_proyecto(),
        "Carga de documentos": test_cargar_documentos(),
        "API Key": test_api_key(),
        "Inicialización RAG": test_inicializacion_rag(),
        "Query simple": test_query_simple(),
    }
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
    
    for nombre, resultado in resultados.items():
        if resultado is True:
            status = "✅ PASS"
        elif resultado is False:
            status = "❌ FAIL"
        else:
            status = "⏭️  SKIP"
        
        print(f"{status} - {nombre}")
    
    # Calcular stats
    passed = sum(1 for r in resultados.values() if r is True)
    failed = sum(1 for r in resultados.values() if r is False)
    skipped = sum(1 for r in resultados.values() if r is None)
    
    print(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed == 0:
        print("\n🎉 ¡Todos los tests pasaron!")
    else:
        print(f"\n⚠️  {failed} test(s) fallaron. Revisa los errores arriba.")


if __name__ == "__main__":
    main()
