# ap/UI/molecules/playlist_panel.py


from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, 
    QListWidget, QHBoxLayout
)
from PySide6.QtCore import Signal
from app.UI.atoms.buttons import AppButton



class PlaylistPanel(QWidget):
    
    request_create_playlist = Signal()
    request_delete_playlist = Signal()
    request_add_track = Signal()
    request_add_track = Signal()
    request_remove_track = Signal()
    request_select_track = Signal()
    
    
    def __init__(self):
        super().__init__()
        
        self.playlist_list = QListWidget()
        self.tracks_list = QListWidget()
        
        
        self.create_btn = AppButton("Nouvelle playlist")
        self.delete_btn = AppButton("Supprimer la playlist")
        self.add_track_btn = AppButton("Ajouter piste")
        self.remove_track_btn = AppButton("Retirer piste")
        
        self._build_ui()
        self._bind_signals()
        
        
    # =========================== #
    #    Construction de l'UI     #
    # =========================== #
    def _build_ui(self):
        layout = QVBoxLayout(self)
        
        layout.addWidget(self.playlist_list)
        layout.addWidget(self.tracks_list)
        
        btns = QHBoxLayout()
        btns.addWidget(self.create_btn)
        btns.addWidget(self.delete_btn)
        btns.addWidget(self.add_track_btn)
        btns.addWidget(self.remove_track_btn)
        
        layout.addLayout(btns)
        
        
    # =========================== #
    #    Connexion des signaux    #
    # =========================== #
    def _bind_signals(self):
        self.create_btn.clicked.connect(self.request_create_playlist.emit)
        self.delete_btn.clicked.connect(self.request_delete_playlist.emit)
        self.add_track_btn.clicked.connect(self.request_add_track.emit)
        self.remove_track_btn.clicked.connect(self.request_remove_track.emit)

        self.tracks_list.itemDoubleClicked.connect(
            lambda item: self.request_select_track.emit(item.text())
        )
        
        