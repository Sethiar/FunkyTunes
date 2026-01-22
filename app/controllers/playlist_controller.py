# app/controllers/playlist_controller.py


from typing import Optional, List

from PySide6.QtCore import Qt, QObject

from app.UI.screens.window_services.playlist_panel import PlaylistPanel
from app.controllers.tracks_sort_controller import TracksBySortController
from services.file_services.player_services.player_services import PlayerServices
from services.file_services.playlist_services.playlist_services import PlaylistServices
from services.file_services.library_services.library_services import LibraryServices

from core.logger import logger
from core.entities.track import Track


class PlaylistController(QObject):
    """
    Controller principal pour la gestion de la playlist et de la bibliothèque musicale.

    Responsabilités :
        - Charger et initialiser la bibliothèque depuis LibraryServices
        - Gérer les playlists via PlaylistServices
        - Préparer la lecture via PlayerServices
        - Réagir aux actions utilisateur via l'UI PlaylistPanel
        - Déléguer les tris à TracksBySortController
    """
    
    def __init__(
        self,
        ui: PlaylistPanel,
        playlist_service: PlaylistServices,
        player_service: PlayerServices,
        library_service: LibraryServices,
        sort_tracks_widget
    ):
        super().__init__()

        self.ui: PlaylistPanel = ui
        self.playlist: PlaylistServices = playlist_service
        self.player: PlayerServices = player_service
        self.library_service: LibraryServices = library_service
        
        # Instanciation du controller de tri
        self.sort_controller = TracksBySortController(self.ui, self.library_service)
        self._bind_sort_buttons(sort_tracks_widget)

        # Lier UI et services
        self._bind_ui()
        self._bind_service()

        # Charger la bibliothèque et la playlist au démarrage
        self.init_library()
        self.show_library_tracks()


    # ========================= #
    #      UI → Controller      #
    # ========================= #
    def _bind_ui(self) -> None:
        """Connecte les signaux de l'UI aux méthodes du controller."""
        self.ui.playlist_menu.request_create_playlist.connect(self._create_playlist)
        self.ui.playlist_menu.request_delete_playlist.connect(self._delete_playlist)
        self.ui.playlist_menu.request_add_track.connect(self._add_track)
        self.ui.playlist_menu.request_remove_track.connect(self._remove_track)


    # ========================= #
    # Services → Controller     #
    # ========================= #
    def _bind_service(self) -> None:
        """Connecte les signaux des services PlaylistServices aux slots du controller."""
        self.playlist.playlist_changed.connect(self._refresh_ui)
        self.playlist.track_changed.connect(self._on_track_changed)


    # ========================= #
    # Initialisation Library     #
    # ========================= #
    def init_library(self) -> None:
        """
        Charge la bibliothèque depuis LibraryServices dans PlaylistServices
        et prépare la lecture du premier titre.
        """
        tracks_paths = self.library_service.get_track_file_paths()
        if not tracks_paths:
            logger.warning("Aucune piste trouvée dans la bibliothèque")
            return

        self.playlist.load_library_tracks(tracks_paths)

        # Préparer la lecture du premier titre si disponible
        first_track = self.playlist.current_track
        if first_track:
            self.player.prepare(first_track)
            
            
    def _bind_sort_buttons(self, sort_widget):
        sort_widget.sort_by_artist.connect(self.sort_controller.show_by_artist)
        sort_widget.sort_by_album.connect(self.sort_controller.show_by_album)
        sort_widget.sort_by_genre.connect(self.sort_controller.show_by_genre)
        sort_widget.sort_by_favorites.connect(self.sort_controller.show_favorites)        
    
    
    # ========================= #
    #   Actions utilisateur     #
    # ========================= #
    def _create_playlist(self) -> None:
        """Créer une nouvelle playlist."""
        self.playlist.create_playlist("Nouvelle playlist")

    def _delete_playlist(self) -> None:
        """Supprime la playlist courante."""
        self.playlist.delete_playlist()

    def _add_track(self) -> None:
        """Ajouter une piste à la playlist (à implémenter)."""
        pass

    def _remove_track(self) -> None:
        """Supprimer une piste de la playlist (à implémenter)."""
        pass

    def _play_track(self, track_path: str) -> None:
        """
        Lit une piste spécifique sélectionnée dans l'UI.

        Args:
            track_path (str): chemin de la piste à lire
        """
        self.player.handle_play(track_path)


    # ========================= #
    #   Méthodes publiques      #
    # ========================= #
    def show_library_tracks(self, tracks: Optional[List[Track]] = None) -> None:
        """
        Met à jour l'affichage des tracks dans le panel.

        Args:
            tracks (Optional[List[Track]]): si None, charge toutes les tracks de LibraryServices
        """
        if tracks is None:
            tracks = self.library_service.get_tracks()
        self.ui.display_tracks(tracks)


    # ========================= #
    #   Slots pour signaux      #
    # ========================= #
    def _refresh_ui(self) -> None:
        """Met à jour l’UI lorsque la playlist change."""
        logger.info("Playlist mise à jour")
        # TODO: Mettre à jour self.ui.playlist_list si nécessaire
        # self.ui.update_playlist(self.playlist.current_playlist)

    def _on_track_changed(self, track_path: str) -> None:
        """
        Sélectionne la piste courante dans la table UI lorsque PlaylistServices change de track.

        Args:
            track_path (str): chemin de la track courante
        """
        logger.info(f"Track changée : {track_path}")
        self.ui.tracks_table_view.clearSelection()
        
        model = self.ui.tracks_proxy_model
        for row in range(model.rowCount()):
            index = model.index(row, 0)
            track: Track = model.data(index, role=Qt.UserRole)  
            if track and track.path == track_path:
                self.ui.tracks_table_view.selectRow(row)
                self.ui.tracks_table_view.scrollTo(index)
                break
            
            