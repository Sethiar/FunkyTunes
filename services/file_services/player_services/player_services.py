# services/file_services/player_services/player_services.py


import os

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QObject, Signal, QUrl

from core.logger import logger


class PlayerServices(QObject):
    """
    Service de lecture audio local.
    Gère la lecture d'un fichier audio à la fois, le volume et le mute.
    N'inclut pas la gestion de playlist complète.
    
    Rôle :
        - Gérer la lecture de fichiers audio locaux
        - Contrôler le volume et le mute
        - Émettre des signaux Qt pour l'état de lecture et le volume

    Signaux :
        playback_state_changed(str) : 'playing', 'paused', 'stopped'
        volume_changed(float) : volume entre 0.0 et 1.0
    """
    
    # ============================ #
    #            Signaux           #
    # ============================ #
    playback_state_changed = Signal(str)
    volume_changed = Signal(float)
    
    def __init__(self):
        """
        Initialialisation du lecteur audio et configuration de QAudioOutput.
        """
        super().__init__()
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        
        # Chemin du fichier courant
        self._current_source: str | None = None
         
        # État mute
        self._is_muted = False
        
        # Connexion pour suivre l'état réel du player Qt
        self.player.playbackStateChanged.connect(self._on_state_changed)
        
        
    # ========================== #
    #    Contrôles playback      #
    # ========================== #      
    def handle_play(self, file_path: str):
        """
        Lancement de la lecture d'un fichier audio.

        Args:
            file_path (str) : chemin du fichier audio à lire
        """
        if not file_path or not os.path.exists(file_path):
            logger.warning(f"Fichier audio invalide : {file_path}")
            return
        
        # Si le fichier diffèrent de celui en cours -> Préparation
        if file_path != self._current_source:
            self._current_source = file_path
            self.player.setSource(QUrl.fromLocalFile(file_path))

        self.player.play()
        logger.info(f"Lecture : {file_path}")
        
    
    def handle_pause(self):
        """Mise en pause de la lecture."""
        self.player.pause()
        logger.info("Pause")
        
    
    def handle_stop(self):
        """Arrêt de la lecture."""
        self.player.stop()
        logger.info("Stop")
    
    
    # ========================= #
    #      Contrôles volume     #
    # ========================= #
    def set_volume(self, value: float):
        """
        Définition du volume du lecteur.

        Args:
            value (float) : volume entre 0.0 et 1.0
        """
        value = max(0.0, min(1.0, value))
        self.audio_output.setVolume(value)
        self.volume_changed.emit(value)
        logger.info(f"Volume : {value}")
    
    
    def handle_volume_up(self):
        """Augmentation du volume de 10%."""
        current = self.audio_output.volume()
        self.set_volume(current + 0.1)
        logger.info(f"Volume augmenté")


    def handle_volume_down(self):
        """Diminution du volume de 10%."""
        current = self.audio_output.volume()
        self.set_volume(current - 0.1)
        logger.info(f"Volume diminué")
        

    def handle_volume_mute(self):
        """Activation ou désactivation du mute."""
        self._is_muted = not self._is_muted
        self.audio_output.setMuted(self._is_muted)
        logger.info(f"Mute : {self._is_muted}")

    
    # ========================== #
    #   Méthodes pour lecture    #
    # ========================== #
    def _on_state_changed(self, state: QMediaPlayer.PlaybackState):
        """
        Slot interne pour convertir l'état Qt en chaîne lisible et émettre le signal.
        """
        mapping = {
            QMediaPlayer.PlayingState: "playing",
            QMediaPlayer.PausedState: "paused",
            QMediaPlayer.StoppedState: "stopped",
        }
        state_str = mapping.get(state, "unknown")
        self.playback_state_changed.emit(state_str)
    
    
    def prepare(self, file_path: str):
        """
        Prépare une piste pour lecture sans la lancer.

        Args:
            file_path (str) : chemin du fichier à préparer
        """
        if not file_path or not os.path.exists(file_path):
            logger.warning(f"Fichier audio invalide : {file_path}")
            return

        if file_path != self._current_source:
            self._current_source = file_path
            self.player.setSource(QUrl.fromLocalFile(file_path))
    
        logger.info(f"Piste préparée : {file_path}")   
               
        