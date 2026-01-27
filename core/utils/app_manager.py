# core/app_manager.py


from typing import Callable
from sqlalchemy.orm import Session

from app.UI.screens.home_screen import HomeScreen
from app.UI.window_manager import WindowManager

# Controllers
from app.controllers.home_screen_controller import HomeScreenController
from app.controllers.player_service_controller import PlayerServiceController
from app.controllers.playlist_controllers.playlist_controller import PlaylistController
from app.controllers.playlist_controllers.playlist_maker_controller import PlaylistMakerController
from app.controllers.library_navigation_controller import LibraryNavigationController

from app.presenter.library_presenter import LibraryPresenter


# Services
from services.file_services.library_services.library_services import LibraryServices
from services.file_services.player_services.player_services import PlayerServices
from services.file_services.playlist_services.playlist_services import PlaylistServices
from services.file_services.playlist_services.playlist_maker_services import PlaylistMakerServices

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
        logger.info("AppManager : Initialisation des composants...")
        """
        Initialise tous les composants de l'application.

        Args:
            session_factory: factory SQLAlchemy pour créer de nouvelles sessions
        """
        logger.info("AppManager : Initialisation des composants...")
        
        # Screens
        self.home_screen = HomeScreen()
        logger.info("HomeScreen initialisé")
        
        # Window Manager
        self.window_manager = WindowManager()
        logger.info("WindowManager initialisé")
        
        # Services Bibliothèque
        self.library_service = LibraryServices(session_factory)
        logger.info("LibraryServices initialisé")
        
        
        # Service Playlist
        self.playlist_service = PlaylistServices()
        logger.info("PlaylistService initialisé")

        # Services du Lecteur
        self.player_service = PlayerServices()
        logger.info("PlayerServices initialisé")


        # PlayerServices Controller
        self.player_service_controller = PlayerServiceController(
            self.home_screen.top_bar.player_controls,
            self.player_service,
            self.playlist_service
        )
        logger.info("PlayerServicesController initialisé")
        
        
        # Playlist Controller
        self.playlist_controller = PlaylistController(
            ui=self.home_screen.content_stack.playlist_panel, 
            playlist_service=self.playlist_service,
            player_service=self.player_service,
            session_factory=session_factory,
            sort_tracks_widget=self.home_screen.top_bar.sort_tracks  
        )
        logger.info("PlaylistController initialisé")
        
        
        # PlaylistMaker Controller
        self.playlist_maker_service = PlaylistMakerServices(session_factory)
        self.playlist_maker_controller =  PlaylistMakerController(
            ui=self.home_screen.content_stack.playlist_panel.create_playlist_form, 
            playlist_maker_service=self.playlist_maker_service
        )
        self.home_screen.content_stack.playlist_panel.request_new_playlist.connect(
            self.playlist_maker_controller.open_form
        )
        self.playlist_maker_controller.playlist_created.connect(
            self.home_screen.content_stack.playlist_panel.add_playlist_to_list
        )
        logger.info("PlaylistMakerController initialisé")
        
        # Presenter
        self.library_presenter = LibraryPresenter(
            self.home_screen.content_stack.library_display, 
            session_factory=session_factory
        )
        logger.info("LibraryPresenter initialisé")
        
        
        # Playlist navigation Controller
        self.library_navigation_controller = LibraryNavigationController(
            menu_library=self.home_screen.content_stack.library_display.menu_library,
            home_screen=self.home_screen,
            library_presenter=self.library_presenter 
        )
        logger.info("LibraryNavigator initialisé")
        
        
        # Controllers
        self.home_controller = HomeScreenController(
            self.home_screen,
            self.library_service,
            self.player_service,
            self.library_presenter,
            self.window_manager
        )
        logger.info("HomeScreenController initialisé")


    def run(self):
        """Affiche l'écran principal et lance l'application."""
        logger.info("AppManager : Lancement du HomeScreen...")
        self.home_screen.show()
