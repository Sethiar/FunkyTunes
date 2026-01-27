# app/controller/player_service_controller.py

from enum import Enum
from typing import Optional

from PySide6.QtCore import QObject

from app.UI.molecules.player_controls import PlayerControls
from services.file_services.player_services.player_services import PlayerServices
from services.file_services.playlist_services.playlist_services import PlaylistServices

from core.logger import logger


class PlaybackState(Enum):
    PLAYING = "playing"
    PAUSED = "paused"
    STOPPED = "stopped"


class PlayerServiceController(QObject):
    """
    Controller minimal reliant PlayerControls aux services Player et Playlist.
    Délègue toute logique métier aux services.
    """
    
    def __init__(
        self, 
        controls: PlayerControls, 
        player_service: PlayerServices,
        playlist_service: PlaylistServices, 
        parent=None
    ):
        """
        Initialise le controller.

        Args:
            controls (PlayerControls) : UI du lecteur
            player_service (PlayerServices) : service audio
            playlist_service (PlaylistServices) : service gestion playlist
        """
        
        super().__init__(parent)
        self.controls = controls
        self.player = player_service
        self.playlist = playlist_service
       
        # Connecte UI → controller → services
        self._bind_ui()
        # Connecte services → controller → UI
        self._bind_services()

        logger.info("PlayerServiceController initialisé")
        
        
    # ========================= #
    #      UI → services        #
    # ========================= #
    def _bind_ui(self):
        """Connecte les signaux UI aux actions du player et de la playlist."""
        self.controls.request_play.connect(self._on_play)
        self.controls.request_pause.connect(self.player.handle_pause)
        self.controls.request_stop.connect(self.player.handle_stop)

        self.controls.request_next.connect(self._on_next)
        self.controls.request_previous.connect(self._on_previous)

        self.controls.request_volume_up.connect(self.player.handle_volume_up)
        self.controls.request_volume_down.connect(self.player.handle_volume_down)
        self.controls.request_volume_mute.connect(self.player.handle_volume_mute)
        
        
    # ========================= #
    #      Services → UI        #
    # ========================= #
    def _bind_services(self) -> None:
        """Connecte les signaux des services aux slots du controller."""
        self.playlist.track_changed.connect(self._on_track_changed)
        self.player.playback_state_changed.connect(self._on_playback_state_changed)
        self.player.volume_changed.connect(self._on_volume_changed)   
        
    
    # ========================= #
    # Actions utilisateur       #
    # ========================= #
    def _on_play(self):
        """Lit la piste courante dans la playlist."""
        track = self.playlist.current_track
        if track:
            self.player.handle_play(track)
        else:
            logger.warning("Aucune piste à lire")
        
    # Navigation dans la playlist
    def _on_next(self):
        """Passe à la piste suivante et la joue."""
        track = self.playlist.get_next_track()
        if track:
            self.player.handle_play(track)
        else:
            logger.info("Fin de playlist")
            
    def _on_previous(self):
        """Retourne à la piste précédente et la joue."""
        track = self.playlist.get_previous_track()
        if track:
            self.player.handle_play(track)
        else:
            logger.info("Début de playlist")
    
    
    # ========================= #
    # Services → UI slots        #
    # ========================= #
    def _on_track_changed(self, track_path: str):
        """Slot appelé quand la piste change dans PlaylistServices."""
        self._update_track(track_path)

    def _on_playback_state_changed(self, state: str):
        """Slot appelé quand l'état change dans PlayerServices."""
        self._update_state(state)

    def _on_volume_changed(self, volume: float):
        """Slot appelé quand le volume change dans PlayerServices."""
        self._update_volume(volume)
    
    
    # ========================= #
    #   Mise à jour UI centralisée
    # ========================= #
    def _update_track(self, track_path: str):
        self.controls.set_track(self.playlist.current_track)

    def _update_state(self, state: str):
        self.controls.set_state(PlaybackState(state))

    def _update_volume(self, volume: float):
        self.controls.set_volume(volume)
            
                 