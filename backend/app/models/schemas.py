from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class JournalEntry(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class JournalEntryCreate(BaseModel):
    text: str
    user_id: str

class JournalEntryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class DashboardData(BaseModel):
    total_entries: int
    recent_entries: List[JournalEntry]

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