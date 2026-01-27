# app/controllers/library_navigation_controller.py


from PySide6.QtCore import QObject

from app.UI.screens.home_screen import HomeScreen
from app.UI.molecules.menus.menu_library import MenuLibrary
from app.presenter.library_presenter import LibraryPresenter

from core.logger import logger


class LibraryNavigationController(QObject):
    """
    Controller responsable de la navigation entre la bibliothèque et les playlists.
    
    Rôle :
        - Écouter les signaux de l'UI (menu, bouton retour)
        - Demander au presenter les données nécessaires
        - Mettre à jour l'UI en conséquence
    """
    
    def __init__(
        self,
        menu_library: MenuLibrary,
        home_screen: HomeScreen,
        library_presenter: LibraryPresenter,
        parent=None
    ) -> None:
        """
        Docstring pour __init__

        :param menu_library: Description
        :type menu_library: MenuLibrary
        :param home_screen: Description
        :type home_screen: HomeScreen
        :param library_presenter: Description
        :type library_presenter: LibraryPresenter
        :param parent: Description
        """
        super().__init__(parent)
        self.menu = menu_library
        self.home_screen = home_screen
        self.playlist_panel = home_screen.content_stack.playlist_panel
        self.library_presenter = library_presenter
        
        self._bind_signals()

    
    # ========================= #
    #      Binding signaux      #
    # ========================= #
    def _bind_signals(self):
        """Connecte les signaux du menu et du panel aux méthodes du controller."""
        self.menu.requested_all_playlist.connect(self._on_playlist_requested)
        self.playlist_panel.request_back_to_library.connect(
            self._on_back_requested
        )    
    
    
    # ========================= #
    #   Slots                   #
    # ========================= #
    def _on_playlist_requested(self):
        """Affiche les playlists et leurs pistes."""
        logger.info("Affichage Playlist demandée")
        self.home_screen.content_stack.show_playlist()
        # Récupère les pistes via le presenter
        tracks = self.library_presenter.refresh_tracks()
        # Affiche les pistes sur le panel
        self.playlist_panel.display_tracks(tracks)
          
        
    def _on_back_requested(self):
        """Retour à la bibliothèque principale."""
        logger.info("Retour bibliothèque")
        self.home_screen.content_stack.show_library()
        
        