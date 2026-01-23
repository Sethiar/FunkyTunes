# core/entities/playlist.py

from dataclasses import dataclass, field
from typing import List, Optional
from core.entities.track import Track


@dataclass
class Playlist:
    name: str
    tracks: List[str] = field(default_factory=list)
    current_index: Optional[int] = None  # permet de suivre la piste courante

    def add_track(self, track: Track):
        if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self, track: Track):
        if track in self.tracks:
            self.tracks.remove(track)
            # si on supprime la piste courante, on réinitialise current_index
            if self.current_index is not None and self.current_index >= len(self.tracks):
                self.current_index = len(self.tracks) - 1 if self.tracks else None

    def clear(self):
        self.tracks.clear()
        self.current_index = None

        
        
                        
    
    