# app/models/artist.py

from typing import List, Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import IntegrityError
from database.base import Base
from app.models.album import Album
from app.models.track import Track

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    albums = relationship("Album", back_populates="artist", cascade="all, delete-orphan")
    tracks = relationship("Track", back_populates="artist", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Artist(name='{self.name}')>"

    # ================= Create =================
    @classmethod
    def create(cls, db: Session, name: str):
        
        artist = cls(name=name)
        
        try:
            db.add(artist)
            db.flush()
        except IntegrityError:
            db.rollback()
            artist = db.query(cls).filter_by(name=name).first()

        return artist


    # ================= Read =================
    @classmethod
    def get_by_id(cls, db: Session, artist_id: int):
        return db.get(cls, artist_id)


    @classmethod
    def get_by_name(cls, db: Session, name: str):

        return db.query(cls).filter_by(name=name).first()


    @classmethod
    def get_all(cls, db: Session, skip: int = 0, limit: int = 100) -> List["Artist"]:

        return (
            db.query(cls)
            .order_by(cls.name)
            .offset(skip)
            .limit(limit)
            .all()
        )


    # ================= Update =================
    @classmethod
    def update(cls, db: Session, artist_id: int, new_name: str):
        artist = db.get(cls, artist_id)
        
        if not artist:
            return None
        
        artist.name = new_name
        db.flush()
        return artist
    
    
    # ================= Delete =================
    @classmethod
    def delete(cls, db: Session, artist_id: int) -> bool:
        artist = db.get(cls, artist_id)
        if not artist:
            return False
        
        db.delete(artist)
        db.flush()
        return True

    # ================= Additional =================
    @classmethod
    def count(cls, db: Session) -> int:
        
        return db.query(cls).count()
    
