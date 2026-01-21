# app/controllers/tracks_sort_controller.py

from PySide6.QtCore import QObject
from typing import List, Dict

from services.file_services.library_services.library_services import LibraryServices
from app.UI.organisms.playlist_files.tracks_view import (
    TracksView,
    TracksByAlbumView,
    TracksByArtistView,
    TracksByGenreView,
    TracksByFavoriteView
)
from app.UI.screens.window_services.playlist_panel import PlaylistPanel

from core.entities.track import Track
from core.logger import logger


class TracksBySortController(QObject):
    """
    Controller général pour l'exploration et le tri des tracks.
    S'occupe de récupérer les données via LibraryServices et
    de créer les vues correspondantes.
    """
    
    def __init__(self, ui: PlaylistPanel, library_service: LibraryServices):
        super().__init__()
        self.ui = ui
        self.library_service = library_service
    
    
    # =========================== #
    #   Affichage bibliothèque    #
    # =========================== #
    def show_library(self):
        tracks: List[Track] = self.library_service.get_tracks()
        tracks_view = TracksView(tracks)
        tracks_view.track_selected.connect(self.ui.display_tracks)
        self.ui.replace_main_view(tracks_view)
    
    
    # =========================== #
    #    Affichage par album      #
    # =========================== #
    def show_by_album(self):
        tracks: List[Track] = self.library_service.get_tracks()
        albums: Dict[str, List[Track]] = {}
        for t in tracks:
            albums.setdefault(t.album, []).append(t)

        album_view = TracksByAlbumView(albums)
        album_view.album_selected.connect(self.ui.display_tracks)
        self.ui.replace_main_view(album_view)
        
        
    # =========================== #
    #  Affichage par artistes     #
    # =========================== #
    def show_by_artist(self):
        tracks: List[Track] = self.library_service.get_tracks()
        artists: Dict[str, List[Track]] = {}
        for t in tracks:
            artists.setdefault(t.artist, []).append(t)

        artist_view = TracksByArtistView(artists)
        artist_view.artist_selected.connect(self.ui.display_tracks)
        self.ui.replace_main_view(artist_view)
        
        
        
    # =========================== #
    #    Affichage par genre      #
    # =========================== #
    def show_by_genre(self):
        tracks: List[Track] = self.library_service.get_tracks()
        genres: Dict[str, List[Track]] = {}
        for t in tracks:
            genres.setdefault(t.genre, []).append(t)

        genre_view = TracksByGenreView(genres)
        genre_view.genre_selected.connect(self.ui.display_tracks)
        self.ui.replace_main_view(genre_view)
    
    
    # =========================== #
    #      Affichage favoris      #
    # =========================== #
    def show_favorites(self):
        tracks: List[Track] = self.library_service.get_tracks()
        favorites: List[Track] = [t for t in tracks if t.is_favorite]

        favorite_view = TracksByFavoriteView(favorites)
        favorite_view.favorite_selected.connect(self.ui.display_tracks)
        self.ui.replace_main_view(favorite_view)
        
        