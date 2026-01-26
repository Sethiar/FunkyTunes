# run.py


"""
Point d'entrée principal de l'application Funkytunes.

Rôle :
- Initialiser la base de données et la session SQLAlchemy.
- Créer l'application Qt et appliquer le style.
- Lancer le AppManager qui orchestre l'application.
- Démarrer la boucle principale Qt.

Auteur : Arnaud
"""

import sys


from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from core.utils.app_manager import AppManager
from core.utils.style_manager import StyleManager

from core.logger import logger

from database.engine import SessionLocal
from database.init_db import init_db


def main():
    """
    Fonction principale : initialise l'environnement et lance l'application.

    Étapes :
    1. Initialisation de la base de données
    2. Création de la session SQLAlchemy
    3. Création et configuration de QApplication
    4. Chargement de la feuille de style
    5. Instanciation et lancement du AppManager
    6. Démarrage de la boucle Qt principale
    """
    try:
        # ========================= #
        #   Initialisation DB       #
        # ========================= #
        logger.info("Initialisation de la base de données...")
        init_db()


        # ============================== #
        #   Création de l'application Qt #
        # ============================== #
        logger.info("Création de l'application Qt...")
        app = QApplication(sys.argv)

        # Application de la feuille de style globale
        StyleManager.load_stylesheet(app)
        
        # Icône globale
        app.setWindowIcon(QIcon("app/resources/icons/app_icon.ico"))


        # ========================= #
        #   Manager de l'application
        # ========================= #
        logger.info("Initialisation du manager de l'application...")
        manager = AppManager(session_factory=SessionLocal)
        manager.run()


        # ========================= #
        #   Boucle principale Qt
        # ========================= #
        logger.info("Lancement de la boucle principale Qt...")
        sys.exit(app.exec())

    except Exception as e:
        # Gestion globale des erreurs
        logger.critical(f"Une erreur critique est survenue : {e}", exc_info=True)
        sys.exit(1)


# Lancement si exécuté directement
if __name__ == "__main__":
    main()