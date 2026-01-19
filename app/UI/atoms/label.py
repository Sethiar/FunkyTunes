# app/UI/atoms/label.py


"""
Fichier qui définit un label personnalisé pour l'interface utilisateur.
"""

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class Label(QLabel):
    """
    Classe pour un label personnalisé de l'application.
    """
    
    def __init__(self, text=""):
        super().__init__(text)
        self.setProperty("component", "label")
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        