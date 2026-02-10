"""
Demo del Sistema RAG Legal con Cohere

Ejecuta este script para ver el sistema en acción
"""
import os
from dotenv import load_dotenv
from rag_system import LegalRAGSystem


def mostrar_respuesta_estructurada(resultado: dict):
    """
    Muestra una respuesta estructurada de forma formateada

    Args:
        resultado: Diccionario con 'answer', 'fuentes', 'confianza'
    """
    # Emoji según nivel de confianza
    confianza_emoji = {
        "alta": "🟢",
        "media": "🟡",
        "baja": "🔴"
    }

    emoji = confianza_emoji.get(resultado.get('confianza', 'media'), "⚪")

    print("\n" + "=" * 60)
    print("📋 RESPUESTA:")
    print("=" * 60)
    print(resultado['answer'])

    # Mostrar fuentes
    if resultado.get('fuentes'):
        print("\n📚 FUENTES CITADAS:")
        for fuente in resultado['fuentes']:
            relevancia_pct = fuente['relevancia'] * 100
            print(f"   • {fuente['nombre']} (relevancia: {relevancia_pct:.0f}%)")

    # Mostrar nivel de confianza
    print(f"\n{emoji} Nivel de confianza: {resultado.get('confianza', 'N/A').upper()}")


def main():
    """
    Función principal de demostración
    """
    # Cargar variables de entorno
    load_dotenv()
    api_key = os.getenv("COHERE_API_KEY")
    
    if not api_key:
        print("❌ ERROR: No se encontró COHERE_API_KEY")
        print("Por favor:")
        print("1. Copia .env.example a .env")
        print("2. Agrega tu API key de Cohere")
        print("3. Obtén una gratis en: https://dashboard.cohere.com/api-keys")
        return
    
    print("=" * 60)
    print("🎓 DEMO: Sistema RAG Legal con Cohere")
    print("=" * 60)
    
    # Inicializar sistema
    print("\n📦 Inicializando sistema...")
    rag = LegalRAGSystem(
        api_key=api_key,
        model="command-r-plus-08-2024"  # Puedes cambiar a "command-r-plus" si prefieres
    )
    
    # Cargar documentos
    rag.load_documents_from_folder("data/legal_docs")
    
    # Lista de consultas de ejemplo
    consultas_ejemplo = [
        "¿Cuál es el plazo para apelar una sentencia civil?",
        "¿Qué es un recurso de casación?",
        "¿Cómo se cuentan los plazos procesales?",
        "¿Qué efectos tiene el recurso de apelación?",
    ]
    
    print("\n" + "=" * 60)
    print("📋 CONSULTAS DE EJEMPLO")
    print("=" * 60)
    for idx, q in enumerate(consultas_ejemplo, 1):
        print(f"{idx}. {q}")
    
    # Modo interactivo o demo automático
    print("\n¿Qué deseas hacer?")
    print("1. Ver demo automática (ejecuta todas las consultas)")
    print("2. Hacer consultas personalizadas")
    print("3. Modo estructurado con Pydantic AI (respuestas con fuentes y confianza)")

    opcion = input("\nSelecciona (1, 2 o 3): ").strip()

    if opcion == "1":
        # Demo automática
        print("\n🚀 Ejecutando demo automática...\n")
        for consulta in consultas_ejemplo[:2]:  # Solo 2 consultas para no gastar mucho API
            resultado = rag.query(
                query=consulta,
                top_k=3,  # Top 3 documentos más relevantes
                initial_candidates=10
            )
            print(resultado['answer'])
            print("\n" + "-" * 60 + "\n")
            
    elif opcion == "2":
        # Modo interactivo
        print("\n💬 Modo interactivo activado")
        print("Escribe 'salir' para terminar\n")
        
        while True:
            consulta = input("Tu consulta: ").strip()
            
            if consulta.lower() in ['salir', 'exit', 'quit']:
                print("\n👋 ¡Hasta luego!")
                break
            
            if not consulta:
                continue
            
            resultado = rag.query(
                query=consulta,
                top_k=5,
                initial_candidates=20
            )
            
            print(resultado['answer'])
            print("\n" + "-" * 60 + "\n")

    elif opcion == "3":
        # Modo estructurado con Pydantic AI
        print("\n🧠 Modo estructurado con Pydantic AI activado")
        print("Las respuestas incluirán fuentes citadas y nivel de confianza")
        print("Escribe 'salir' para terminar\n")

        while True:
            consulta = input("Tu consulta: ").strip()

            if consulta.lower() in ['salir', 'exit', 'quit']:
                print("\n👋 ¡Hasta luego!")
                break

            if not consulta:
                continue

            resultado = rag.query(
                query=consulta,
                structured=True
            )

            # Mostrar respuesta estructurada
            mostrar_respuesta_estructurada(resultado)
            print("\n" + "-" * 60 + "\n")

    else:
        print("❌ Opción no válida")
    
    print("\n✅ Demo completado")
    print("\n📚 Próximos pasos:")
    print("   - Revisa el código en rag_system.py")
    print("   - Agrega tus propios documentos en data/legal_docs/")
    print("   - Experimenta con diferentes consultas")
    print("   - Lee el README.md para ideas de mejora")


if __name__ == "__main__":
    main()
