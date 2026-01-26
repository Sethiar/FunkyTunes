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
    Controller reliant l'UI PlayerControls aux services Player et Playlist.

    Responsabilités :
    - Relier actions UI → services audio/playlist
    - Mettre à jour l'UI en fonction des événements services
    """
    
    def __init__(
        self, 
        controls: PlayerControls, 
        player_service: PlayerServices,
        playlist_service: PlaylistServices
    ) -> None:
        """
        Initialise le controller.

        Args:
            controls (PlayerControls) : UI du lecteur
            player_service (PlayerServices) : service audio
            playlist_service (PlaylistServices) : service gestion playlist
        """
        
        super().__init__()
        self.controls = controls
        self.player = player_service
        self.playlist = playlist_service
       
        # Binding UI ↔ Controller
        self._bind_ui_to_controller()
        
        # Binding Services ↔ Controller
        self._bind_services_to_controller()

        logger.info("PlayerServiceController initialisé")
        
        
    # ========================= #
    #      UI → Controller      #
    # ========================= #
    def _bind_ui_to_controller(self):
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
    # Services → Controller     #
    # ========================= #
    def _bind_services_to_controller(self) -> None:
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
        if not track:
            logger.warning("Aucune piste à lire")
            return
        self.player.handle_play(track)
        
    # Navigation dans la playlist
    def _on_next(self):
        """Passe à la piste suivante et la joue."""
        track = self.playlist.get_next_track()
        if track:
            self.player.handle_play(track)
        else:
            logger.info("Fin de la playlist ou aucune piste suivante")
            
    def _on_previous(self):
        """Retourne à la piste précédente et la joue."""
        track = self.playlist.get_previous_track()
        if track:
            self.player.handle_play(track)
        else:
            logger.info("Début de la playlist ou aucune piste précédente")
    
    
    # ========================= #
    # Retours services          #
    # ========================= #    
    def _on_track_changed(self, track_path: str):
        """
        Slot appelé quand la piste change dans PlaylistServices.

        Args:
            track_path (str) : chemin de la nouvelle piste
        """
        logger.info(f"Track changée : {track_path}")
        self._update_controls_ui(track=self.playlist.current_track)


    def _on_playback_state_changed(self, state: str):
        """
        Slot appelé quand l'état de lecture change dans PlayerServices.

        Args:
            state (str) : 'playing', 'paused', 'stopped'
        """
        logger.info(f"État lecture : {state}")
        self._update_controls_ui(state=PlaybackState(state))


    def _on_volume_changed(self, volume: float):
        """
        Slot appelé quand le volume change dans PlayerServices.

        Args:
            volume (float) : volume entre 0.0 et 1.0
        """
        logger.info(f"Volume changé : {volume*100:.0f}%")
        self._update_controls_ui(volume=volume)
        
        
    # ========================= #
    #   Mise à jour UI centralisée
    # ========================= #
    def _update_controls_ui(
        self,
        track=None,
        state: Optional[PlaybackState] = None,
        volume: Optional[float] = None
    ) -> None:
        """Met à jour tous les widgets UI en fonction des signaux reçus."""
        if track:
            self.controls.track_label.setText(track.title)
        if state:
            self.controls.update_play_pause_icon(state)
        if volume is not None:
            self.controls.volume_slider.setValue(int(volume * 100))   
            
                 