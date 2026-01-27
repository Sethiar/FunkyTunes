# app/file_services/playlist_maker_services.py

from repositories.playlist_repository import PlaylistRepository
from mappers.playlist_mapper import orm_to_entity
from core.entities.playlist import Playlist as PlaylistEntity
from repositories.track_repository import TrackRepository

class PlaylistMakerServices:
    """
    Service pour la création et gestion de playlists.
    Contient toute la logique métier liée aux playlists.
    """

    def __init__(self, session_factory):
        self.session_factory = session_factory


    def create_playlist(self, name: str, user_id: int) -> PlaylistEntity:
        """
        Crée une nouvelle playlist et la persiste en DB.
        """
        session = self.session_factory()
        repo = PlaylistRepository(session)
        try:
            # Création via le repository (ORM)
            playlist_orm = repo.create(name=name, user_id=user_id)
            session.commit()
            session.refresh(playlist_orm)
            # Mapper ORM -> Entité métier
            return orm_to_entity(playlist_orm)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
            
    def get_available_tracks(self) -> list[dict]:
        session = self.session_factory()
        try:
            repo = TrackRepository(session)
            tracks = repo.get_all()

            return [
                {
                    "id": track.id,
                    "label": f"{track.artist.name} – {track.title}"
                }
                for track in tracks
            ]
        finally:
            session.close()        
            
            
    def add_track_to_playlist(self, playlist_id: int, track_id: int):
        session = self.session_factory()
        try:
           repo = PlaylistRepository(session)
           repo.add_track(playlist_id, track_id)
           session.commit()
        finally:
           session.close()

