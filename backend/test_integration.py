#!/usr/bin/env python3
"""
Test de integración completo CORREGIDO
"""

def test_integration_fixed():
    print("🧪 Iniciando test de integración completa (CORREGIDO)...")
    print("=" * 60)
    
    # Test 1: PySentimiento
    print("\n1. 🔍 Probando PySentimiento...")
    try:
        from test_pysentimiento import test_pysentimiento
        pysentimiento_ok = test_pysentimiento()
    except Exception as e:
        print(f"❌ Error importando test_pysentimiento: {e}")
        pysentimiento_ok = False
    
    # Test 2: Gemini
    print("\n2. 🔍 Probando Gemini...")
    try:
        from test_gemini import test_gemini
        gemini_ok = test_gemini()
    except Exception as e:
        print(f"❌ Error importando test_gemini: {e}")
        gemini_ok = False
    
    # Test 3: Base de datos
    print("\n3. 🔍 Probando Base de Datos...")
    try:
        from test_database import test_database
        database_ok = test_database()
    except Exception as e:
        print(f"❌ Error importando test_database: {e}")
        database_ok = False
    
    # Test 4: Servicios combinados (CORREGIDO)
    print("\n4. 🔍 Probando Servicios Combinados...")
    integration_ok = False
    try:
        from app.services.ai_service import AIService
        from app.database import engine  # ← Importar engine
        from app.services.database import DatabaseService
        from app.models.database_models import JournalEntry
        from sqlalchemy.orm import Session
        import json
        
        # Crear instancia de servicios
        ai_service = AIService()
        
        # Test de análisis de texto
        test_text = "Estoy muy contento con el progreso del proyecto integrado"
        print(f"📝 Texto de prueba: '{test_text}'")
        
        # Análisis con PySentimiento
        analysis = ai_service.analyze_sentiment(test_text)
        print(f"🎯 Análisis de sentimiento: {analysis['sentiment']['label']}")
        print(f"😄 Análisis de emoción: {analysis['emotion']['label']}")
        
        # Generación con Gemini (gratuito)
        feedback = ai_service.generate_feedback(test_text)
        print(f"🤖 Feedback de Gemini: {feedback}")
        
        # Integración con base de datos (CORREGIDO)
        with Session(engine) as session:  # ← USAR engine, NO get_db()
            db_service = DatabaseService(session)
            
            # Guardar en base de datos
            entry = db_service.create_journal_entry(
                "integration_test_user",
                test_text,
                analysis,
                feedback
            )
            print(f"💾 Entrada guardada en BD con ID: {entry.id}")
            
            # Leer de la base de datos
            entries = db_service.get_user_entries("integration_test_user")
            print(f"📖 Entradas recuperadas: {len(entries)}")
            
            # Limpiar
            session.query(JournalEntry).filter_by(user_id="integration_test_user").delete()
            session.commit()
        
        print("✅ Integración de servicios funcionando correctamente!")
        integration_ok = True
        
    except Exception as e:
        print(f"❌ Error en integración: {e}")
        import traceback
        traceback.print_exc()
        integration_ok = False
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS:")
    print(f"   PySentimiento: {'✅' if pysentimiento_ok else '❌'}")
    print(f"   Gemini: {'✅' if gemini_ok else '❌'}")
    print(f"   Base de Datos: {'✅' if database_ok else '❌'}")
    print(f"   Integración: {'✅' if integration_ok else '❌'}")
    
    all_ok = all([pysentimiento_ok, gemini_ok, database_ok, integration_ok])
    
    if all_ok:
        print("\n🎉 ¡TODOS LOS TESTS PASARON! El sistema está listo.")
        print("\n🚀 Para ejecutar el servidor:")
        print("   cd backend/")
        print("   uvicorn app.main:app --reload --port 8000")
        print("\n🌐 Luego abre: http://localhost:8000/docs")
    else:
        print("\n❌ Algunos tests fallaron. Revisa los mensajes de error arriba.")
    
    return all_ok

if __name__ == "__main__":
    test_integration_fixed()