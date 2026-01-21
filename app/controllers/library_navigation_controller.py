# app/controllers/library_navigation_controller.py


from PySide6.QtCore import QObject


from app.UI.screens.home_screen import HomeScreen
from app.UI.molecules.menus.menu_library import MenuLibrary


class LibraryNavigationController(QObject):
    """
    Controller responsable de la navigation bibliothèque / playlists
    au sein du HomeScreen.
    """
    
    def __init__(self, menu_library: MenuLibrary, home_screen: HomeScreen, parent=None):
        super().__init__(parent)
        self.menu = menu_library
        self.home_screen = home_screen
        self.playlist_panel = home_screen.playlist_panel
        self._bind()
        
        
    def _bind(self):
        self.menu.requested_all_playlist.connect(self._on_playlist_requested)
        self.playlist_panel.request_back_to_library.connect(
    self._on_back_requested
)

    def _on_playlist_requested(self):
        self.home_screen.show_playlist()
        
    def _on_back_requested(self):
        self.home_screen.show_library()