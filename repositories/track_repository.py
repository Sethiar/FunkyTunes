# app/repositories/tack_repository.py

from typing import List, Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError
from app.models.track import Track, playlist_track_association



class TrackRepository:
    def __init__(self, db: Session):
        self.db = db


    # ========================= #
    #          CREATE           #
    # ========================= #
    def create(
        self, title: str, file_path: str,
        artist_id: int, album_id: int,
        format: Optional[str] = None,
        duration_seconds: Optional[int] = None,
        track_number: Optional[int] = None
    ) -> Optional[Track]:
        
        track = Track(
            title=title, file_path=file_path,
            artist_id=artist_id, album_id=album_id,
            format=format,
            duration_seconds=duration_seconds,
            track_number=track_number
        )
        
        try:
            self.db.add(track)
            self.db.flush()
        except IntegrityError:
            self.db.rollback()
            return None
        
        return track


    # ========================= #
    #           READ            #
    # ========================= #
    def get_by_id(self, track_id: int) -> Optional[Track]:
        return self.db.get(Track, track_id)


    def get_by_title(self, title: str) -> Optional[Track]:
        return self.db.query(Track).filter_by(title=title).first()


    def get_all(self, skip=0, limit=100):
        return (
            self.db.query(Track)
            .options(selectinload(Track.artist))
            .offset(skip)
            .limit(limit)
            .all()
        )


    def get_by_artist(self, artist_id: int, skip: int = 0, limit: int = 100) -> List[Track]:
        return self.db.query(Track).filter_by(artist_id=artist_id).offset(skip).limit(limit).all()


    def get_by_album(self, album_id: int, skip: int = 0, limit: int = 100) -> List[Track]:
        return self.db.query(Track).filter_by(album_id=album_id).order_by(Track.track_number).offset(skip).limit(limit).all()


    def get_in_playlist(self, playlist_id: int, skip: int = 0, limit: int = 100) -> List[Track]:
        return (
            self.db.query(Track)
            .join(playlist_track_association, Track.id == playlist_track_association.c.track_id)
            .filter(playlist_track_association.c.playlist_id == playlist_id)
            .order_by(Track.track_number)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    
    # ========================= #
    #         UPDATE            #
    # ========================= #
    def update(self, track_id: int, **fields) -> Optional[Track]:
        ALLOWED_FIELDS = {"title", "duration_seconds", "track_number", "format", "genre", "is_favorite"}
        track = self.get_by_id(track_id)
        
        if not track:
            return None
        
        for k, v in fields.items():
            if k not in ALLOWED_FIELDS:
                raise ValueError(f"Field '{k}' is not updatable")
            setattr(track, k, v)
        self.db.flush()
       
        return track
    
    
    # ========================= #
    #          DELETE           #
    # ========================= #
    def delete(self, track_id: int) -> bool:
        track = self.get_by_id(track_id)
        
        if not track:
            return False
        
        self.db.delete(track)
        self.db.flush()
        
        return True
    
    