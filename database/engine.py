# database/engine.py

"""
Configuration et initialisation du moteur de base de données pour l'application FunkyTunes.
"""
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'funkytunes.db'}"


engine = create_engine(
    DATABASE_URL, 
    echo=True,
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

def get_session():
    """
    Retourne une nouvelle session SQLAlchemy.
    
    Utiliser avec un contexte `with` est conseillé pour le commit/rollback automatique.
    """
    return SessionLocal()

