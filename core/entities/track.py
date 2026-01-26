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
    file_path: str
    artist: Artist  
    album: Optional[Album]
    duration: int
    year: int


    