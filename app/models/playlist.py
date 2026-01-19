# app/models/playlist.py


"""
Modèle de données pour une playlist musicale dans l'application FunkyTunes.
"""

from typing import List, Optional
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import IntegrityError
from database.base import Base


# Table d'association many-to-many Playlist <-> Track
playlist_track_association = Table(
    'playlist_track_association',
    Base.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.id')),
    Column('track_id', Integer, ForeignKey('tracks.id'))
)


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    tracks = relationship(
        "Track",
        secondary=playlist_track_association,
        back_populates="playlists"
    )

    def __repr__(self):
        return f"<Playlist(name='{self.name}', description='{self.description}')>"

    # ================= Create =================
    @classmethod
    def create(cls, db: Session, name: str, description: Optional[str] = None):

        playlist = cls(name=name, description=description)
        try:
            db.add(playlist)
            db.flush()
        except IntegrityError:
            db.rollback()
            playlist = db.query(cls).filter_by(name=name).first()

        return playlist

    # ================= Read =================
    @classmethod
    def get_by_id(cls, db: Session, playlist_id: int):
        
        return db.get(cls, playlist_id)
    

    @classmethod
    def get_by_name(cls, db: Session, name: str):
        return db.query(cls).filter_by(name=name).first()


    @classmethod
    def get_all(cls, db: Session, skip: int = 0, limit: int = 100) -> List["Playlist"]:

        return db.query(cls).order_by(cls.name).offset(skip).limit(limit).all()


    # ================= Update =================
    @classmethod
    def update(cls, db: Session, playlist_id: int, new_name: Optional[str] = None, new_description: Optional[str] = None):

        playlist = db.get(cls, playlist_id)
        if not playlist:
            return None
        
        if new_name:
            playlist.name = new_name
            
        if new_description is not None:
            playlist.description = new_description
        db.flush()
        
        return playlist

    # ================= Delete =================
    @classmethod
    def delete(cls, db: Session, playlist_id: int) -> bool:
        playlist = db.get(cls, playlist_id)
        if not playlist:
            return False
        
        db.delete(playlist)
        db.flush()
        
        return True

    # ================= Add / Remove Tracks =================
    @classmethod
    def add_track(cls, db: Session, playlist_id: int, track_id: int):
        from app.models.track import Track
        playlist = db.get(cls, playlist_id)
        if not playlist:
            return None
        
        track = db.get(Track, track_id)
        if not track:
            return None
        
        if track in playlist.tracks:
            raise Exception(f"Track '{track.title}' already in playlist '{playlist.name}'")
        playlist.tracks.append(track)
        
        try:
            db.flush()
        except Exception:
            db.rollback()
            raise
        return playlist

    @classmethod
    def remove_track(cls, db: Session, playlist_id: int, track_id: int):
        from app.models.track import Track
        playlist = db.get(cls, playlist_id)
        if not playlist:
            return None
        
        track = db.get(Track, track_id)
        if track in playlist.tracks:
            playlist.tracks.remove(track)
        try:
            db.flush()
        except Exception:
            db.rollback()
            raise
        
        return playlist

    # ================= Get Tracks =================
    @classmethod
    def get_tracks(cls, db: Session, playlist_id: int, skip: int = 0, limit: int = 100):
        from app.models.track import Track

        return (
            db.query(Track)
            .join(playlist_track_association, Track.id == playlist_track_association.c.track_id)
            .filter(playlist_track_association.c.playlist_id == playlist_id)
            .order_by(Track.track_number)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    
    