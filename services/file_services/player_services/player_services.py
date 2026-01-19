# services/file_services/player_services/player_services.py


import os

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QObject, Signal, QUrl

from core.logger import logger


class PlayerServices(QObject):
    """
    Service de lecture audio local.
    Gère la playlist, la lecture, le volume, le mute, et les signaux Qt.
    """
    # ============ #
    #    Signaux   #
    # ============ #
    track_changed = Signal(str)
    playback_state_changed = Signal(str)
    volume_changed = Signal(float)
    
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        
        # Playlist : liste des chemins
        self.playlist = []
        self.current_index = -1
        
        # État mute
        self._is_muted = False
        
        # Connexion des signaux internes Qt
        self.player.playbackStateChanged.connect(self._on_state_changed)
        
        
    # ========================= #
    #       Playlist API        #
    # ========================= #
    def set_playlist(self, tracks: list[str]):
        """Remplace la playlist par une nouvelle liste de fichiers audio"""
        self.playlist = tracks
        self.current_index = 0 if tracks else -1
        logger.info(f"Playlist mise à jour avec {len(tracks)} pistes.")
        
        
    # ========================== #
    #    Contrôles playback      #
    # ========================== #      
    def handle_play(self):
        if self.current_index == -1 or not self.playlist:
            logger.warning("Aucune piste à lire")
            return
    
        file_path = self.playlist[self.current_index]
        self._set_source(file_path)
        self.player.play()
        logger.info(f"Lecture : {file_path}")
        
    
    def handle_pause(self):
        self.player.pause()
        logger.info("Pause")
        
    
    def handle_previous(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        file_path = self.playlist[self.current_index]
        self._set_source(file_path)
        self.player.play()
        logger.info(f"Piste précédente : {file_path}")
        
        
    def handle_next(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        file_path = self.playlist[self.current_index]
        self._set_source(file_path)
        self.player.play()
        logger.info(f"Piste suivante : {file_path}")
    
    
    def handle_stop(self):
        self.player.stop()
        logger.info("Stop")
    
    
    # ========================= #
    #      Contrôles volume     #
    # ========================= #
    def handle_volume_up(self):
        vol = min(self.audio_output.volume() + 0.1, 1.0)
        self.audio_output.setVolume(vol)
        self.volume_changed.emit(vol)
        logger.info(f"Volume augmenté : {vol*100:.0f}%")

    def handle_volume_down(self):
        vol = max(self.audio_output.volume() - 0.1, 0.0)
        self.audio_output.setVolume(vol)
        self.volume_changed.emit(vol)
        logger.info(f"Volume diminué : {vol*100:.0f}%")

    def handle_volume_mute(self):
        self._is_muted = not self._is_muted
        self.audio_output.setMuted(self._is_muted)
        logger.info(f"Mute : {self._is_muted}")

    # ========================= #
    #        Méthodes internes #
    # ========================= #
    def _set_source(self, file_path: str):
        """Charge une piste audio si ce n'est pas déjà la piste courante."""
        if os.path.exists(file_path):
            self.player.setSource(QUrl.fromLocalFile(file_path))
            self.track_changed.emit(file_path)
        else:
            logger.error(f"Fichier introuvable : {file_path}")

    def _on_state_changed(self, state):
        """Émet le signal playback_state_changed quand le state change."""
        states = {
            QMediaPlayer.PlayingState: "playing",
            QMediaPlayer.PausedState: "paused",
            QMediaPlayer.StoppedState: "stopped"
        }
        self.playback_state_changed.emit(states.get(state, "unknown"))
        
        