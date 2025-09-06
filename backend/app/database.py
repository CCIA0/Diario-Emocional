from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .core.config import settings

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Solo para SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear tablas al iniciar
def create_tables():
    from .models.database_models import Base
    Base.metadata.create_all(bind=engine)