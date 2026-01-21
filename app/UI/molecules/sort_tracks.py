# app/UI/molecules/sort_tracks.py

"""
Composant pour trier les pistes dans l'interface utilisateur.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Signal

from app.UI.atoms.buttons import AppButton


class SortTracks(QWidget):
    """
    Composant pour trier les pistes par différents critères.
    """
    # =========================== #
    #           Signaux           #
    # =========================== #
    sort_by_artist = Signal()
    sort_by_album = Signal()
    sort_by_genre = Signal()
    sort_favorites = Signal()
    
    def __init__(self):
        super().__init__()
        
        self.sort_tracks_layout = QHBoxLayout()
        self.sort_tracks_layout.setSpacing(10)
        
        self.btn_artist = AppButton("Artiste", variant="sort_menu")
        self.btn_album = AppButton("Album", variant="sort_menu")
        self.btn_genre = AppButton("Genre", variant="sort_menu")
        self.btn_favorites = AppButton("Favoris", variant="sort_menu")

        self.sort_tracks_layout.addWidget(self.btn_artist)
        self.sort_tracks_layout.addWidget(self.btn_album)
        self.sort_tracks_layout.addWidget(self.btn_genre)
        self.sort_tracks_layout.addWidget(self.btn_favorites)

        self.sort_tracks_layout.addStretch(1)
        self.setLayout(self.sort_tracks_layout)

        self._connect_signals()

    def _connect_signals(self):
        self.btn_artist.clicked.connect(self.sort_by_artist.emit)
        self.btn_album.clicked.connect(self.sort_by_album.emit)
        self.btn_genre.clicked.connect(self.sort_by_genre.emit)
        self.btn_favorites.clicked.connect(self.sort_favorites.emit)
        
        
    # Slots de debug
    def _on_artist_clicked(self):
        print("[SortTracks] Artist clicked")
        self.sort_by_artist.emit()

    def _on_album_clicked(self):
        print("[SortTracks] Album clicked")
        self.sort_by_album.emit()

    def _on_genre_clicked(self):
        print("[SortTracks] Genre clicked")
        self.sort_by_genre.emit()

    def _on_favorites_clicked(self):
        print("[SortTracks] Favorites clicked")
        self.sort_favorites.emit()
                
        