# app/UI/atoms/ProgressBar.py

"""
Barre de progression personnalisée pour l'interface utilisateur.
"""

from PySide6.QtWidgets import QProgressBar
from PySide6.QtCore import Qt

class ProgressBar(QProgressBar):
    """
    Classe pour une barre de progression personnalisée de l'application.
    """
    
    def __init__(self):
        super().__init__()
        self.setProperty("component", "progress-bar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setMinimumHeight(10)
        self.setTextVisible(False)
        self.setRange(0, 100)
        self.setValue(0)
        
    def set_progress(self, value: int):
        """
        Met à jour la valeur de la barre de progression.
        
        Args:
            value (int): La nouvelle valeur de progression (0-100).
        """
        if 0 <= value <= 100:
            self.setValue(value)
        else:
            raise ValueError("La valeur de progression doit être comprise entre 0 et 100.")
        
        
        