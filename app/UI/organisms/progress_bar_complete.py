# app/UI/organisms/progress_bar_complete.py

"""
Barre de progression complète pour l'interface utilisateur.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, Signal

from app.UI.atoms.icons_button import IconButton
from app.UI.atoms.progress_bar import ProgressBar

class ProgressBarComplete(QWidget):
    """
    Widget de barre de progression complète avec bouton d'annulation.

    Signaux :
        cancel_requested : émis quand l'utilisateur clique sur le bouton Annuler

    Composants :
        icons_button : bouton d'annulation
        progress_bar  : barre de progression standard
    """
    
    # ============== #
    #    Signaux     #
    # ============== #
    
    cancel_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self.setProperty("component", "progress-bar-complete")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setMinimumWidth(200)
        
        self.progress_bar_complete_layout = QVBoxLayout()
        self.progress_bar_complete_layout.setSpacing(5)
        self.progress_bar_complete_layout.setContentsMargins(8, 8, 8, 8)
        
        # Bouton d'annulation
        self.icons_button = IconButton("stop_2", tooltip="Annuler")
         # Connexion du bouton Stop
        self.icons_button.clicked.connect(self.cancel_requested.emit)
        # Ajouter et aligner le bouton à droite
        self.progress_bar_complete_layout.addWidget(self.icons_button, alignment=Qt.AlignRight)
        
        # Barre de progression
        self.progress_bar = ProgressBar()
 
        # Ajouter la barre de progression au layout
        self.progress_bar_complete_layout.addWidget(self.progress_bar)

       
        
        # Définir le layout principal
        self.setLayout(self.progress_bar_complete_layout)
        
        