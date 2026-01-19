# app/controller/player_service_controller.py


from PySide6.QtCore import QObject

from app.UI.molecules.player_controls import PlayerControls
from services.file_services.player_services.player_services import PlayerServices
from services.file_services.playlist_services.playlist_services import PlaylistServices

from core.logger import logger


class PlayerServiceController(QObject):
    """
    Controller pour relier PlayerControls à PlayerServices.
    
    Rôle :
        - Connecter les boutons de l'UI aux méthodes du service
        - Connecter les signaux du service pour mettre à jour l'UI
    """
    
    def __init__(
        self, 
        controls: PlayerControls, 
        player_service: PlayerServices,
        playlist_service: PlaylistServices
    ):
        
        super().__init__()
        self.controls = controls
        self.player = player_service
        self.playlist = playlist_service

        self._bind_ui_to_controller()
        self._bind_services_to_controller()

        logger.info("PlayerServiceController initialisé")
        
    # ========================= #
    #      UI → Controller      #
    # ========================= #
    def _bind_ui_to_controller(self):
        self.controls.request_play.connect(self.player.handle_play)
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
        self.playlist.track_changed.connect(self._on_track_changed)
        self.player.playback_state_changed.connect(self._on_playback_state_changed)
        self.player.volume_changed.connect(self._on_volume_changed)   
        
    
    # ========================= #
    # Actions utilisateur       #
    # ========================= #
    def _on_play(self):
        track = self.playlist.current_track
        if not track:
            logger.warning("Aucune piste à lire")
            return
        self.player.handle_play(track)
        
        
    def _on_next(self):
        track = self.playlist.next()
        if track:
            self.player.handle_play(track)

    def _on_previous(self):
        track = self.playlist.previous()
        if track:
            self.player.handle_play(track)   
    
    
    # ========================= #
    # Retours services          #
    # ========================= #    
    def _on_track_changed(self, track_path: str):
        logger.info(f"Track changée : {track_path}")
        # Ici, tu peux mettre à jour un label ou la jaquette si tu veux
        # Ex: self.controls.track_label.setText(os.path.basename(file_path))

    def _on_playback_state_changed(self, state: str):
        logger.info(f"État lecture : {state}")
        # Ici, tu peux changer l'icône Play/Pause selon state

    def _on_volume_changed(self, volume: float):
        logger.info(f"Volume changé : {volume*100:.0f}%")
        # Ici, tu peux mettre à jour un slider ou un label volume
        
        
    # ============================ #
    #     Gestion de la playlist   #   
    # ============================ #
    def load_playlist(self, tracks: list[str]):
        """
        Charge la playlist dans PlayerServices.
        """
        if not tracks:
            logger.warning("Aucune piste fournie pour la playlist")
            return

        self.player.set_playlist(tracks)
        logger.info(f"{len(tracks)} pistes chargées dans PlayerServices")    
        
            