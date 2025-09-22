from pydantic import BaseModel
from typing import List, Dict
import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

class SentimentAnalysisResult(BaseModel):
    sentiment: str
    score: float

class AIService:
    @staticmethod
    def analyze_sentiment(text: str) -> dict:
        """
        Análisis de sentimientos usando Gemini AI (versión simplificada para deploy)
        Temporalmente sin pysentimiento para evitar problemas de compilación
        """
        try:
            # Usar Gemini para análisis básico de sentimientos
            prompt = f"""
            Analiza el sentimiento y emoción del siguiente texto en español.
            Responde SOLO en formato JSON con esta estructura exacta:
            {{
                "sentiment": {{"label": "POS|NEU|NEG", "confidence": 0.95}},
                "emotion": {{"label": "joy|sadness|anger|fear|surprise|disgust", "confidence": 0.90}}
            }}
            
            Texto: "{text}"
            """
            
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            response = model.generate_content(prompt)
            
            # Parsear respuesta de Gemini (simplificado)
            import json
            try:
                result = json.loads(response.text.strip())
                return {
                    "sentiment": {
                        "label": result["sentiment"]["label"],
                        "probabilities": {result["sentiment"]["label"]: result["sentiment"]["confidence"]}
                    },
                    "emotion": {
                        "label": result["emotion"]["label"], 
                        "probabilities": {result["emotion"]["label"]: result["emotion"]["confidence"]}
                    }
                }
            except (json.JSONDecodeError, KeyError):
                # Fallback si el parsing falla
                return {
                    "sentiment": {
                        "label": "NEU",
                        "probabilities": {"NEU": 0.8}
                    },
                    "emotion": {
                        "label": "neutral",
                        "probabilities": {"neutral": 0.8}
                    }
                }
                
        except Exception as e:
            print(f"Error en análisis de sentimientos: {e}")
            # Fallback en caso de error
            return {
                "sentiment": {
                    "label": "NEU",
                    "probabilities": {"NEU": 0.5}
                },
                "emotion": {
                    "label": "neutral", 
                    "probabilities": {"neutral": 0.5}
                }
            }

    @staticmethod
    def generate_feedback(user_text: str) -> str:
        prompt = f"""
        Eres un tutor emocional inteligente y empático para adolescentes. 
        Responde en español, sé breve (máximo 3-4 oraciones), empático y de apoyo.
        No des consejos genéricos, solo ayuda a identificar y normalizar emociones.
        Texto del usuario: "{user_text}"
        Feedback:
        """
        try:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception:
            return "Gracias por compartir tus pensamientos. Es importante reflexionar sobre lo que sentimos."

ai_service = AIService()