from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...services.database import DatabaseService
from ...models.schemas import DashboardResponse
from ...database import get_db
from collections import Counter
import json
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(db: Session = Depends(get_db)):
    db_service = DatabaseService(db)
    entries = db_service.get_all_entries_for_dashboard()
    
    # Calcular métricas
    total_entries = len(entries)
    
    # Contadores para sentimientos y emociones
    sentiment_counter = Counter()
    emotion_counter = Counter()
    
    # Calcular entradas de la última semana
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    entries_last_week = 0
    
    # Obtener usuarios únicos
    user_ids = set()
    
    for entry in entries:
        try:
            # Contar usuarios únicos
            user_ids.add(entry['user_id'])
            
            # Verificar si es de la última semana
            if 'created_at' in entry and entry['created_at']:
                entry_date = datetime.fromisoformat(entry['created_at'].replace('Z', '+00:00'))
                if entry_date >= one_week_ago:
                    entries_last_week += 1
            
            # Procesar análisis de sentimientos
            if 'sentiment_analysis' in entry and entry['sentiment_analysis']:
                # Si es string, convertirlo a dict
                if isinstance(entry['sentiment_analysis'], str):
                    analysis = json.loads(entry['sentiment_analysis'])
                else:
                    analysis = entry['sentiment_analysis']
                
                sentiment = analysis.get('sentiment', {}).get('label', 'unknown')
                emotion = analysis.get('emotion', {}).get('label', 'unknown')
                
                sentiment_counter[sentiment] += 1
                emotion_counter[emotion] += 1
                
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Error procesando entrada: {e}")
            continue
    
    # Calcular porcentajes para distribución de sentimientos
    sentiment_distribution = []
    total_sentiments = sum(sentiment_counter.values())
    
    for sentiment, count in sentiment_counter.items():
        percentage = round((count / total_sentiments) * 100) if total_sentiments > 0 else 0
        sentiment_distribution.append({
            "sentiment": sentiment,
            "count": count,
            "percentage": percentage
        })
    
    # Obtener emociones más comunes (top 5)
    top_emotions = [{"emotion": emotion, "count": count} 
                   for emotion, count in emotion_counter.most_common(5)]
    
    # Estadísticas por usuario
    users_stats = []
    for user_id in user_ids:
        user_entries = [e for e in entries if e.get('user_id') == user_id]
        user_sentiment_counter = Counter()
        user_emotion_counter = Counter()
        
        for entry in user_entries:
            try:
                if 'sentiment_analysis' in entry and entry['sentiment_analysis']:
                    if isinstance(entry['sentiment_analysis'], str):
                        analysis = json.loads(entry['sentiment_analysis'])
                    else:
                        analysis = entry['sentiment_analysis']
                    
                    sentiment = analysis.get('sentiment', {}).get('label', 'unknown')
                    emotion = analysis.get('emotion', {}).get('label', 'unknown')
                    
                    user_sentiment_counter[sentiment] += 1
                    user_emotion_counter[emotion] += 1
            except:
                continue
        
        # Sentimiento y emoción dominante del usuario
        dominant_sentiment = user_sentiment_counter.most_common(1)
        dominant_emotion = user_emotion_counter.most_common(1)
        
        users_stats.append({
            "user_id": user_id,
            "entries_count": len(user_entries),
            "dominant_sentiment": dominant_sentiment[0][0] if dominant_sentiment else "unknown",
            "dominant_emotion": dominant_emotion[0][0] if dominant_emotion else "unknown"
        })
    
    # Calcular sentimiento promedio (0-1 scale)
    sentiment_scores = {
        'pos': 1.0,
        'neu': 0.5, 
        'neg': 0.0
    }
    total_score = 0
    count_with_sentiment = 0
    
    for sentiment, count in sentiment_counter.items():
        if sentiment in sentiment_scores:
            total_score += sentiment_scores[sentiment] * count
            count_with_sentiment += count
    
    avg_sentiment_score = total_score / count_with_sentiment if count_with_sentiment > 0 else 0.5
    
    return {
        "total_users": len(user_ids),
        "total_entries": total_entries,
        "avg_sentiment_score": avg_sentiment_score,
        "entries_last_week": entries_last_week,
        "sentiment_distribution": sentiment_distribution,
        "top_emotions": top_emotions,
        "users_stats": users_stats
    }