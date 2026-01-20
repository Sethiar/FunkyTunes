# services/file_services/playlist_services/playlist_services.py


from uuid import uuid4
from PySide6.QtCore import QObject, Signal

from core.entities.playlist import Playlist
from core.logger import logger

    
class PlaylistServices(QObject):
    """
    Service pour gérer toutes les playlists, y compris la bibliothèque.

    Rôle :
        - Charger et gérer la bibliothèque musicale
        - Créer, supprimer et sélectionner des playlists
        - Naviguer dans les pistes (next / previous)
        - Émettre des signaux pour mise à jour de l'UI
    """
    
    # ======================== #
    #        Signaux           #
    # ======================== #
    
    playlist_changed = Signal()
    current_playlist_changed = Signal(str)
    track_changed = Signal(str)
    
    
    def __init__(self):
        """Initialise le service avec un dictionnaire de playlists vide."""
        super().__init__()
        self._playlists: dict[str, Playlist] = {}
        self._current_playlist_id: str | None = None
        
        
    # =============================== #
    #  Chargement de la bibliothèque  #
    # =============================== #
    def load_library_tracks(self, tracks: list[str]):
        """
        Charge toutes les pistes de la bibliothèque dans une playlist interne "Bibliothèque".

        Args:
            tracks (list[str]): liste de chemins de fichiers audio
        """
        library_id = "library"
        self._playlists[library_id] = Playlist(
            name="Bibliothèque",
            tracks=tracks.copy(),
            current_index=0 if tracks else None
        )

        # Définir comme playlist active
        self._current_playlist_id = library_id

        # Signaux
        self.playlist_changed.emit()
        if tracks:
            self.track_changed.emit(self.current_track)  
        
        
    # ============================= #
    #    Gestion des playlists      #
    # ============================= #
    def create_playlist(self, name: str) -> str:
        """
        Crée une nouvelle playlist vide et la définit comme playlist courante.

        Args:
            name (str): nom de la nouvelle playlist

        Returns:
            str: identifiant unique de la playlist créée
        """
        playlist_id = str(uuid4())
        self._playlists[playlist_id] = Playlist(name=name, tracks=[])
        self._current_playlist_id = playlist_id

        # Signaux
        self.playlist_changed.emit()
        self.current_playlist_changed.emit(playlist_id)

        return playlist_id


    def delete_playlist(self, playlist_id: str):
        """
        Supprime une playlist par son ID.

        Args:
            playlist_id (str): ID de la playlist à supprimer
        """
        if playlist_id not in self._playlists:
            return

        del self._playlists[playlist_id]

        if playlist_id == self._current_playlist_id:
            self._current_playlist_id = next(iter(self._playlists), None)

        self.playlist_changed.emit()


    def set_current_playlist(self, playlist_id: str):
        """
        Définit la playlist courante par son ID et prépare la première piste.

        Args:
            playlist_id (str): ID de la playlist
        """
        if playlist_id not in self._playlists:
            return

        self._current_playlist_id = playlist_id
        self.current_playlist_changed.emit(playlist_id)

        playlist = self.current_playlist
        if playlist and playlist.tracks:
            playlist.current_index = 0
            self.track_changed.emit(self.current_track)


    # ============================ #
    #     Gestion des tracks       #
    # ============================ #
    def add_track(self, track_path: str):
        """
        Ajoute une piste à la playlist courante.

        Args:
            track_path (str): chemin du fichier audio
        """
        playlist = self.current_playlist
        if not playlist:
            return
        playlist.tracks.append(track_path)
        self.playlist_changed.emit()


    def remove_track(self, track_path: str):
        """
        Supprime une piste de la playlist courante.

        Args:
            track_path (str): chemin du fichier à supprimer
        """
        playlist = self.current_playlist
        if not playlist or track_path not in playlist.tracks:
            return

        index = playlist.tracks.index(track_path)
        playlist.tracks.remove(track_path)

        # Ajuster l'index si nécessaire
        if playlist.current_index == index:
            playlist.current_index = 0 if playlist.tracks else None
            self.track_changed.emit(self.current_track)

        self.playlist_changed.emit()


    # ========================= #
    #         Navigation        #
    # ========================= #
    def next(self) -> str | None:
        """
        Passe à la piste suivante de la playlist courante.

        Returns:
            str | None: chemin de la piste suivante ou None si aucune piste
        """
        playlist = self.current_playlist
        if not playlist or not playlist.tracks:
            return None

        playlist.current_index = (playlist.current_index + 1) % len(playlist.tracks)
        self.track_changed.emit(self.current_track)
        return self.current_track


    def previous(self) -> str | None:
        """
        Passe à la piste précédente de la playlist courante.

        Returns:
            str | None: chemin de la piste précédente ou None si aucune piste
        """
        playlist = self.current_playlist
        if not playlist or not playlist.tracks:
            return None

        playlist.current_index = (playlist.current_index - 1) % len(playlist.tracks)
        self.track_changed.emit(self.current_track)
        return self.current_track


    # ======================== #
    #        Propriétés        #
    # ======================== #
    @property
    def current_playlist(self) -> Playlist | None:
        """Retourne la playlist courante ou None si aucune sélection."""
        if not self._current_playlist_id:
            return None
        return self._playlists.get(self._current_playlist_id)


    @property
    def current_track(self) -> str | None:
        """
        Retourne la piste courante de la playlist.

        Returns:
            str | None: chemin du fichier audio ou None si aucune piste
        """
        playlist = self.current_playlist
        if not playlist or playlist.current_index is None:
            logger.warning("PlaylistServices.current_track : aucune piste disponible")
            return None
        return playlist.tracks[playlist.current_index]
    
    