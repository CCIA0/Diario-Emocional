#!/usr/bin/env python3
"""
Test completo para verificar que la base de datos SQLite + SQLAlchemy funciona.
"""

def test_database():
    print("🧪 Iniciando test de base de datos...")
    print("=" * 50)
    
    try:
        # Test de importación
        from app.database import engine, create_tables, get_db
        from app.models.database_models import Base, JournalEntry
        from sqlalchemy import inspect
        from sqlalchemy.orm import Session
        import json
        
        print("✅ Módulos de base de datos importados correctamente")
        
        # Crear tablas
        create_tables()
        print("✅ Tablas creadas/existen")
        
        # Verificar estructura de la base de datos
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"📊 Tablas en la base de datos: {tables}")
        
        if 'journal_entries' not in tables:
            print("�ERROR: La tabla journal_entries no existe")
            return False
        
        # Verificar estructura de la tabla
        columns = inspector.get_columns('journal_entries')
        print("\n📋 Estructura de la tabla journal_entries:")
        for col in columns:
            print(f"   - {col['name']}: {col['type']} {'(PK)' if col.get('primary_key') else ''}")
        
        # Test de operaciones CRUD
        print("\n🔍 Probando operaciones de base de datos...")
        
        # Crear una sesión
        with Session(engine) as session:
            # Test de creación
            test_entry = JournalEntry(
                user_id="test_user",
                text="Este es un texto de prueba para la base de datos",
                sentiment_analysis=json.dumps({
                    "sentiment": {"label": "POS", "probabilities": {"POS": 0.9, "NEG": 0.1}},
                    "emotion": {"label": "joy", "probabilities": {"joy": 0.8, "others": 0.2}}
                }),
                ai_feedback="Feedback de prueba generado por la IA"
            )
            
            session.add(test_entry)
            session.commit()
            print("✅ Entrada creada correctamente")
            print(f"   ID generado: {test_entry.id}")
            
            # Test de lectura
            entries = session.query(JournalEntry).filter_by(user_id="test_user").all()
            print(f"✅ Entradas encontradas: {len(entries)}")
            
            for entry in entries:
                print(f"   📝 Entry {entry.id}: {entry.text[:50]}...")
                if entry.sentiment_analysis:
                    sentiment_data = json.loads(entry.sentiment_analysis)
                    print(f"   🎯 Sentimiento: {sentiment_data.get('sentiment', {}).get('label', 'N/A')}")
            
            # Test de actualización
            if entries:
                entry = entries[0]
                original_text = entry.text
                entry.text = "Texto actualizado para prueba"
                session.commit()
                print("✅ Entrada actualizada correctamente")
                
                # Revertir cambio
                entry.text = original_text
                session.commit()
            
            # Test de eliminación (limpieza)
            session.query(JournalEntry).filter_by(user_id="test_user").delete()
            session.commit()
            print("✅ Entradas de prueba eliminadas (limpieza)")
        
        # Verificar que la base de datos persiste
        db_file = "diario.db"
        import os
        if os.path.exists(db_file):
            size_kb = os.path.getsize(db_file) / 1024
            print(f"💾 Base de datos persistente: {db_file} ({size_kb:.1f} KB)")
        else:
            print("❌ La base de datos no se creó correctamente")
            return False
        
        print("🎉 ¡Todos los tests de base de datos pasaron correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en test de base de datos: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_database()