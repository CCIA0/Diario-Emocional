diario_emocional_mvp/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # App principal FastAPI
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── endpoints/
│   │   │       ├── __init__.py
│   │   │       ├── journal.py      # Endpoints del diario
│   │   │       └── dashboard.py    # Endpoints del dashboard
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py           # Configuración
│   │   │   └── security.py         # Auth (básico para MVP)
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py          # Pydantic models
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ai_service.py       # PySentimiento & Gemini
│   │   │   └── database.py         # Manejo de DB
│   │   └── database.py             # Config de DB
│   ├── requirements.txt
│   └── README.md
│