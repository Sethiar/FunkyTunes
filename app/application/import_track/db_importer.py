# services/file_services/library_services/db_importer.py

from sqlalchemy.orm import Session
from repositories.artist_repository import ArtistRepository
from repositories.album_repository import AlbumRepository
from repositories.track_repository import TrackRepository

from core.logger import logger


class DBImporter:
    """
    Classe pour insérer les entités Artist, Album et Track dans la base de données.

    Rôle :
        - Vérifie si l'artiste/album existe déjà.
        - Crée de nouvelles entrées si nécessaire.
        - Assure la persistance des tracks avec commit sécurisé.
    """
    def __init__(self, db_session: Session):
        """
        Initialise l'importeur DB.

        Args:
            db_session: Session SQLAlchemy
        """
        self.db = db_session

    def import_track(self, metadata: dict):
        """
        Crée ou récupère les entités Artist/Album/Track dans la base de données.

        Args:
            metadata: Dictionnaire contenant les informations d'un track

        Raises:
            Exception: si l'insertion échoue
        """
        try:
            # Gestion de l'artiste
            artist_repo = ArtistRepository(self.db)
            artist = artist_repo.create(name=metadata["artist"])
            logger.debug(f"DBImporter : Artiste traité: {artist.name} (ID {artist.id})")

            # Gestion de l'album
            album_repo = AlbumRepository(self.db)
            album = album_repo.create(
                title=metadata["album"],
                artist_id=artist.id,
                release_year=metadata.get("year")
            )
            logger.debug(f"DBImporter : Album traité: {album.title} (ID {album.id})")

            # Création du track
            track_repo = TrackRepository(self.db)
            track = track_repo.create(
                title=metadata["title"],
                file_path=metadata["file_path"],
                artist_id=artist.id,
                album_id=album.id,
                format=metadata["format"],
                duration_seconds=metadata["duration"],
                track_number=metadata["track_number"]
            )
            logger.info(f"DBImporter : Track importé: {track.title}")

            # Commit après chaque track pour éviter la perte en cas d'erreur
            self.db.commit()

        except Exception as e:
            logger.exception(f"Erreur lors de l'import du track {metadata.get('title')}")
            self.db.rollback()
            raise
        
        