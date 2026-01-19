# core/app_manager.py


from typing import Callable
from sqlalchemy.orm import Session

from app.UI.screens.home_screen import HomeScreen
from app.controllers.home_screen_controller import HomeScreenController
from services.file_services.library_services.library_services import LibraryServices
from app.presenter.library_presenter import LibraryPresenter
from services.file_services.player_services.player_services import PlayerServices
from app.controllers.player_service_controller import PlayerServiceController

from core.logger import logger

class AppManager:
    """
    Manager principal de l'application FunkyTunes.

    Rôle :
        - Instancier les services, écrans et controllers.
        - Orchestrer l'affichage des screens.
        - Assurer le passage des dépendances.
    """
    
    def __init__(self, session_factory: Callable[[], "Session"]) -> None:
        """
        Initialise tous les composants de l'application.

        Args:
            session_factory: factory SQLAlchemy pour créer de nouvelles sessions
        """
        logger.info("AppManager : Initialisation des composants...")
        
        # Screens
        self.home_screen = HomeScreen()
        logger.info("HomeScreen initialisé")
        
        # Services Bibliothèque
        self.library_service = LibraryServices(session_factory())
        logger.info("LibraryServices initialisé")
        
        
        # Services du Lecteur
        self.player_service = PlayerServices()
        logger.info("PlayerServices initialisé")

        # PlayerServices Controller
        self.player_service_controller = PlayerServiceController(
            self.home_screen.player_controls,
            self.player_service
        )
        logger.info("PlayerServicesController initialisé")
        
        # ===============================
        # Chargement de la playlist
        # ===============================
        tracks_paths = self.library_service.get_track_file_paths()
        logger.info(f"{len(tracks_paths)} pistes récupérées depuis la bibliothèque")
        self.player_service_controller.load_playlist(tracks_paths)
        
        # Presenter
        self.library_presenter = LibraryPresenter(
            self.home_screen.library_display, 
            session_factory
        )
        logger.info("LibraryPresenter initialisé")
        
        # Controllers
        self.home_controller = HomeScreenController(
            self.home_screen,
            self.library_service,
            self.player_service,
            self.library_presenter
        )
        logger.info("HomeScreenController initialisé")


    def run(self):
        """Affiche l'écran principal et lance l'application."""
        logger.info("AppManager : Lancement du HomeScreen...")
        self.home_screen.show()
