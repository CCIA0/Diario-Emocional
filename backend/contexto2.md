2. Backend - FastAPI
requirements.txt
python
fastapi==0.111.0
uvicorn[standard]==0.30.4
pydantic==2.8.0
pysentimiento==0.6.0
google-generativeai==0.3.2
python-multipart==0.0.9
python-dotenv==1.0.1
sqlite3
app/core/config.py
python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Diario Emocional API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
settings = Settings()
app/services/ai_service.py
python
from pysentimiento import create_analyzer
import google.generativeai as genai
from ...core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

sentiment_analyzer = create_analyzer(task="sentiment", lang="es")
emotion_analyzer = create_analyzer(task="emotion", lang="es")

class AIService:
    @staticmethod
    def analyze_sentiment(text: str):
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
    def generate_feedback(user_text: str):
        prompt = f"""
        Eres un tutor emocional inteligente y empático para adolescentes. 
        Responde en español, sé breve (máximo 3-4 oraciones), empático y de apoyo.
        No des consejos genéricos, solo ayuda a identificar y normalizar emociones.
        
        Texto del usuario: "{user_text}"
        
        Feedback:
        """
        
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Gracias por compartir tus pensamientos. Es importante reflexionar sobre lo que sentimos. Error: {str(e)}"

ai_service = AIService()
app/models/schemas.py
python
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, Optional

class JournalEntryCreate(BaseModel):
    text: str
    user_id: str

class JournalEntryResponse(BaseModel):
    id: int
    text: str
    user_id: str
    sentiment_analysis: Dict[str, Any]
    ai_feedback: str
    created_at: datetime

class DashboardResponse(BaseModel):
    total_entries: int
    sentiment_distribution: Dict[str, int]
    emotion_distribution: Dict[str, int]
    recent_activity: list
app/services/database.py
python
import sqlite3
from datetime import datetime
from typing import List, Dict, Any

class Database:
    def __init__(self, db_path: str = "diario.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS journal_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    text TEXT NOT NULL,
                    sentiment_analysis TEXT,
                    ai_feedback TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def create_journal_entry(self, user_id: str, text: str, 
                           sentiment_analysis: dict, ai_feedback: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO journal_entries (user_id, text, sentiment_analysis, ai_feedback)
                VALUES (?, ?, ?, ?)
            """, (user_id, text, str(sentiment_analysis), ai_feedback))
            conn.commit()
            return cursor.lastrowid
    
    def get_user_entries(self, user_id: str) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM journal_entries 
                WHERE user_id = ? 
                ORDER BY created_at DESC
            """, (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_all_entries_for_dashboard(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM journal_entries")
            return [dict(row) for row in cursor.fetchall()]

db = Database()
app/api/endpoints/journal.py
python
from fastapi import APIRouter, HTTPException
from ...models.schemas import JournalEntryCreate, JournalEntryResponse
from ...services.database import db
from ...services.ai_service import ai_service
from datetime import datetime

router = APIRouter()

@router.post("/entries", response_model=JournalEntryResponse)
async def create_journal_entry(entry: JournalEntryCreate):
    try:
        analysis = ai_service.analyze_sentiment(entry.text)
        feedback = ai_service.generate_feedback(entry.text)
        
        entry_id = db.create_journal_entry(
            entry.user_id, entry.text, analysis, feedback
        )
        
        return {
            "id": entry_id,
            "text": entry.text,
            "user_id": entry.user_id,
            "sentiment_analysis": analysis,
            "ai_feedback": feedback,
            "created_at": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/entries/{user_id}")
async def get_user_entries(user_id: str):
    try:
        entries = db.get_user_entries(user_id)
        return entries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
app/api/endpoints/dashboard.py
python
from fastapi import APIRouter
from ...services.database import db
from ...models.schemas import DashboardResponse
from collections import Counter
import ast

router = APIRouter()

@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard():
    entries = db.get_all_entries_for_dashboard()
    
    sentiment_counter = Counter()
    emotion_counter = Counter()
    
    for entry in entries:
        try:
            analysis = ast.literal_eval(entry['sentiment_analysis'])
            sentiment = analysis['sentiment']['label']
            emotion = analysis['emotion']['label']
            
            sentiment_counter[sentiment] += 1
            emotion_counter[emotion] += 1
        except:
            continue
    
    return DashboardResponse(
        total_entries=len(entries),
        sentiment_distribution=dict(sentiment_counter),
        emotion_distribution=dict(emotion_counter),
        recent_activity=entries[:5]
    )
app/main.py
python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.endpoints import journal, dashboard

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(journal.router, prefix="/api/v1/journal", tags=["journal"])
app.include_router(dashboard.router, prefix="/api/v1", tags=["dashboard"])

@app.get("/")
async def root():
    return {"message": "Diario Emocional API funcionando!"}