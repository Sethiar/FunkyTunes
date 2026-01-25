# database/init_db.py

"""
Initialisation de la base de données pour l'application FunkyTunes.
"""

from sqlalchemy.orm import sessionmaker
from database.engine import engine
from database.base import Base


# Importation des modèles pour créer les tables
from app.models.artist import Artist
from app.models.album import Album
from app.models.track import Track
from app.models.user import User
from app.models.playlist import Playlist


def init_db():
    """
    Initialise la base de données en créant toutes les tables définies dans les modèles.
    """
    Base.metadata.create_all(bind=engine)
  

    
    
