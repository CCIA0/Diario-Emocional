from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .core.config import settings
import os

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Configuración específica para SQLite en producción
connect_args = {}
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    connect_args = {"check_same_thread": False}
    
    # En producción (Render), asegurar que el directorio existe
    if settings.is_production:
        db_dir = os.path.dirname("./diario.db")
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args=connect_args,
    pool_pre_ping=True,  # Verificar conexiones antes de usar
    echo=not settings.is_production  # Solo log SQL en desarrollo
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
    try:
        from .models.database_models import Base
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas de base de datos creadas exitosamente")
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        raise