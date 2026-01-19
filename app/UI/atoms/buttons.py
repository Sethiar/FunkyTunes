# app/ui/atoms/buttons.py

"""
Fichier qui crée des boutons pour l'interface utilisateur.
"""

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt




class AppButton(QPushButton):
    """
    Classe pour un bouton personnalisé de l'application.
    """
    
    def __init__(self, label: str, variant: str = "default"):
        super().__init__(label)
        self.setFixedSize(200, 50)
        # interaction au survol
        self.setCursor(Qt.PointingHandCursor)
        # Variant du bouton (style)
        self.setProperty("menu", variant)