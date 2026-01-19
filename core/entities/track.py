# core/entities/track.py

from dataclasses import dataclass


@dataclass(frozen=True)
class Track:
    counttrack: int
    title: str
    artist: str
    album: str
    duration: int
    year: int
    