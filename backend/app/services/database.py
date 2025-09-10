from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
from ..models.database_models import JournalEntry
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_journal_entry(self, user_id: str, text: str, 
                           sentiment_analysis: dict, ai_feedback: str) -> JournalEntry:
        try:
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
            logger.info(f"Entrada creada exitosamente para usuario {user_id}, ID: {new_entry.id}")
            return new_entry
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creando entrada para usuario {user_id}: {str(e)}")
            raise
    
    def get_user_entries(self, user_id: str) -> List[Dict[str, Any]]:
        try:
            logger.info(f"Buscando entradas para usuario: {user_id}")
            entries = self.db.query(JournalEntry)\
                .filter(JournalEntry.user_id == user_id)\
                .order_by(JournalEntry.created_at.desc())\
                .all()
            
            logger.info(f"Encontradas {len(entries)} entradas para usuario {user_id}")
            
            result = []
            for entry in entries:
                try:
                    entry_dict = entry.to_dict()
                    # Convertir string JSON back to dict
                    if entry_dict["sentiment_analysis"]:
                        entry_dict["sentiment_analysis"] = json.loads(entry_dict["sentiment_analysis"])
                    result.append(entry_dict)
                except json.JSONDecodeError as e:
                    logger.warning(f"Error decodificando JSON para entrada {entry.id}: {e}")
                    # Si hay error con el JSON, mantener el string original
                    entry_dict["sentiment_analysis"] = {"error": "Invalid JSON format"}
                    result.append(entry_dict)
                except Exception as e:
                    logger.error(f"Error procesando entrada {entry.id}: {e}")
                    # Agregar entrada básica sin análisis
                    result.append({
                        "id": entry.id,
                        "user_id": entry.user_id,
                        "text": entry.text,
                        "ai_feedback": entry.ai_feedback,
                        "created_at": entry.created_at.isoformat() if entry.created_at else None,
                        "error": "Error processing entry"
                    })
            
            return result
            
        except Exception as e:
            logger.error(f"Error obteniendo entradas para usuario {user_id}: {str(e)}")
            raise
    
    def get_all_entries_for_dashboard(self) -> List[Dict[str, Any]]:
        try:
            entries = self.db.query(JournalEntry).all()
            logger.info(f"Total de entradas en la base de datos: {len(entries)}")
            
            result = []
            for entry in entries:
                try:
                    entry_dict = entry.to_dict()
                    if entry_dict["sentiment_analysis"]:
                        entry_dict["sentiment_analysis"] = json.loads(entry_dict["sentiment_analysis"])
                    result.append(entry_dict)
                except Exception as e:
                    logger.warning(f"Error procesando entrada {entry.id} para dashboard: {e}")
                    # Continuar con las demás entradas
                    continue
            
            return result
            
        except Exception as e:
            logger.error(f"Error obteniendo todas las entradas: {str(e)}")
            raise