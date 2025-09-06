#!/usr/bin/env python3
"""
Test específico para modelos Gemini gratuitos
"""

def test_gemini():
    print("🧪 Probando modelos Gemini GRATUITOS...")
    print("=" * 50)
    
    try:
        import google.generativeai as genai
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            print("❌ No API key found")
            return False
        
        genai.configure(api_key=api_key)
        
        # MODELOS GRATUITOS A PROBAR (en orden de preferencia)
        free_models = [
            "gemini-1.5-flash-latest",    # ← MEJOR OPCIÓN
            "gemini-1.5-flash",           # ← Alternativa
            "gemini-2.0-flash-lite",      # ← Modelo ligero
            "gemini-2.0-flash-lite-001",  # ← Otra alternativa
        ]
        
        print("🔍 Probando modelos gratuitos...")
        
        for model_name in free_models:
            try:
                print(f"   Testing: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Responde con 'Hola, funciona' si estás operativo")
                
                if "hola" in response.text.lower() or "funciona" in response.text.lower():
                    print(f"   ✅ {model_name} - FUNCIONA! Respuesta: {response.text.strip()}")
                    return True, model_name
                else:
                    print(f"   ⚠️  {model_name} - Respuesta inesperada: {response.text.strip()}")
                    
            except Exception as e:
                error_msg = str(e)
                if "quota" in error_msg.lower() or "429" in error_msg:
                    print(f"   ❌ {model_name} - Límite de quota excedido")
                elif "404" in error_msg:
                    print(f"   ❌ {model_name} - Modelo no encontrado")
                else:
                    print(f"   ❌ {model_name} - Error: {error_msg[:80]}...")
                continue
        
        print("\n❌ Ningún modelo gratuito funcionó")
        return False, None
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False, None

def update_to_free_model(model_name):
    """Actualiza el archivo ai_service.py al modelo gratuito"""
    try:
        with open('app/services/ai_service.py', 'r') as f:
            content = f.read()
        
        # Buscar y reemplazar la línea del modelo
        import re
        new_content = re.sub(
            r'model = genai\.GenerativeModel\(["\']([^"\']+)["\']\)',
            f'model = genai.GenerativeModel("{model_name}")',
            content
        )
        
        with open('app/services/ai_service.py', 'w') as f:
            f.write(new_content)
        
        print(f"✅ Actualizado a modelo gratuito: {model_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando: {e}")
        return False

if __name__ == "__main__":
    success, model_name = test_gemini()
    
    if success:
        print(f"\n🎉 Modelo gratuito encontrado: {model_name}")
        update_to_free_model(model_name)
        print("\n🚀 ¡Configuración completada! Tu proyecto ahora usa modelos gratuitos.")
    else:
        print("\n💡 Soluciones:")
        print("1. Espera 1 hora y vuelve a probar (límites de quota)")
        print("2. Crea una nueva API Key en Google AI Studio")
        print("3. Verifica que tu cuenta Google tenga acceso a Gemini")