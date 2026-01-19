# services/file_services/playlist_services/playlist_services.py


from uuid import uuid4
from PySide6.QtCore import QObject, Signal

from core.entities.playlist import Playlist
from core.logger import logger

    
class PlaylistServices(QObject):
    """Gère toutes les playlists, y compris la bibliothèque."""
    
    # ======================== #
    #        Signaux           #
    # ======================== #
    
    playlist_changed = Signal()
    current_playlist_changed = Signal(str)
    track_changed = Signal(str)
    
    
    def __init__(self):
        super().__init__()
        self._playlists: dict[str, Playlist] = {}
        self._current_playlist_id: str | None
        
        
    # =============================== #
    #  Chargement de la bibliothèque  #
    # =============================== #
    def load_library_tracks(self, tracks: list[str]):
        """
        Charge toutes les pistes de la bibliothèque dans une playlist interne "Bibliothèque".
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
        
    @property
    def current_playlist(self) -> Playlist | None:
        if not self._current_playlist_id:
            return None
        return self._playlists.get(self._current_playlist_id)

    @property
    def current_track(self) -> str | None:
        playlist = self.current_playlist
        if not playlist or playlist.current_index is None:
            return None
        return playlist.tracks[playlist.current_index]
    
    def next(self) -> str | None:
        playlist = self.current_playlist
        if not playlist or not playlist.tracks:
            return None
        playlist.current_index = (playlist.current_index + 1) % len(playlist.tracks)
        self.track_changed.emit(self.current_track)
        return self.current_track
    
    
    # ============================= #
    #    Gestion des playlists      #
    # ============================= #    
    def create_playlist(self, name: str) -> str:
        playlist_id = str(uuid4())
        self._playlists[playlist_id] = Playlist(name=name, tracks=[])
        self._current_playlist_id = playlist_id
        self.playlist_changed.emit()
        self.current_playlist_changed.emit(playlist_id)
        return playlist_id

    def delete_playlist(self, playlist_id: str):
        if playlist_id not in self._playlists:
            return

        del self._playlists[playlist_id]

        if playlist_id == self._current_playlist_id:
            self._current_playlist_id = next(iter(self._playlists), None)

        self.playlist_changed.emit()
        
        
    def set_current_playlist(self, playlist_id: str):
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
        playlist = self.current_playlist
        if not playlist:
            return
        playlist.tracks.append(track_path)
        self.playlist_changed.emit()


    def remove_track(self, track_path: str):
        playlist = self.current_playlist
        if not playlist or track_path not in playlist.tracks:
            return
        index = playlist.tracks.index(track_path)
        playlist.tracks.remove(track_path)
        if playlist.current_index == index:
            playlist.current_index = 0 if playlist.tracks else None
            self.track_changed.emit(self.current_track)
        self.playlist_changed.emit()

    
    # ========================= #
    #         Navigation        #
    # ========================= #
    def next(self) -> str | None:
        playlist = self.current_playlist
        if not playlist or not playlist.tracks:
            return None

        playlist.current_index = (playlist.current_index + 1) % len(playlist.tracks)
        self.track_changed.emit(self.current_track)
        return self.current_track


    def previous(self) -> str | None:
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
        if not self._current_playlist_id:
            return None
        return self._playlists.get(self._current_playlist_id)

    @property
    def current_track(self) -> str | None:
        playlist = self.current_playlist
        if not playlist or playlist.current_index is None:
            logger.warning("PlaylistServices.current_track : aucune piste disponible")
            return None
        return playlist.tracks[playlist.current_index]
