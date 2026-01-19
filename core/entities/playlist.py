# core/entities/playlist.py

from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class Playlist:
    name: str
    tracks: List[str] = field(default_factory=list)
    current_index: Optional[int] = None
    
    