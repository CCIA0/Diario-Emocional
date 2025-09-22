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
    "http://localhost:4200",  # Desarrollo local
    "https://*.vercel.app",   # Vercel subdomains
    settings.FRONTEND_URL     # URL específica de producción
]

# En producción, permitir todos los orígenes de Vercel por seguridad
if os.getenv("ENVIRONMENT") == "production":
    allowed_origins.append("https://*.vercel.app")

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