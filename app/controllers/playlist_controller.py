# app/controllers/playlist_controller.py


from PySide6.QtCore import QObject
from core.logger import logger

from app.UI.molecules.playlist_panel import PlaylistPanel
from services.file_services.player_services.player_services import PlayerServices
from services.file_services.playlist_services.playlist_services import PlaylistServices
from services.file_services.library_services.library_services import LibraryServices

class PlaylistController(QObject):
    """
    Controller pour gérer la bibliothèque musicale et la playlist.

    Rôle :
        - Initialiser la bibliothèque depuis le service LibraryServices
        - Charger les pistes dans PlaylistServices
        - Préparer la lecture dans PlayerServices
        - Réagir aux actions utilisateur via l'UI PlaylistPanel
        - Ne gère pas la lecture directement (délégué à PlayerServices)
    """
    
    def __init__(self, ui: PlaylistPanel, playlist_service: PlaylistServices, player_service: PlayerServices, library_service: LibraryServices):
        super().__init__()
        self.ui = ui
        self.playlist = playlist_service
        self.player = player_service
        self.library_service = library_service
        
        # Lier l'UI aux méthodes du controller
        self._bind_ui()
        
        # Lier les signaux des services aux slots du controller
        self._bind_service()
        
        # Initialisation de la bibliothèque au démarrage
        self.init_library()
        
        
    # ========================= #
    #      UI → Controller      #
    # ========================= #     
    def _bind_ui(self):
        """Connecte les signaux de l'UI aux méthodes du controller."""
        self.ui.request_create_playlist.connect(self._create_playlist)
        self.ui.request_delete_playlist.connect(self._delete_playlist)
        self.ui.request_add_track.connect(self._add_track)
        self.ui.request_remove_track.connect(self._remove_track)
        self.ui.request_select_track.connect(self._play_track)   
        
    
    # ========================= #
    # Services → Controller     #
    # ========================= #    
    def _bind_service(self):
        """Connecte les signaux des services PlaylistServices aux slots du controller."""
        self.playlist.playlist_changed.connect(self._refresh_ui)
        self.playlist.track_changed.connect(self._on_track_changed)

    
    # ================================= #
    #       Initialisation Library      #
    # ================================= #
    def init_library(self):
        """
        Récupère les pistes depuis LibraryServices et les charge dans PlaylistServices.

        Prépare le premier titre pour lecture via PlayerServices.
        """
        tracks_paths = self.library_service.get_track_file_paths()
        if not tracks_paths:
            logger.warning("Aucune piste trouvée dans la bibliothèque")
            return
        
        # Charger les pistes dans la playlist
        self.playlist.load_library_tracks(tracks_paths)

        # Lecture du premier titre (si existant)
        first_track = self.playlist.current_track
        if first_track:
            self.player.prepare(first_track)
                
    
    # ========================= #
    #   Actions utilisateur     #
    # ========================= #            
    def _create_playlist(self):
        """Créer une nouvelle playlist."""
        self.playlist.create_playlist("Nouvelle playlist")


    def _delete_playlist(self):
        """Supprime la playlist courante."""
        self.playlist.delete_playlist()


    def _add_track(self):
        """Ajouter une piste à la playlist (à implémenter)."""
        pass


    def _remove_track(self):
        """Supprimer une piste de la playlist (à implémenter)."""
        pass


    def _play_track(self, track_path: str):
        """
        Lit une piste spécifique sélectionnée dans l'UI.

        Args:
            track_path (str) : chemin de la piste à lire
        """
        self.player.handle_play(track_path)
        
    
    # ========================= #
    #   Slots pour signaux      #
    # ========================= #
    def _refresh_ui(self):
        """Met à jour l’UI de la playlist lorsque celle-ci change."""
        logger.info("Playlist mise à jour")
        # TODO: mettre à jour self.ui, ex: self.ui.update_playlist(self.playlist.current_playlist)

    def _on_track_changed(self, track_path: str):
        """Réagit quand la piste courante change dans PlaylistServices."""
        logger.info(f"Track changée dans la playlist: {track_path}")
        # TODO: sélectionner la track dans l’UI
        
        