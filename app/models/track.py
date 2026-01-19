# app/models/track.py

"""
Modèle de données pour une piste musicale dans l'application FunkyTunes.
"""

from typing import Optional, List
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import IntegrityError
from database.base import Base

from app.models.playlist import playlist_track_association

class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    duration_seconds = Column(Integer, nullable=True)
    file_path = Column(String, unique=True, nullable=False)
    format = Column(String, nullable=True)
    track_number = Column(Integer, nullable=True)
    
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)    
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)
    
    artist = relationship("Artist", back_populates="tracks")
    album = relationship("Album", back_populates="tracks")
    playlists = relationship(
        "Playlist",
        secondary=playlist_track_association,
        back_populates="tracks"
    )
    
    # Unicité du numéro de piste par album
    __table_args__ = (UniqueConstraint("album_id", "track_number", name="uix_album_track_number"),)

    def __repr__(self):
        return f"<Track(title='{self.title}', duration_seconds={self.duration_seconds}, format='{self.format}', track_number={self.track_number})>"

    # ================= Create =================
    @classmethod
    def create(cls, db: Session, title: str, file_path: str, artist_id: int, album_id: int,
               format: Optional[str] = None, duration_seconds: Optional[int] = None,
               track_number: Optional[int] = None):
        
        track = cls(
            title=title, file_path=file_path, artist_id=artist_id, album_id=album_id,
            format=format, duration_seconds=duration_seconds, track_number=track_number
        )
        try:
            db.add(track)
            db.flush()
        except IntegrityError as e:
            db.rollback()
            return None
        return track

    # ================= Read =================
    @classmethod
    def get_by_id(cls, db: Session, track_id: int):
        
        track = db.get(cls, track_id)
        
        return track

    @classmethod
    def get_by_title(cls, db: Session, title: str):
        track = db.query(cls).filter_by(title=title).first()
        
        return track

    @classmethod
    def get_all(cls, db: Session, skip: int = 0, limit: int = 100) -> List["Track"]:
        
        tracks = db.query(cls).offset(skip).limit(limit).all()
        
        return tracks

    @classmethod
    def get_by_artist(cls, db: Session, artist_id: int, skip: int = 0, limit: int = 100) -> List["Track"]:

        tracks = db.query(cls).filter_by(artist_id=artist_id).offset(skip).limit(limit).all()

        return tracks

    @classmethod
    def get_by_album(cls, db: Session, album_id: int, skip: int = 0, limit: int = 100) -> List["Track"]:

        tracks = db.query(cls).filter_by(album_id=album_id).order_by(cls.track_number).offset(skip).limit(limit).all()

        return tracks

    @classmethod
    def get_in_playlist(cls, db: Session, playlist_id: int, skip: int = 0, limit: int = 100) -> List["Track"]:

        tracks = (
            db.query(cls)
            .join(playlist_track_association, cls.id == playlist_track_association.c.track_id)
            .filter(playlist_track_association.c.playlist_id == playlist_id)
            .order_by(cls.track_number)
            .offset(skip).limit(limit)
            .all()
        )
        
        return tracks

    # ================= Update =================
    @classmethod
    def update(cls, db: Session, track_id: int, **fields):
        ALLOWED_FIELDS = {"title", "duration_seconds", "track_number", "format"}

        track = db.get(cls, track_id)
        if not track:
            return None
        
        for k, v in fields.items():
            if k not in ALLOWED_FIELDS:
                raise ValueError(f"Field '{k}' is not updatable")
            setattr(track, k, v)

        db.flush()
        
        return track

    # ================= Delete =================
    @classmethod
    def delete(cls, db: Session, track_id: int) -> bool:
        
        track = db.get(cls, track_id)
        if not track:
            return False
        
        db.delete(track)
        db.flush()
        
        return True
    
    