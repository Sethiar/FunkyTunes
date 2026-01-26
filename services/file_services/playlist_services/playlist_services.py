# services/file_services/playlist_services/playlist_services.py


from typing import List
from PySide6.QtCore import QObject, Signal

from core.entities.playlist import Playlist as PlaylistEntity
from core.logger import logger

    
class PlaylistServices(QObject):
    """
    Service pour gérer les playlists en mémoire (entités métier),
    séparées de la base de données.

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
        self._playlists: dict[str, PlaylistEntity] = {}
        self._current_playlist_id: str | None = None
    
        
    # =============================== #
    #  Chargement de la bibliothèque  #
    # =============================== #
    def load_library_tracks(self, tracks_path: List[str]):
        """
        Charge toutes les pistes de la bibliothèque dans une playlist interne "Bibliothèque".

        Args:
            tracks_path (list[str]): liste de chemins de fichiers audio
        """
        library_id = "library"
        
        # Création d'une entité PlaylistEntity pour la bibliothèque
        self._playlists[library_id] = PlaylistEntity(
            id=-1,
            name="Bibliothèque",
            
            track_ids=[],
            tracks_path=tracks_path.copy() if tracks_path else [],
            
            current_index=0,
            user_id = None,
        )
        
        self._current_playlist_id = library_id

        # Signaux
        self.playlist_changed.emit()
        if tracks_path:
            self.track_changed.emit(self.current_track)  
        
        
    # ============================= #
    #    Gestion des playlists      #
    # ============================= #
    def create_playlist(self, name: str, tracks_path) -> str:
        """
        Crée une nouvelle playlist vide et la définit comme playlist courante.

        Args:
            name (str): nom de la nouvelle playlist

        Returns:
            str: identifiant unique de la playlist créée
        """
        playlist_id = f"playlist_{len(self._playlists)+1}" 
        
        playlist_id = "library"
        self._playlists[playlist_id] = PlaylistEntity(
            id=-1,
            name=name,
            track_ids=[],
            tracks_path=[],
            current_index=0,
            user_id=None
        )
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
            
            
    def get_current_track(self):
        return self.current_track


    def get_next_track(self):
        playlist = self.current_playlist
        if playlist and playlist.current_index + 1 < len(playlist.tracks_path):
            playlist.current_index += 1
            track = playlist.tracks_path[playlist.current_index]
            self.track_changed.emit(track)
            return track
        return None


    def get_previous_track(self):
        playlist = self.current_playlist
        if playlist and playlist.current_index - 1 >= 0:
            playlist.current_index -= 1
            track = playlist.tracks_path[playlist.current_index]
            self.track_changed.emit(track)
            return track
        return None
                

    # ============================ #
    #     Gestion des tracks       #
    # ============================ #
    def add_track_to_playlist(self, playlist_id: str, track_id: int):
        playlist = self._playlists.get(playlist_id)
        if not playlist:
            raise ValueError(f"Playlist {playlist_id} inexistante")
        if track_id not in playlist.track_ids:
            playlist.track_ids.append(track_id)
            self.playlist_changed.emit()


    def remove_track_from_playlist(self, playlist_id: str, track_id: int):
        playlist = self._playlists.get(playlist_id)
        if not playlist:
            raise ValueError(f"Playlist {playlist_id} inexistante")
        if track_id in playlist.track_ids:
            playlist.track_ids.remove(track_id)
            self.playlist_changed.emit()


    # ========================= #
    #       Accesseurs          #
    # ========================= #
    @property
    def current_playlist(self) -> PlaylistEntity | None:
        if self._current_playlist_id:
            return self._playlists.get(self._current_playlist_id)
        return None

    @property
    def current_track(self) -> str | None:
        playlist = self.current_playlist
        if playlist and playlist.tracks_path and playlist.current_index is not None:
            if 0 <= playlist.current_index < len(playlist.tracks_path):
                return playlist.tracks_path[playlist.current_index]
        return None
    
    