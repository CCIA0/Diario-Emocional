from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.endpoints import journal, dashboard
from .database import create_tables
import os

# Crear tablas al iniciar
create_tables()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Configurar CORS para desarrollo y producción
allowed_origins = [
    "http://localhost:4200",                    # Desarrollo local
    "https://urban-winner-blond.vercel.app",    # Nueva URL del frontend
    "https://diario-emocional-eight.vercel.app", # URL anterior (por compatibilidad)
    settings.FRONTEND_URL                       # URL específica de configuración
]

# En producción, permitir orígenes específicos
if os.getenv("ENVIRONMENT") == "production":
    allowed_origins.extend([
        "https://urban-winner-blond.vercel.app",
        "https://diario-emocional-eight.vercel.app",
        "https://*.vercel.app"
    ])

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(journal.router, prefix="/api/v1/journal", tags=["journal"])
app.include_router(dashboard.router, prefix="/api/v1", tags=["dashboard"])

@app.get("/")
async def root():
    return {"message": "Diario Emocional API funcionando!"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ai_service": "configured"
    }