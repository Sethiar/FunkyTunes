# app/models/album.py

from typing import List, Optional
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import IntegrityError

from database.base import Base
from app.models.track import Track

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    release_year = Column(String, nullable=True)
    jacket_path = Column(String, nullable=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)

    artist = relationship("Artist", back_populates="albums")
    tracks = relationship("Track", back_populates="album", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("title", "artist_id", name="uix_album_artist"),)

    def __repr__(self):
        return f"<Album(title='{self.title}', release_year={self.release_year})>"

    # ================= Create =================
    @classmethod
    def create(cls, db: Session, title: str, artist_id: int, release_year: Optional[str] = None, jacket_path: Optional[str] = None):
        
        album = cls(title=title, artist_id=artist_id, release_year=release_year, jacket_path=jacket_path)
        try:
            db.add(album)
            db.flush()
        except IntegrityError:
            db.rollback()
            return (
                db.query(cls)
                .filter_by(title=title, artist_id=artist_id)
                .first()
            )

        return album

    # ================= Read =================
    @classmethod
    def get_by_id(cls, db: Session, album_id: int):
        
        album = db.get(cls, album_id)

        return album

    @classmethod
    def get_by_title_and_artist(cls, db: Session, title: str, artist_id: int):
        
        album = db.query(cls).filter_by(title=title, artist_id=artist_id).first()

        return album

    @classmethod
    def get_all(cls, db: Session, skip: int = 0, limit: int = 100) -> List["Album"]:
        
        albums = db.query(cls).order_by(cls.title).offset(skip).limit(limit).all()

        return albums

    @classmethod
    def get_by_artist(cls, db: Session, artist_id: int, skip: int = 0, limit: int = 100) -> List["Album"]:

        albums = db.query(cls).filter_by(artist_id=artist_id)\
                   .order_by(cls.title).offset(skip).limit(limit).all()
        
        return albums

    # ================= Update =================
    @classmethod
    def update(cls, db: Session, album_id: int, **kwargs):
        
        album = db.get(cls, album_id)
        if not album:
            return None
        
        for k, v in kwargs.items():
            setattr(album, k, v)
        
        db.flush()
        return album

    # ================= Delete =================
    @classmethod
    def delete(cls, db: Session, album_id: int) -> bool:

        album = db.get(cls, album_id)
        if not album:
            return False
        
        db.delete(album)
        db.flush()
        
        return True

    # ================= Get tracks by album =================
    @classmethod
    def get_tracks(cls, db: Session, album_id: int, skip: int = 0, limit: int = 100) -> List[Track]:

        tracks = db.query(Track).filter_by(album_id=album_id)\
                   .order_by(Track.track_number).offset(skip).limit(limit).all()

        return tracks
