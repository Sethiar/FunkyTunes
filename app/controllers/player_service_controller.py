# app/controller/player_service_controller.py


from PySide6.QtCore import QObject

from app.UI.molecules.player_controls import PlayerControls
from services.file_services.player_services.player_services import PlayerServices
from services.file_services.playlist_services.playlist_services import PlaylistServices

from core.logger import logger


class PlayerServiceController(QObject):
    """
    Controller qui relie l'interface PlayerControls à PlayerServices et PlaylistServices.

    Responsabilités :
    - Relier les actions de l'UI aux services audio et playlist
    - Suivre les changements d'état et mettre à jour l'UI
    - Ne fait pas de lecture directe ou de gestion de fichiers
    
    """
    
    def __init__(
        self, 
        controls: PlayerControls, 
        player_service: PlayerServices,
        playlist_service: PlaylistServices
    ):
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
       
        # Lier l'UI aux méthodes du controller
        self._bind_ui_to_controller()
        
        # Lier les signaux des services aux méthodes de mise à jour
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
    def _bind_services_to_controller(self):
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
        
        
    def _on_next(self):
        """Passe à la piste suivante et la joue."""
        track = self.playlist.next()
        if track:
            self.player.handle_play(track)

    def _on_previous(self):
        """Retourne à la piste précédente et la joue."""
        track = self.playlist.previous()
        if track:
            self.player.handle_play(track)   
    
    
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
        # Ici, tu peux mettre à jour un label ou la jaquette si tu veux
        # Ex: self.controls.track_label.setText(os.path.basename(file_path))


    def _on_playback_state_changed(self, state: str):
        """
        Slot appelé quand l'état de lecture change dans PlayerServices.

        Args:
            state (str) : 'playing', 'paused', 'stopped'
        """
        logger.info(f"État lecture : {state}")
        # Ici, tu peux changer l'icône Play/Pause selon state


    def _on_volume_changed(self, volume: float):
        """
        Slot appelé quand le volume change dans PlayerServices.

        Args:
            volume (float) : volume entre 0.0 et 1.0
        """
        logger.info(f"Volume changé : {volume*100:.0f}%")
        # Ici, tu peux mettre à jour un slider ou un label volume
        
        
            