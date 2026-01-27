# core/entities/playlist.py

from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class Playlist:
    """
    Entité métier représentant une playlist de lecture.
    Indépendante de la base de données et de l'UI.
    """
    name: str
    id: Optional[int] = None 
    track_ids: List[int] = field(default_factory=list)
    tracks_path: List[str] = field(default_factory=list)
    current_index: int = 0
    user_id: Optional[int] = None
    
    