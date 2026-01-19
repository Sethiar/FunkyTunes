# app/controller/player_service_controller.py


from PySide6.QtCore import QObject

from app.UI.molecules.player_controls import PlayerControls
from services.file_services.player_services.player_services import PlayerServices

from core.logger import logger


class PlayerServiceController(QObject):
    """
    Controller pour relier PlayerControls à PlayerServices.
    
    Rôle :
        - Connecter les boutons de l'UI aux méthodes du service
        - Connecter les signaux du service pour mettre à jour l'UI
    """
    
    def __init__(self, controls: PlayerControls, service: PlayerServices):
        super().__init__()
        self.controls = controls
        self.service = service

        self._bind_ui_to_service()
        self._bind_service_to_ui()

        logger.info("PlayerController initialisé")
        
    # ========================= #
    # Connexion UI → Service    #
    # ========================= #
    def _bind_ui_to_service(self):
        self.controls.request_play.connect(self.service.handle_play)
        self.controls.request_pause.connect(self.service.handle_pause)
        self.controls.request_stop.connect(self.service.handle_stop)
        self.controls.request_next.connect(self.service.handle_next)
        self.controls.request_previous.connect(self.service.handle_previous)
        self.controls.request_volume_up.connect(self.service.handle_volume_up)
        self.controls.request_volume_down.connect(self.service.handle_volume_down)
        self.controls.request_volume_mute.connect(self.service.handle_volume_mute)
        
        
    # ========================= #
    # Connexion Service → UI    #
    # ========================= #
    def _bind_service_to_ui(self):
        self.service.track_changed.connect(self._on_track_changed)
        self.service.playback_state_changed.connect(self._on_playback_state_changed)
        self.service.volume_changed.connect(self._on_volume_changed)    
        
        
    # ========================= #
    #    Slots pour UI update   #
    # ========================= #        
    def _on_track_changed(self, file_path: str):
        logger.info(f"Track changée : {file_path}")
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

        self.service.set_playlist(tracks)
        logger.info(f"{len(tracks)} pistes chargées dans PlayerServices")    
        
            