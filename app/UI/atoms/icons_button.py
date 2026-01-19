# app/UI/atoms/icons_button.py

"""
Fichier qui crée des boutons avec icônes pour l'interface utilisateur.
"""

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
from core.icon_loader import load_icon


class IconButton(QPushButton):
    """
    Classe pour un bouton avec icône personnalisé de l'application.
    """

    def __init__(self, icon_name: str, tooltip: str = "", size: int = 20):
        super().__init__()
        self.setFixedSize(size, size)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(tooltip)
        
        icon = load_icon(icon_name)
        self.setIcon(icon)
        self.setIconSize(self.size())
        
        self.setProperty("variant", "icon-button")
        
        
class IconButton_2(QPushButton):
    """
    Classe 2 pour Icône dans écran.
    """
    def __init__(self, icon_name: str, tooltip: str = "", size: int = 100):
        super().__init__()
        self.setFixedSize(size, size)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(tooltip)
        
        icon = load_icon(icon_name)
        self.setIcon(icon)
        self.setIconSize(self.size())
        
        self.setProperty("variant", "icon-button-2")
        
        