# Esto asegura que el modelo esté disponible para Alembic y otras partes
from .database_models import Base, JournalEntry

__all__ = ["Base", "JournalEntry"]