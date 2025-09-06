from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ...models.schemas import JournalEntryCreate, JournalEntryResponse
from ...services.ai_service import ai_service
from ...database import get_db
from ...services.database import DatabaseService
from datetime import datetime
import json

router = APIRouter()

@router.post("/entries", response_model=JournalEntryResponse)
async def create_journal_entry(
    entry: JournalEntryCreate, 
    db: Session = Depends(get_db)
):
    try:
        db_service = DatabaseService(db)
        
        # Analizar con AI
        analysis = ai_service.analyze_sentiment(entry.text)
        feedback = ai_service.generate_feedback(entry.text)
        
        # Guardar en DB usando SQLAlchemy
        new_entry = db_service.create_journal_entry(
            entry.user_id, entry.text, analysis, feedback
        )
        
        # Convertir para la respuesta
        sentiment_dict = json.loads(new_entry.sentiment_analysis) if new_entry.sentiment_analysis else {}
        
        return JournalEntryResponse(
            id=new_entry.id,
            text=new_entry.text,
            user_id=new_entry.user_id,
            sentiment_analysis=sentiment_dict,
            ai_feedback=new_entry.ai_feedback,
            created_at=new_entry.created_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/entries/{user_id}")
async def get_user_entries(user_id: str, db: Session = Depends(get_db)):
    try:
        db_service = DatabaseService(db)
        entries = db_service.get_user_entries(user_id)
        return entries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))