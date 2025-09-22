import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Diario Emocional API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./diario.db")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:4200")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Configuración específica para producción
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
settings = Settings()