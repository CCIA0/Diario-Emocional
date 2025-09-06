from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
from ..models.database_models import JournalEntry

class DatabaseService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_journal_entry(self, user_id: str, text: str, 
                           sentiment_analysis: dict, ai_feedback: str) -> JournalEntry:
        # Convertir el análisis de sentimientos a string JSON
        sentiment_str = json.dumps(sentiment_analysis)
        
        # Crear nueva entrada
        new_entry = JournalEntry(
            user_id=user_id,
            text=text,
            sentiment_analysis=sentiment_str,
            ai_feedback=ai_feedback
        )
        
        self.db.add(new_entry)
        self.db.commit()
        self.db.refresh(new_entry)
        return new_entry
    
    def get_user_entries(self, user_id: str) -> List[Dict[str, Any]]:
        entries = self.db.query(JournalEntry)\
            .filter(JournalEntry.user_id == user_id)\
            .order_by(JournalEntry.created_at.desc())\
            .all()
        
        result = []
        for entry in entries:
            entry_dict = entry.to_dict()
            # Convertir string JSON back to dict
            if entry_dict["sentiment_analysis"]:
                entry_dict["sentiment_analysis"] = json.loads(entry_dict["sentiment_analysis"])
            result.append(entry_dict)
        
        return result
    
    def get_all_entries_for_dashboard(self) -> List[Dict[str, Any]]:
        entries = self.db.query(JournalEntry).all()
        
        result = []
        for entry in entries:
            entry_dict = entry.to_dict()
            if entry_dict["sentiment_analysis"]:
                entry_dict["sentiment_analysis"] = json.loads(entry_dict["sentiment_analysis"])
            result.append(entry_dict)
        
        return result

# No necesitamos instanciar aquí, lo haremos en los endpoints