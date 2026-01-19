# core/icon_loader.py

"""
Fichier pour charger et gérer les icônes de l'application.
"""
from PySide6.QtGui import QIcon

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ICONS_DIR = BASE_DIR / "resources" / "icons"


def load_icon(name: str):
    """
    Charge une icône à partir du répertoire des ressources.
    
    Args:
        name (str): Le nom de l'icône à charger (sans extension).
        
    Returns:
        QIcon: L'icône chargée.
    """
    return QIcon(str(ICONS_DIR / f"{name}.svg"))