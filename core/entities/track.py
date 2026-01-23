# core/entities/track.py


from typing import Optional

from app.models.album import Album
from app.models.artist import Artist


from dataclasses import dataclass


@dataclass(frozen=True)
class Track:
    id: int
    counttrack: int
    title: str
    
    artist_name: str
    
    album_title: str
    album_jacket_path: Optional[str]
    
    genre: str
    duration: int
    year: int


    