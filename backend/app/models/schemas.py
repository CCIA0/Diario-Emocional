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
    total_users: int
    total_entries: int
    avg_sentiment_score: float
    entries_last_week: int
    sentiment_distribution: List[Dict[str, Any]]
    top_emotions: List[Dict[str, Any]]
    users_stats: List[Dict[str, Any]]