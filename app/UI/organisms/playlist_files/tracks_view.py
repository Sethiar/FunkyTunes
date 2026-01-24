# app/UI/organisms/tracks_view.py

from typing import List, Dict

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QListWidgetItem, QLabel, QScrollArea, QGridLayout
)
from PySide6 import QtCore
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItem, QIcon

from app.UI.organisms.explorer_grid_view import ExplorerGridView
from core.entities.track import Track


# ============================ #
#   Vue générique pour tracks  #
# ============================ #
class TracksView(QWidget):
    """
    Vue pour afficher une liste de pistes.
    """
    track_selected = Signal(Track)

    def __init__(self, tracks: List[Track] = None):
        super().__init__()
        self.tracks: List[Track] = tracks or []

        self.list_widget = QListWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Liste des pistes"))
        layout.addWidget(self.list_widget)

        self._populate()
        self.list_widget.itemClicked.connect(self._on_item_clicked)


    def _populate(self):
        self.list_widget.clear()
        for track in self.tracks:
            item = QListWidgetItem(f"{track.title} — {track.artist}")
            item.setData(256, track)
            self.list_widget.addItem(item)


    def set_tracks(self, tracks: List[Track]):
        """Met à jour la liste des tracks affichées."""
        self.tracks = tracks
        self._populate()


    def _on_item_clicked(self, item: QListWidgetItem):
        track: Track = item.data(256)
        self.track_selected.emit(track)


# ============================ #
#   Vue par Album              #
# ============================ #
class TracksByAlbumView(QWidget):
    """
    Vue pour afficher les albums en grille type "Explorer".
    Cliquer sur un album émet la liste de tracks de cet album.
    """
    
    album_selected = Signal(object)

    def __init__(self, albums: Dict[str, List[Track]], album_icons: Dict[str, str] = None, parent=None):
        """
        albums: dict[album_name -> list[Track]]
        album_icons: dict[album_name -> path_to_image]
        """
        super().__init__(parent)
        
        self.album_icons = album_icons or {}
        
        
        items = {
            album: {
                "title": album,
                "icon": album_icons.get(album, "resources/icons/album_icon.svg"),
                "payload": tracks
            }
            for album, tracks in albums.items()
        }
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Albums"))

        explorer = ExplorerGridView(items, columns=4, icon_size=60)
        explorer.item_clicked.connect(self.album_selected)

        layout.addWidget(explorer)


# ============================ #
#   Vue par Artiste            #
# ============================ #
class TracksByArtistView(QWidget):
    """
    Vue pour afficher les artistes.
    Cliquer sur un artiste émet la liste de tracks de cet artiste.
    """
    artist_selected = Signal(object)

    def __init__(self, artists: Dict[str, List[Track]], parent=None):
        super().__init__(parent)

        items = {
            artist: {
                "title": artist,
                "icon": "resources/icons/album_icon.svg",
                "payload": tracks
            }
            for artist, tracks in artists.items()
        }

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Artistes"))

        explorer = ExplorerGridView(items, columns=5, icon_size=50)
        explorer.item_clicked.connect(self.artist_selected)

        layout.addWidget(explorer)


# ============================ #
#   Vue par Genre              #
# ============================ #
class TracksByGenreView(QWidget):
    """
    Vue pour afficher les genres.
    Cliquer sur un genre émet la liste de tracks de ce genre.
    """
    genre_selected = Signal(list)

    def __init__(self, genres: Dict[str, List[Track]], parent=None):
        super().__init__(parent)

        items = {
            genre: {
                "title": genre,
                "icon": "resources/icons/genre_icon.svg",
                "tracks": tracks
            }
            for genre, tracks in genres.items()
        }

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Genres"))

        explorer = ExplorerGridView(items, columns=6, icon_size=48)
        explorer.item_clicked.connect(self.genre_selected)

        layout.addWidget(explorer)

        self._populate()
        self.list_widget.itemClicked.connect(self._on_item_clicked)


    def _populate(self):
        self.list_widget.clear()
        for genre_name, tracks in sorted(self.genres.items()):
            item = QListWidgetItem(genre_name)
            item.setData(256, tracks)
            self.list_widget.addItem(item)


    def _on_item_clicked(self, item: QListWidgetItem):
        tracks: List[Track] = item.data(256)
        self.genre_selected.emit(tracks)


# ============================ #
#   Vue Favoris                #
# ============================ #
class TracksByFavoriteView(QWidget):
    """
    Vue pour afficher uniquement les tracks favorites.
    """
    favorite_selected = Signal(list)

    def __init__(self, favorites: List[Track]):
        super().__init__()
        self.favorites = favorites

        self.list_widget = QListWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Favoris"))
        layout.addWidget(self.list_widget)

        self._populate()
        self.list_widget.itemClicked.connect(self._on_item_clicked)

    def _populate(self):
        self.list_widget.clear()
        for track in self.favorites:
            item = QListWidgetItem(f"{track.title} — {track.artist}")
            item.setData(256, track)
            self.list_widget.addItem(item)

    def _on_item_clicked(self, item: QListWidgetItem):
        track: Track = item.data(256)
        self.favorite_selected.emit([track])
        
        