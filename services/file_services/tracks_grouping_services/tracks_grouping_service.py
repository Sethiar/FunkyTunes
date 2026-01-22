# app/services/tracks_grouping_services/tracks_grouping_services.py


from typing import Dict, List
from core.entities.track import Track


class TrackGroupingService:

    @staticmethod
    def by_album(tracks: List[Track]) -> Dict[str, List[Track]]:
        albums = {}
        for t in tracks:
            albums.setdefault(t.album, []).append(t)
        return albums

    @staticmethod
    def by_artist(tracks: List[Track]) -> Dict[str, List[Track]]:
        artists = {}
        for t in tracks:
            artists.setdefault(t.artist, []).append(t)
        return artists

    @staticmethod
    def by_genre(tracks: List[Track]) -> Dict[str, List[Track]]:
        genres = {}
        for t in tracks:
            genres.setdefault(t.genre, []).append(t)
        return genres
    
    