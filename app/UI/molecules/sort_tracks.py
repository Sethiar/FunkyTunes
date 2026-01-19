# app/UI/molecules/sort_tracks.py

"""
Composant pour trier les pistes dans l'interface utilisateur.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout
from app.UI.atoms.buttons import AppButton


class SortTracks(QWidget):
    """
    Composant pour trier les pistes par différents critères.
    """
    
    def __init__(self):
        super().__init__()
        self.sort_tracks_layout = QHBoxLayout()
        self.sort_tracks_layout.setSpacing(10)
        
        self.button_sort = [
            AppButton("Trier par artiste", variant="sort_menu"),
            AppButton("Trier par album", variant="sort_menu"),
            AppButton("Trier par genre", variant="sort_menu"),
            AppButton("Favoris", variant="sort_menu")
        ]

        for button in self.button_sort:
            self.sort_tracks_layout.addWidget(button)
        
        self.sort_tracks_layout.addStretch(1)
        self.setLayout(self.sort_tracks_layout)
        
        