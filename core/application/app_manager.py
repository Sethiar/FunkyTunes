# core/app_manager.py


from typing import Callable
from sqlalchemy.orm import Session

from app.UI.screens.home_screen import HomeScreen

# Controllers
from app.controllers.home_screen_controller import HomeScreenController
from app.controllers.player_service_controller import PlayerServiceController
from app.controllers.playlist_controller import PlaylistController
from app.controllers.library_navigation_controller import LibraryNavigationController

from app.presenter.library_presenter import LibraryPresenter

# Services
from services.file_services.library_services.library_services import LibraryServices
from services.file_services.player_services.player_services import PlayerServices
from services.file_services.playlist_services.playlist_services import PlaylistServices


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
        
        # Service Playlist
        self.playlist_service = PlaylistServices()
        logger.info("PlaylistService initialisé")

        # Services du Lecteur
        self.player_service = PlayerServices()
        logger.info("PlayerServices initialisé")


        # PlayerServices Controller
        self.player_service_controller = PlayerServiceController(
            self.home_screen.player_controls,
            self.player_service,
            self.playlist_service
        )
        logger.info("PlayerServicesController initialisé")
        
        # Playlist Controller
        self.playlist_controller = PlaylistController(
            ui=self.home_screen.playlist_panel, 
            playlist_service=self.playlist_service,
            player_service=self.player_service,
            library_service=self.library_service,
            sort_tracks_widget=self.home_screen.sort_tracks  
        )
        logger.info("PlaylistController initialisé")
        
        
        # Playlist navigation Controller
        self.library_navigation_controller = LibraryNavigationController(
            menu_library=self.home_screen.library_display.menu_library,
            home_screen=self.home_screen
        )
        logger.info("LibraryNavigator initialisé")
        
        
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
