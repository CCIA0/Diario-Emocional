Documentación del Backend - Diario Emocional API
📋 Descripción General
El backend es una API REST construida con FastAPI que gestiona un diario emocional con análisis de sentimientos mediante IA usando PySentimiento y Gemini.

🏗️ Arquitectura
Estructura de Carpetas
text
diario_emocional_mvp/
└── backend/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py                 # Punto de entrada de la aplicación
    │   ├── api/
    │   │   ├── __init__.py
    │   │   └── endpoints/
    │   │       ├── __init__.py
    │   │       ├── journal.py      # Endpoints del diario
    │   │       └── dashboard.py    # Endpoints del dashboard
    │   ├── core/
    │   │   ├── __init__.py
    │   │   ├── config.py           # Configuración de la aplicación
    │   │   └── security.py         # Autenticación básica
    │   ├── models/
    │   │   ├── __init__.py
    │   │   └── schemas.py          # Esquemas Pydantic
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── ai_service.py       # Servicios de IA (PySentimiento & Gemini)
    │   │   └── database.py         # Servicio de base de datos
    │   └── database.py             # Configuración de la base de datos
    ├── requirements.txt
    └── README.md
🗄️ Modelos de Base de Datos
JournalEntry (SQLAlchemy)
python
class JournalEntry(Base):
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    sentiment_analysis = Column(Text)  # Almacenado como JSON string
    ai_feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
📊 Endpoints Disponibles
Journal Endpoints (/api/v1/journal)
Método	Endpoint	Descripción	Body
POST	/entries	Crear una nueva entrada	{"text": string, "user_id": string}
GET	/entries/{user_id}	Obtener entradas de un usuario	-
Dashboard Endpoints (/api/v1)
Método	Endpoint	Descripción
GET	/dashboard	Obtener estadísticas generales
🎯 Esquemas de Respuesta (Pydantic)
JournalEntryResponse
python
class JournalEntryResponse(BaseModel):
    id: int
    text: str
    user_id: str
    sentiment_analysis: Dict[str, Any]
    ai_feedback: str
    created_at: datetime
DashboardResponse
python
class DashboardResponse(BaseModel):
    total_users: int
    total_entries: int
    avg_sentiment_score: float
    entries_last_week: int
    sentiment_distribution: List[Dict[str, Any]]
    top_emotions: List[Dict[str, Any]]
    users_stats: List[Dict[str, Any]]
🔧 Configuración
Variables de Entorno (config.py)
python
class Settings(BaseSettings):
    PROJECT_NAME: str = "Diario Emocional API"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./diario_emocional.db"
    GEMINI_API_KEY: Optional[str] = None
Base de Datos
SQLite con SQLAlchemy ORM

Conexión con check_same_thread=False para SQLite

Sesiones gestionadas automáticamente con dependency injection

🤖 Servicios de IA
AIService (ai_service.py)
python
class AIService:
    def __init__(self):
        self.analyzer = create_analyzer(task="sentiment", lang="es")
        self.emotion_analyzer = create_analyzer(task="emotion", lang="es")
        self.gemini_client = None  # Configurable con API key
    
    def analyze_sentiment(self, text: str) -> Dict:
        # Usa PySentimiento para análisis en español
        return self.analyzer.predict(text)
    
    def generate_feedback(self, text: str, sentiment: Dict) -> str:
        # Genera feedback usando Gemini o lógica predefinida
        return "Feedback personalizado basado en el análisis"
🚀 Características Principales
1. Gestión de Entradas
✅ Creación de entradas con análisis de sentimientos

✅ Almacenamiento de feedback de IA

✅ Registro temporal automático

✅ Validación de datos con Pydantic

2. Análisis de Sentimientos
✅ Procesamiento de texto en español con PySentimiento

✅ Detección de emociones (alegría, tristeza, enojo, etc.)

✅ Clasificación de sentimientos (POS/NEG/NEU)

✅ Integración con Gemini para feedback avanzado

3. Dashboard Analytics
✅ Estadísticas de usuarios únicos

✅ Distribución de sentimientos con porcentajes

✅ Emociones más comunes (top 5)

✅ Métricas por usuario individual

✅ Actividad de la última semana

4. Seguridad y Configuración
✅ CORS configurado para frontend Angular

✅ Validación de datos con Pydantic

✅ Manejo de errores estructurado

✅ Configuración mediante variables de entorno

🛠️ Tecnologías Utilizadas
FastAPI: Framework web moderno y rápido

SQLAlchemy: ORM para base de datos

Pydantic: Validación de datos y serialización

PySentimiento: NLP para análisis de sentimientos en español

Google Gemini: IA para generación de feedback (opcional)

SQLite: Base de datos embebida para MVP

Uvicorn: Servidor ASGI de alto rendimiento

📈 Flujo de Datos
1. Creación de Entrada
text
Cliente → POST /entries → FastAPI → AIService → DatabaseService → SQLite
                                 ↓
                         Respuesta con análisis → Cliente
2. Consulta de Dashboard
text
Cliente → GET /dashboard → FastAPI → DatabaseService → SQLite
                                     ↓
                         Procesamiento estadístico → Cliente
🔍 Ejemplos de Uso
Crear entrada
bash
curl -X POST "http://localhost:8000/api/v1/journal/entries" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hoy me siento muy feliz con mis logros", "user_id": "usuario_1"}'
Obtener dashboard
bash
curl "http://localhost:8000/api/v1/dashboard"
Obtener entradas de usuario
bash
curl "http://localhost:8000/api/v1/journal/entries/usuario_1"
🚦 Estado del API
Health Check
bash
curl "http://localhost:8000/health"
Root Endpoint
bash
curl "http://localhost:8000/"
📊 Estructura de Respuestas
Entrada de Diario Exitosa
json
{
  "id": 1,
  "text": "Hoy me siento muy feliz",
  "user_id": "usuario_1",
  "sentiment_analysis": {
    "sentiment": {"label": "POS", "probabilities": {"POS": 0.95, "NEU": 0.03, "NEG": 0.02}},
    "emotion": {"label": "joy", "probabilities": {"joy": 0.85, "surprise": 0.10, "neutral": 0.05}}
  },
  "ai_feedback": "¡Qué bueno que te sientes feliz! Sigue así...",
  "created_at": "2024-01-15T10:30:00Z"
}
Dashboard Response
json
{
  "total_users": 3,
  "total_entries": 15,
  "avg_sentiment_score": 0.72,
  "entries_last_week": 5,
  "sentiment_distribution": [
    {"sentiment": "POS", "count": 8, "percentage": 53},
    {"sentiment": "NEU", "count": 5, "percentage": 33},
    {"sentiment": "NEG", "count": 2, "percentage": 14}
  ],
  "top_emotions": [
    {"emotion": "joy", "count": 6},
    {"emotion": "neutral", "count": 4},
    {"emotion": "sadness", "count": 3}
  ],
  "users_stats": [
    {
      "user_id": "usuario_1",
      "entries_count": 8,
      "dominant_sentiment": "POS",
      "dominant_emotion": "joy"
    }
  ]
}
📝 Próximas Mejoras
Funcionalidades
Autenticación JWT

Rate limiting

Exportación de reportes PDF

Notificaciones push

Integración con más servicios de IA

Técnicas
Migraciones de base de datos con Alembic

Cache con Redis

Logging estructurado

Metrics y monitoring

Tests automatizados

🚀 Instalación y Uso
Requisitos
Python 3.8+

pip

Instalación
bash
cd backend
pip install -r requirements.txt
Ejecución
bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Variables de Entorno Opcionales
bash
export GEMINI_API_KEY=tu_api_key_aqui
export DATABASE_URL=sqlite:///./diario_prod.db