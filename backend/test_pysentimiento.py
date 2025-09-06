#!/usr/bin/env python3
"""
Test completo para verificar que PySentimiento está instalado y funciona correctamente.
"""

def test_pysentimiento():
    print("🧪 Iniciando test de PySentimiento...")
    print("=" * 50)
    
    try:
        # Test de importación
        from pysentimiento import create_analyzer
        print("✅ Módulo pysentimiento importado correctamente")
        
        # Test de analizador de sentimientos
        print("\n🔍 Probando analizador de sentimientos...")
        sentiment_analyzer = create_analyzer(task="sentiment", lang="es")
        
        # Test con diferentes textos
        test_cases = [
            "Estoy muy feliz hoy",
            "Me siento terrible y triste",
            "Es un día normal, sin emociones fuertes",
            "¡Qué enojo me da esta situación!"
        ]
        
        for i, text in enumerate(test_cases, 1):
            result = sentiment_analyzer.predict(text)
            print(f"📝 Texto {i}: '{text}'")
            print(f"   🎯 Sentimiento: {result.output}")
            print(f"   📊 Probabilidades: {result.probas}")
            print()
        
        # Test de analizador de emociones
        print("🔍 Probando analizador de emociones...")
        emotion_analyzer = create_analyzer(task="emotion", lang="es")
        
        emotion_test_cases = [
            "Estoy emocionado por el proyecto",
            "Tengo miedo de no terminar a tiempo",
            "Me da asco la comida podrida",
            "¡Qué sorpresa tan agradable!"
        ]
        
        for i, text in enumerate(emotion_test_cases, 1):
            result = emotion_analyzer.predict(text)
            print(f"📝 Texto {i}: '{text}'")
            print(f"   🎯 Emoción: {result.output}")
            print(f"   📊 Probabilidades: {result.probas}")
            print()
        
        print("🎉 ¡Todos los tests de PySentimiento pasaron correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en test de PySentimiento: {e}")
        print("\n🔧 Solución:")
        print("1. Verifica que transformers y torch estén instalados")
        print("2. Ejecuta: pip install transformers torch")
        print("3. Reinstala pysentimiento: pip uninstall pysentimiento && pip install pysentimiento")
        return False

if __name__ == "__main__":
    test_pysentimiento()