# core/style_manager.py


"""
Docstring pour core.style_manager
"""

from pathlib import Path


class StyleManager:
    """
    Classe pour gérer les styles de l'application.
    """

    @staticmethod
    def load_stylesheet(app, style_dirs=None) -> str:
        """
        Charge tous les fichiers QSS et les applique à l'application.

        :param app: QApplication
        :param style_dirs: liste de dossiers à parcourir pour les fichiers QSS
        """
        # Récupération du dossier de styles
        base_dir = Path(__file__).parent/"styles"
        
        # Dossiers à parcourir si non fourni
        if style_dirs is None:
            style_dirs = ["", "atomic", "molecules", "organisms"]
        
        
        full_qss = ""
        
        for folder in style_dirs:
            folder_path = base_dir / folder
            if folder_path.exists() and folder_path.is_dir():
                # Trouver tous les fichiers .qss dans le dossier
                qss_files = sorted(folder_path.glob("*.qss"))
                for qss_file in qss_files:
                    full_qss += qss_file.read_text(encoding="utf-8") + "\n"
        
        # Appliquer tout le QSS concaténé        
        app.setStyleSheet(full_qss)
        
        