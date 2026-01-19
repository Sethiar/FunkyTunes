# app/controllers/homescreen_controller.py


from typing import Optional, List

from app.UI.screens.window_services.import_source_dialog import ImportSourceDialog
from app.controllers.import_source_controller import ImportSourceController

from core.logger import logger


class HomeScreenController:
    """
    Contrôleur principal du HomeScreen.

    Il orchestre les actions globales de l'application :
        - import / export de musique
        - navigation vers les écrans secondaires
        - ouverture des paramètres et de l'aide
    """
    
    def __init__(self, home_screen, library_service, player_service, library_presenter) -> None:
        """
        Initialise le contrôleur du HomeScreen.

        Args:
            home_screen: Vue principale de l'application.
            library_service: Service métier de gestion de la bibliothèque musicale.
            player_service: Service de lecture audio.
            library_presenter: Presenter chargé de rafraîchir l'affichage de la bibliothèque.
        """
        
        self._view = home_screen
        self._library_service = library_service
        self._player_service = player_service
        self._library_presenter = library_presenter
        
        # Fenêtres secondaires / controllers
        self._import_dialog: Optional[ImportSourceDialog] = None
        self._import_controller: Optional[ImportSourceController] = None
        logger.info("HomeScreenController : initialisation complète")
        
        # Connexion des signaux
        self._bind_signals()
        
        
    def _bind_signals(self):
        """Connecte les signaux du screen aux méthodes du controller."""
        self._view.request_import_music.connect(self.import_music)
        self._view.request_export_library.connect(self.export_music)
        self._view.request_open_settings.connect(self.open_settings)
        self._view.request_help.connect(self.open_help)
        logger.debug("HomeScreenController : signaux connectés")
        
    
    # ============================= #
    #       Slots principaux        #    
    # ============================= #
    
    def import_music(self):
        """
        Ouvre la fenêtre de sélection du support d'import musical
        et instancie le controller associé.
        """
        if self._import_dialog and self._import_dialog.isVisible():
            logger.info("ImportScreen déjà ouverte, focus dessus")
            self._import_dialog.raise_()
            self._import_dialog.activateWindow()
            return
        
        logger.info("Ouverture de la fenêtre d'import musical")
        # Création de l'écran de sélection du type d'import
        self._import_dialog = ImportSourceDialog(parent=self._view)
        # Création des services d'import de la bibliothèque
        self._import_controller = ImportSourceController(
            dialog=self._import_dialog,
            library_service=self._library_service,
            presenter=self._library_presenter
        )
        
        # Affichage de l'écran d'import
        self._import_dialog.show()
        
    
    def export_music(self, export_list):
        """
        Lance l'export de la bibliothèque musicale.

        Args:
            export_list: Liste de pistes à exporter (peut être None).
        """
        if export_list == None:
            print("Aucune liste préétablie")
    
    
    def open_settings(self):
        """Ouvre la fenêtre des paramètres de l'application."""
        pass
    
    def open_help(self):
        """Ouvre la fenêtre d'aide de l'application."""
        pass
        
        
        
        