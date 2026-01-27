# app/controllers/playlist_controllers/playlist_maker_controller.py


from PySide6.QtCore import QObject, Signal

from app.UI.screens.window_services.create_playlist_dialog import CreatePlaylistDialog
from services.file_services.playlist_services.playlist_maker_services import PlaylistMakerServices

from core.logger import logger

class PlaylistMakerController(QObject):
    """
    Controller pour gérer la création d'une playlist.
    """
    
    # =========== #
    #    Signal   #
    # =========== #
    playlist_created = Signal(object)


    def __init__(self, ui: CreatePlaylistDialog, playlist_maker_service: PlaylistMakerServices):
        super().__init__()
        self.ui = ui
        self.playlist_maker_service = playlist_maker_service

        # Connecter les callbacks UI
        self.ui.on_submit = self._on_submit
        self.ui.on_cancel = self._on_cancel

   
    # ============= #
    #  Submit Form  #
    # ============= #
    def _on_submit(self, data: dict):
        name = data.get("name")
        tracks = data.get("tracks", [])
        user_id = data.get("user_id", 1)
        
        if not name:
            self.ui._show_error("Le nom de la playlist est obligatoire")
            return
        
        try:
            # Création de la playlist en DB via le service
            playlist = self.playlist_maker_service.create_playlist(name, user_id)
            # Ajout des pistes si nécessaire
            for track_id in tracks:
                self.playlist_maker_service.add_track_to_playlist(
                    playlist_id=playlist.id,
                    track_id=track_id
                )
                
        except Exception as e:
            logger.exception("Erreur lors de la création de la playlist")
            self.ui._show_error("Impossible de créer la playlist")
            
            return

        # Émission du signal pour mise à jour du panel
        self.playlist_created.emit(playlist)
        self.ui.setVisible(False)

    
    # =============== #
    #  Cancel Action  #
    # =============== #
    def _on_cancel(self):
        logger.info("Création de playlist annulée")
        self.ui.setVisible(False)

    
    # =============== #
    #    Open Form    #
    # =============== #
    def open_form(self):
        """Affiche le formulaire."""
        logger.info("PlaylistMakerController : ouverture du formulaire")

        tracks = self.playlist_maker_service.get_available_tracks()

        self.ui.set_available_tracks(tracks)

        self.ui.setVisible(True)
        self.ui.raise_()
        self.ui.activateWindow()

        
        