# app/UI/molecules/menus/menu_playlist.py

from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Signal
from app.UI.atoms.buttons import AppButton


class PlaylistMenu(QWidget):
    """
    Création du menu de l'écran des playlists.
    """
    
    # ============================ #
    #        Signalisation         #
    # ============================ #          
    request_create_playlist = Signal()
    request_delete_playlist = Signal()
    request_add_track = Signal()
    request_remove_track = Signal()
    
    
    def __init__(self):
        super().__init__()
        self.menu_playlist = QHBoxLayout(self)
        self.menu_playlist.setSpacing(15)
        
        self._build_ui()
        self._bind_signals()
        
    
    # =========================== #
    #    Construction de l'UI     #
    # =========================== #
    def _build_ui(self):
        self.create_btn = AppButton("Nouvelle playlist")
        self.delete_btn = AppButton("Supprimer la playlist")
        self.add_track_btn = AppButton("Ajouter piste")
        self.remove_track_btn = AppButton("Retirer piste")
    
        for btn in (
            self.create_btn,
            self.delete_btn, 
            self.add_track_btn, 
            self.remove_track_btn,
        ):
            self.menu_playlist.addWidget(btn)
 
 
    # =========================== #
    #    Connexion des signaux    #
    # =========================== #
    def _bind_signals(self):
        self.create_btn.clicked.connect(self.request_create_playlist.emit)
        self.delete_btn.clicked.connect(self.request_delete_playlist.emit)
        self.add_track_btn.clicked.connect(self.request_add_track.emit)
        self.remove_track_btn.clicked.connect(self.request_remove_track.emit)

        
            