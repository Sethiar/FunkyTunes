# app/repositories/artist_repository.py

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.artist import Artist


class ArtistRepository:
    def __init__(self, db: Session):
        self.db = db

    # ========================= #
    #          CREATE           #
    # ========================= #
    def create(self, name: str) -> Artist:
        artist = Artist(name=name)
        
        try:
            self.db.add(artist)
            self.db.flush()
        except IntegrityError:
            self.db.rollback()
            artist = self.db.query(Artist).filter_by(name=name).first()
        
        return artist


    # ========================= #
    #           READ            #
    # ========================= #
    def get_by_id(self, artist_id: int) -> Optional[Artist]:
        return self.db.get(Artist, artist_id)


    def get_by_name(self, name: str) -> Optional[Artist]:
        return self.db.query(Artist).filter_by(name=name).first()


    def get_all(self, skip: int = 0, limit: int = 100) -> List[Artist]:
        return self.db.query(Artist).order_by(Artist.name).offset(skip).limit(limit).all()
    
    
    # ========================= #
    #         UPDATE            #
    # ========================= #
    def update(self, artist_id: int, new_name: str) -> Optional[Artist]:
        artist = self.get_by_id(artist_id)
        if not artist:
            return None
        
        artist.name = new_name
        self.db.flush()
        
        return artist
    
      
    # ========================= #
    #          DELETE           #
    # ========================= #
    def delete(self, artist_id: int) -> bool:
        artist = self.get_by_id(artist_id)
        if not artist:
            return False
        
        self.db.delete(artist)
        self.db.flush()
        
        return True
    
    
    # ========================= #
    #        Additional         #
    # ========================= #
    def count(self) -> int:
        return self.db.query(Artist).count()