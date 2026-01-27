# app/UI/molecules/player_controls.py


"""
Fichier qui crée les contrôles du lecteur pour l'interface utilisateur.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Qt, Signal

from app.UI.atoms.icons_button import IconButton


class PlayerControls(QWidget):
    """
    Classe pour les contrôles du lecteur personnalisé de l'application.
    """
    
    # ======================== # 
    #         Signaux          #
    # ======================== # 
    
    request_play = Signal()
    request_pause = Signal()
    request_next = Signal()
    request_previous = Signal()
    request_stop = Signal()
    request_volume_up = Signal()
    request_volume_down = Signal()
    request_volume_mute = Signal()
    
    
    # ============================ # 
    #        Initialisation        #
    # ============================ # 
    def __init__(self):
        super().__init__()
        self.setProperty("component", "player-controls")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setMinimumWidth(300)
        
        self._build_ui()
        self._binding_signals()
    
    
    # ============================ # 
    #     Construction de l'UI     #
    # ============================ #     
    def _build_ui(self):   
        # Ajout d'un layout horizontal pour les boutons
        self.player_controls_layout = QHBoxLayout()
        self.player_controls_layout.setSpacing(5)
        self.player_controls_layout.setContentsMargins(8, 8, 8, 8)

        self.play_button = IconButton("play", tooltip="Lire")
        self.pause_button = IconButton("pause", tooltip="Pause")
        self.next_button = IconButton("next", tooltip="Piste suivante")
        self.previous_button = IconButton("previous", tooltip="Piste précédente")
        self.stop_button = IconButton("stop", tooltip="Arrêter")
        self.volume_up_button = IconButton("volume_1", tooltip="Augmenter le volume")
        self.volume_down_button = IconButton("volume_2", tooltip="Réduire le volume")
        self.mute_button = IconButton("volume_x", tooltip="Muet")

        for btn in (
            self.play_button,
            self.pause_button,
            self.next_button,
            self.previous_button,
            self.stop_button,
            self.volume_up_button,
            self.volume_down_button,
            self.mute_button
            
        ):
            self.player_controls_layout.addWidget(btn)

        self.setLayout(self.player_controls_layout)
        
    
    # ============================ # 
    #     Liaison des boutons      #
    # ============================ # 
    def _binding_signals(self):
        """
        Connecte dynamiquement les boutons aux signaux correspondants.
        """
        self.play_button.clicked.connect(self.request_play.emit)
        self.pause_button.clicked.connect(self.request_pause.emit)
        self.next_button.clicked.connect(self.request_next.emit)
        self.previous_button.clicked.connect(self.request_previous.emit)
        self.stop_button.clicked.connect(self.request_stop.emit)
        self.volume_up_button.clicked.connect(self.request_volume_up.emit)
        self.volume_down_button.clicked.connect(self.request_volume_down.emit)
        self.mute_button.clicked.connect(self.request_volume_mute.emit)
        
    
    # ============================ # 
    #     Méthodes publiques       #
    # ============================ # 
    def set_track(self, track):
        """Met à jour le titre de la piste affiché."""
        # Si tu as un QLabel pour le titre, tu le mets ici
        if hasattr(self, "track_label"):
            self.track_label.setText(track.title if track else "")

    def set_state(self, state):
        """Met à jour les icônes Play/Pause selon l'état."""
        self.update_play_pause_icon(state)

    def set_volume(self, volume: float):
        """Met à jour le slider de volume (0.0 à 1.0)."""
        if hasattr(self, "volume_slider"):
            self.volume_slider.setValue(int(volume * 100))