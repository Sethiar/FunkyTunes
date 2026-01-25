# app/repositories/album_repository


from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.album import Album
from app.models.track import Track


class AlbumRepository:
    def __init__(self, db: Session):
        self.db = db
        
        
    # ========================= #
    #          CREATE           #
    # ========================= #
    def create(self, title: str, artist_id: int, release_year: Optional[int] = None, jacket_path: Optional[str] = None) -> Album:
        album = Album(title=title, artist_id=artist_id, release_year=release_year, jacket_path=jacket_path)
        
        try:
            self.db.add(album)
            self.db.flush()
        except IntegrityError:
            self.db.rollback()
            album = self.db.query(Album).filter_by(title=title, artist_id=artist_id).first()
        
        return album     
    
    
    # ========================= #
    #           READ            #
    # ========================= #
    def get_by_id(self, album_id: int) -> Optional[Album]:
        return self.db.get(Album, album_id)


    def get_by_title_and_artist(self, title: str, artist_id: int) -> Optional[Album]:
        return self.db.query(Album).filter_by(title=title, artist_id=artist_id).first()


    def get_all(self, skip: int = 0, limit: int = 100) -> List[Album]:
        return self.db.query(Album).order_by(Album.title).offset(skip).limit(limit).all()


    def get_by_artist(self, artist_id: int, skip: int = 0, limit: int = 100) -> List[Album]:
        return self.db.query(Album).filter_by(artist_id=artist_id).order_by(Album.title).offset(skip).limit(limit).all()

    
    # ========================= #
    #         UPDATE            #
    # ========================= #
    def update(self, album_id: int, **kwargs) -> Optional[Album]:
        album = self.get_by_id(album_id)
        if not album:
            return None
       
        for k, v in kwargs.items():
            setattr(album, k, v)
        self.db.flush()
        
        return album
    
    
    # ========================= #
    #          DELETE           #
    # ========================= #
    def delete(self, album_id: int) -> bool:
        album = self.get_by_id(album_id)
        if not album:
            return False
        
        self.db.delete(album)
        self.db.flush()
       
        return True
 
    
    # ========================= #
    #    Get tracks by album    #
    # ========================= #
    def get_tracks(self, album_id: int, skip: int = 0, limit: int = 100) -> List[Track]:
        return self.db.query(Track).filter_by(album_id=album_id).order_by(Track.track_number).offset(skip).limit(limit).all()   
    
    