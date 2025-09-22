#!/usr/bin/env python3
"""
Script de inicialización para el deploy en Render
Este script se ejecuta después del build para preparar la base de datos
"""
import os
import sys
from pathlib import Path

# Añadir el directorio de la aplicación al path
sys.path.append(str(Path(__file__).parent))

from app.database import create_tables, engine
from app.core.config import settings

def init_database():
    """Inicializar la base de datos en producción"""
    try:
        print("🔄 Iniciando configuración de base de datos...")
        
        # Verificar configuración
        print(f"📊 Base de datos: {settings.DATABASE_URL}")
        print(f"🌍 Entorno: {settings.ENVIRONMENT}")
        
        # Crear tablas
        create_tables()
        
        # Verificar que las tablas se crearon
        with engine.connect() as conn:
            result = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in result]
            print(f"✅ Tablas creadas: {tables}")
        
        print("🎉 Base de datos configurada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error al configurar la base de datos: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()