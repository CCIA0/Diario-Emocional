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
        Análisis de sentimientos usando Gemini AI 
        Detecta emociones específicas para mostrar stickers apropiados
        """
        try:
            # Prompt mejorado para análisis más preciso de emociones
            prompt = f"""
            Analiza el sentimiento y emoción predominante en el siguiente texto en español.
            
            Para SENTIMENT, clasifica como:
            - POS: Emociones positivas (alegría, amor, esperanza, gratitud, orgullo, etc.)
            - NEG: Emociones negativas (tristeza, enojo, miedo, frustración, ansiedad, etc.)  
            - NEU: Neutral o mixto
            
            Para EMOTION, identifica la emoción más específica:
            - joy: alegría, felicidad, diversión, entusiasmo
            - sadness: tristeza, melancolía, decepción, pena
            - anger: enojo, frustración, molestia, indignación
            - fear: miedo, ansiedad, preocupación, nervios
            - surprise: sorpresa, asombro
            - disgust: asco, disgusto, rechazo
            - love: amor, cariño, ternura
            - neutral: neutral, sin emoción clara
            
            Responde SOLO en formato JSON válido:
            {{
                "sentiment": {{"label": "POS", "confidence": 0.85}},
                "emotion": {{"label": "joy", "confidence": 0.80}}
            }}
            
            Texto a analizar: "{text}"
            """
            
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            response = model.generate_content(prompt)
            
            # Parsear respuesta de Gemini
            import json
            import re
            
            # Limpiar la respuesta para extraer solo el JSON
            response_text = response.text.strip()
            
            # Buscar el JSON en la respuesta
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                result = json.loads(json_str)
                
                sentiment_label = result["sentiment"]["label"]
                sentiment_confidence = result["sentiment"]["confidence"]
                emotion_label = result["emotion"]["label"]
                emotion_confidence = result["emotion"]["confidence"]
                
                return {
                    "sentiment": {
                        "label": sentiment_label,
                        "probabilities": {sentiment_label: sentiment_confidence}
                    },
                    "emotion": {
                        "label": emotion_label,
                        "probabilities": {emotion_label: emotion_confidence}
                    }
                }
            else:
                # Si no se encuentra JSON válido, analizar manualmente
                response_lower = response_text.lower()
                
                # Detectar sentimiento basado en palabras clave
                if any(word in response_lower for word in ['alegr', 'feliz', 'content', 'bien', 'positiv', 'amor', 'bueno']):
                    return {
                        "sentiment": {"label": "POS", "probabilities": {"POS": 0.7}},
                        "emotion": {"label": "joy", "probabilities": {"joy": 0.7}}
                    }
                elif any(word in response_lower for word in ['trist', 'mal', 'deprimi', 'pena', 'llor', 'dolor']):
                    return {
                        "sentiment": {"label": "NEG", "probabilities": {"NEG": 0.7}},
                        "emotion": {"label": "sadness", "probabilities": {"sadness": 0.7}}
                    }
                elif any(word in response_lower for word in ['enoj', 'molest', 'rabia', 'frustr', 'odio']):
                    return {
                        "sentiment": {"label": "NEG", "probabilities": {"NEG": 0.7}},
                        "emotion": {"label": "anger", "probabilities": {"anger": 0.7}}
                    }
                elif any(word in response_lower for word in ['mied', 'ansied', 'preocup', 'nervi', 'temor']):
                    return {
                        "sentiment": {"label": "NEG", "probabilities": {"NEG": 0.7}},
                        "emotion": {"label": "fear", "probabilities": {"fear": 0.7}}
                    }
                else:
                    return {
                        "sentiment": {"label": "NEU", "probabilities": {"NEU": 0.6}},
                        "emotion": {"label": "neutral", "probabilities": {"neutral": 0.6}}
                    }
                
        except Exception as e:
            print(f"Error en análisis de sentimientos: {e}")
            
            # Análisis de fallback más inteligente basado en palabras clave
            text_lower = text.lower()
            
            # Detectar emociones positivas
            if any(word in text_lower for word in ['feliz', 'alegr', 'content', 'bien', 'genial', 'amor', 'bueno', 'perfecto', 'increíble']):
                return {
                    "sentiment": {"label": "POS", "probabilities": {"POS": 0.8}},
                    "emotion": {"label": "joy", "probabilities": {"joy": 0.8}}
                }
            
            # Detectar tristeza
            elif any(word in text_lower for word in ['trist', 'deprimi', 'llor', 'pena', 'dolor', 'mal', 'horrible', 'terrible']):
                return {
                    "sentiment": {"label": "NEG", "probabilities": {"NEG": 0.8}},
                    "emotion": {"label": "sadness", "probabilities": {"sadness": 0.8}}
                }
            
            # Detectar enojo
            elif any(word in text_lower for word in ['enoj', 'molest', 'rabia', 'frustr', 'odio', 'furioso', 'irritad']):
                return {
                    "sentiment": {"label": "NEG", "probabilities": {"NEG": 0.8}},
                    "emotion": {"label": "anger", "probabilities": {"anger": 0.8}}
                }
            
            # Detectar miedo/ansiedad
            elif any(word in text_lower for word in ['mied', 'ansied', 'preocup', 'nervi', 'temor', 'pánico', 'asust']):
                return {
                    "sentiment": {"label": "NEG", "probabilities": {"NEG": 0.8}},
                    "emotion": {"label": "fear", "probabilities": {"fear": 0.8}}
                }
            
            # Default neutral
            else:
                return {
                    "sentiment": {"label": "NEU", "probabilities": {"NEU": 0.6}},
                    "emotion": {"label": "neutral", "probabilities": {"neutral": 0.6}}
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