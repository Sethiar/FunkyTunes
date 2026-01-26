 # app/UI/organisms/top_bar.py
 
from PySide6.QtWidgets import QWidget, QHBoxLayout

from PySide6.QtCore import Qt

from app.UI.molecules.sort_tracks import SortTracks
from app.controllers.player_service_controller import PlayerControls


class TopBar(QWidget):
    def __init__(self):
        super().__init__()
        
        self.sort_tracks = SortTracks()
        self.player_controls = PlayerControls()
        
        layout = QHBoxLayout()
       
        layout.addWidget(self.sort_tracks, alignment=Qt.AlignLeft)
        layout.addWidget(self.player_controls, alignment=Qt.AlignRight)
        
        self.setLayout(layout)
        
        
        