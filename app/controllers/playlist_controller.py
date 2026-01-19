# app/controllers/playlist_controller.py


from PySide6.QtCore import QObject
from core.logger import logger


class PlaylistController(QObject):
    
    def __init__(self, ui, playlist_service, player_service, library_service):
        super().__init__()
        self.ui = ui
        self.playlist = playlist_service
        self.player = player_service
        self.library_service = library_service
        
        # Connecter signaux UI et service
        self._bind_ui()
        self._bind_service()
        
        # Initialisation de la bibliothèque au démarrage
        self.init_library()
        
        
    def _bind_ui(self):
        self.ui.request_create_playlist.connect(self._create_playlist)
        self.ui.request_delete_playlist.connect(self._delete_playlist)
        self.ui.request_add_track.connect(self._add_track)
        self.ui.request_remove_track.connect(self._remove_track)
        self.ui.request_select_track.connect(self._play_track)   
        
        
    def _bind_service(self):
        self.playlist.playlist_changed.connect(self._refresh_ui)
        self.playlist.track_changed.connect(self._on_track_changed)

    
    # ================================= #
    #     Initialisation de la library  #
    # ================================= #
    def init_library(self):
        tracks_paths = self.library_service.get_track_file_paths()
        if tracks_paths:
            self.playlist.load_library_tracks(tracks_paths)
            # On prépare le premier titre dans le PlayerService
            first_track = self.playlist.current_track
            if first_track:
                self.player.set_playlist(tracks_paths)  # PlayerService garde une référence
                self.player.handle_play(first_track)
                
                
    def _create_playlist(self):
        self.playlist.create_playlist("Nouvelle playlist")


    def _delete_playlist(self):
        self.playlist.delete_current()


    def _add_track(self):
        # plus tard: file picker
        pass


    def _remove_track(self):
        pass


    def _play_track(self, track_path: str):
        self.player.handle_play(track_path)
        
    
    # =============================
    # Slots pour signals service
    # =============================
    def _refresh_ui(self):
        """Met à jour l’UI de la playlist (liste, etc.)."""
        logger.info("Playlist mise à jour")
        # TODO: mettre à jour self.ui, ex: self.ui.update_playlist(self.playlist.current_playlist)

    def _on_track_changed(self, track_path: str):
        """Réagit quand la track change dans la playlist."""
        logger.info(f"Track changée dans la playlist: {track_path}")
        # TODO: sélectionner la track dans l’UI