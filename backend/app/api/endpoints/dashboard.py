from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...services.database import DatabaseService
from ...models.schemas import DashboardResponse
from ...database import get_db
from collections import Counter
import json

router = APIRouter()

@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(db: Session = Depends(get_db)):
    db_service = DatabaseService(db)
    entries = db_service.get_all_entries_for_dashboard()
    
    sentiment_counter = Counter()
    emotion_counter = Counter()
    
    for entry in entries:
        try:
            analysis = entry['sentiment_analysis']
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