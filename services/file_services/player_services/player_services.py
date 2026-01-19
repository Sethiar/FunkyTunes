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
    def handle_play(self, track_path: str | None = None):
        """
        Lit la piste donnée. Si track_path est None, lit la piste courante de la playlist.
        """
        # Si on a reçu un track à jouer, on met à jour l'index
        if track_path:
            try:
                self.current_index = self.playlist.index(track_path)
            except ValueError:
                logger.warning(f"Piste non trouvée dans la playlist : {track_path}")
                return

        # Vérification de la playlist
        if not self.playlist or self.current_index == -1:
            logger.warning("Aucune piste à lire")
            return

        file_path = self.playlist[self.current_index]
        
        # Définir le fichier à lire
        self.player.setSource(QUrl.fromLocalFile(file_path))
       
        self.player.play()
        logger.info(f"Lecture : {file_path}")
        
    
    def handle_pause(self):
        self.player.pause()
        logger.info("Pause")
        
    
    
    def handle_stop(self):
        self.player.stop()
        logger.info("Stop")
    
    
    # ========================= #
    #      Contrôles volume     #
    # ========================= #
    def handle_volume_up(self):
        self.player.setVolume(min(self.player.volume() + 10, 100))
        self.volume_changed.emit(self.player.volume() / 100)
        logger.info(f"Volume augmenté")

    def handle_volume_down(self):
        self.player.setVolume(max(self.player.volume() - 10, 0))
        self.volume_changed.emit(self.player.volume() / 100)
        logger.info(f"Volume diminué")

    def handle_volume_mute(self):
        self._is_muted = not self._is_muted
        self.audio_output.setMuted(self._is_muted)
        logger.info(f"Mute : {self._is_muted}")

        
        