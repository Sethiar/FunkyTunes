# app/controllers/playlist_controllers/playlist_maker_controller.p

from typing import Callable

from PySide6.QtWidgets import QLabel

from app.UI.screens.window_services.create_playlist_screen import CreateplaylistForm

from PySide6.QtCore import QObject 

class PlaylistMakerController(QObject):
    """
    Controller pour lé création de playlist.
    """
    
    def __init__(
        self, 
        ui: CreateplaylistForm,
        session_factory: Callable):
        super().__init__(parent)
        
        se
    
