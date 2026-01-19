# app/UI/atoms/search_input.py

"""
Docstring pour app.UI.atoms.search_input
"""

from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt

class SearchInput(QLineEdit):
    """
    Classe pour un champ de recherche personnalisé.
    """

    def __init__(self, placeholder: str = "Rechercher..."):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(30)
        self.setFixedWidth(300)
        # Interaction au survol
        self.setCursor(Qt.IBeamCursor)
        # Propriété personnalisée pour le style
        self.setProperty("variant", "search")