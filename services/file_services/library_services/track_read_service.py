# app/fiel_service/library_services/track_read_service.py

from typing import List

from sqlalchemy.orm import Session, joinedload

from core.entities.track import Track as TrackDataClass
from app.models.track import Track as TrackORM

from core.logger import logger


class TrackReadService():
    """
    Service de lecture des tracks depuis la BDD.
    """
    
    def __init__(self, session: Session):
        self.db = session
    
    def get_tracks(self) -> List[TrackDataClass]:
        """
        Retourne toutes les pistes sous forme de dataclasses pour affichage UI.

        Args:
            session (Session): session SQLAlchemy active

        Returns:
            List[TrackDataClass]: liste des pistes avec titre, artiste, album, durée, année
        """
        orm_tracks = (
            self.db.query(TrackORM)
            .options(joinedload(TrackORM.artist), joinedload(TrackORM.album))
            .order_by(TrackORM.album_id, TrackORM.track_number)
            .all()
        )

        tracks = [
            TrackDataClass(
                id=t.id,
                counttrack=i,
                title=t.title,
                file_path=t.file_path,
                artist=t.artist.name,
                album=t.album,
                duration=t.duration_seconds or 0,
                year=getattr(t.album, "year", "Indisponible")
            )
            for i, t in enumerate(orm_tracks, start=1)
        ]

        logger.info(f"LibraryServices : {len(tracks)} tracks chargées depuis la BDD")
        return tracks
    
    
    def get_track_file_paths(self) -> list[str]:
        """
        Retourne la liste des chemins complets pour le PlayerServices.

        Args:
            session (Session): session SQLAlchemy active

        Returns:
            list[str]: chemins des fichiers audio
        """
        orm_tracks = self.db.query(TrackORM).order_by(TrackORM.album_id, TrackORM.track_number).all()
        paths = [t.file_path for t in orm_tracks]

        logger.info(f"LibraryServices : {len(paths)} tracks pour le PlayerServices")
        return paths
    
    