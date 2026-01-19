# app/UI/molecules/menus/menu_library.py


from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Signal

from app.UI.atoms.buttons import AppButton


class MenuLibrary(QWidget):
    # ============================= #
    #            Signaux            #
    # ============================= #
    requested_all_tracks = Signal()
    requested_edit_track = Signal()
    requested_remove_track = Signal()
    requested_all_playlist = Signal()
    requested_new_playlist = Signal()
    requested_remove_playlist = Signal()

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        self._build_ui()
        self._bind_signals()

    def _build_ui(self):
        self.all_tracks_btn = AppButton("Toutes les chansons", variant="library_menu")
        self.edit_track_btn = AppButton("Modifier la chanson", variant="library_menu")
        self.remove_track_btn = AppButton("Supprimer la chanson", variant="library_menu")

        self.all_playlist_btn = AppButton("Playlists", variant="library_menu")
        self.new_playlist_btn = AppButton("Nouvelle playlist", variant="library_menu")
        self.remove_playlist_btn = AppButton("Supprimer la playlist", variant="library_menu")

        for btn in (
            self.all_tracks_btn,
            self.edit_track_btn,
            self.remove_track_btn,
            self.all_playlist_btn,
            self.new_playlist_btn,
            self.remove_playlist_btn,
        ):
            self.layout.addWidget(btn)

        self.layout.addStretch(1)

    def _bind_signals(self):
        self.all_tracks_btn.clicked.connect(self.requested_all_tracks.emit)
        self.edit_track_btn.clicked.connect(self.requested_edit_track.emit)
        self.remove_track_btn.clicked.connect(self.requested_remove_track.emit)

        self.all_playlist_btn.clicked.connect(self.requested_all_playlist.emit)
        self.new_playlist_btn.clicked.connect(self.requested_new_playlist.emit)
        self.remove_playlist_btn.clicked.connect(self.requested_remove_playlist.emit)
        
        
        