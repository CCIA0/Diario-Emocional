from app.core.config import settings

print("🔍 Probando configuración...")
print(f"Project Name: {settings.PROJECT_NAME}")
print(f"API Key length: {len(settings.GEMINI_API_KEY)}")
print(f"API Key (primeros 10 chars): {settings.GEMINI_API_KEY[:10]}...")

if settings.GEMINI_API_KEY:
    print("✅ API Key cargada correctamente!")
else:
    print("❌ ERROR: API Key no encontrada")
    print("Verifica que:")
    print("1. El archivo .env esté en backend/")
    print("2. La variable se llame GEMINI_API_KEY")
    print("3. Hayas reiniciado Python después de crear el .env")