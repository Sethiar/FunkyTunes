# app/repositories/playlist_repository.py


from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.playlist import Playlist, playlist_track_association
from app.models.track import Track


class PlaylistRepository:
    def __init__(self, db: Session):
        self.db = db


    # ========================= #
    #          CREATE           #
    # ========================= #
    def create(self, name: str, description: Optional[str] = None) -> Playlist:
        playlist = Playlist(name=name, description=description)
        try:
            self.db.add(playlist)
            self.db.flush()
        except IntegrityError:
            self.db.rollback()
            playlist = self.db.query(Playlist).filter_by(name=name).first()
        
        return playlist


    # ========================= #
    #           READ            #
    # ========================= #
    def get_by_id(self, playlist_id: int) -> Optional[Playlist]:
        return self.db.get(Playlist, playlist_id)


    def get_by_name(self, name: str) -> Optional[Playlist]:
        return self.db.query(Playlist).filter_by(name=name).first()


    def get_all(self, skip: int = 0, limit: int = 100) -> List[Playlist]:
        return self.db.query(Playlist).order_by(Playlist.name).offset(skip).limit(limit).all()
    
    
    # ========================= #
    #         UPDATE            #
    # ========================= #
    def update(self, playlist_id: int, new_name: Optional[str] = None, new_description: Optional[str] = None) -> Optional[Playlist]:
        playlist = self.get_by_id(playlist_id)
        if not playlist:
            return None
        
        if new_name:
            playlist.name = new_name
        
        if new_description is not None:
            playlist.description = new_description
        self.db.flush()
       
        return playlist
    
    
    # ========================= #
    #          DELETE           #
    # ========================= #
    def delete(self, playlist_id: int) -> bool:
        playlist = self.get_by_id(playlist_id)
        if not playlist:
            return False
        
        self.db.delete(playlist)
        self.db.flush()
        
        return True
    
    
    # ========================= #
    #          ADDITIONAL       #
    # ========================= #
    
    # Add Tracks/ Remove Tracks
    def add_track(self, playlist_id: int, track_id: int) -> Optional[Playlist]:
        playlist = self.get_by_id(playlist_id)
        track = self.db.get(Track, track_id)
        if not playlist or not track:
            return None
        if track in playlist.tracks:
            raise Exception(f"Track '{track.title}' already in playlist '{playlist.name}'")
        playlist.tracks.append(track)
        self.db.flush()
        return playlist


    # Remove Tracks
    def remove_track(self, playlist_id: int, track_id: int) -> Optional[Playlist]:
        playlist = self.get_by_id(playlist_id)
        track = self.db.get(Track, track_id)
        if not playlist or not track:
            return None
        if track in playlist.tracks:
            playlist.tracks.remove(track)
        self.db.flush()
        return playlist


    # Get Tracks
    def get_tracks(self, playlist_id: int, skip: int = 0, limit: int = 100) -> List[Track]:
        return (
            self.db.query(Track)
            .join(playlist_track_association, Track.id == playlist_track_association.c.track_id)
            .filter(playlist_track_association.c.playlist_id == playlist_id)
            .order_by(Track.track_number)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        