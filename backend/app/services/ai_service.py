from pydantic import BaseModel
from typing import List, Dict
from pysentimiento import create_analyzer
import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

sentiment_analyzer = create_analyzer(task="sentiment", lang="es")
emotion_analyzer = create_analyzer(task="emotion", lang="es")

class SentimentAnalysisResult(BaseModel):
    sentiment: str
    score: float

class AIService:
    @staticmethod
    def analyze_sentiment(text: str) -> dict:
        sentiment_result = sentiment_analyzer.predict(text)
        emotion_result = emotion_analyzer.predict(text)
        return {
            "sentiment": {
                "label": sentiment_result.output,
                "probabilities": sentiment_result.probas
            },
            "emotion": {
                "label": emotion_result.output,
                "probabilities": emotion_result.probas
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
        except Exception as e:
            return f"Gracias por compartir tus pensamientos. Es importante reflexionar sobre lo que sentimos. Error: {str(e)}"

ai_service = AIService()

# Example usage
# result = ai_service.analyze_sentiment("I love programming!")
# print(result)