# app/UI/screens/home_screen.py

"""
Fenêtre principale de l'application utilisant PySide6.
    - Affichage du menu principal.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
)
from PySide6.QtCore import Qt, Signal

from app.UI.atoms.search_input import SearchInput

from app.UI.molecules.menus.menu_principal import MenuPrincipal
from app.UI.organisms.top_bar import TopBar
from app.UI.organisms.content_stack import ContentStack
from app.UI.organisms.library_display_menu import LibraryDisplayMenu

from app.UI.screens.window_services.playlist_panel import PlaylistPanel


# Classe de l'écran principal
class HomeScreen(QWidget):
    """Écran principal de FunkyTunes."""
    
    # ================================================= #
    #              Déclaration des signaux              #
    # ================================================= #
    request_import_music = Signal()
    request_export_library = Signal()
    request_open_settings = Signal()
    request_help = Signal()
    
    # ============================= #
    #   Initialisation du widget    #
    # ============================= #
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("FunkyTunes")
        self.resize(1000, 650)
        
        # Containers principaux
        self.menu = MenuPrincipal()
        # widget TopBar avec tri + player
        self.top_bar = TopBar()
        # bibliothèque + playlist
        self.content_stack = ContentStack()
        
        self.search_input = SearchInput()
        
        self._build_layout()
        self._connect_signals()
        
    
    # ================================================= #
    #             Construction par étapes               #
    # ================================================= #
    def _build_layout(self):
        """
        Construit la mise en page principale du HomeScreen.
        - Menu à gauche
        - Contenu à droite : SearchInput + TopBar + ContentStack
        """
        
        # Layout racine (menu gauche / contenu droite)
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
    
        # ===== Contenu droit (SearchInput + TopBar + ContentStack)
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(10)
    
        content_layout.addWidget(self.search_input)
        content_layout.addWidget(self.top_bar)
        content_layout.addWidget(self.content_stack)
    
        # ===== Ajout du menu gauche
        menu_container = QWidget()
        menu_layout = QVBoxLayout(menu_container)
        menu_layout.setContentsMargins(10, 10, 10, 10)
        menu_layout.addWidget(self.menu)
    
        # Assemblage final
        main_layout.addWidget(menu_container, stretch=0)
        main_layout.addWidget(content_container, stretch=1)
    
        self.setLayout(main_layout)
    
    
    # ================================================= #
    #             Déclaration des signaux               #
    # ================================================= # 
    def _connect_signals(self):
        """Connecte les signaux des composants UI aux signaux du screen."""
        
        self.menu.request_import.connect(self.request_import_music.emit)
        self.menu.request_export.connect(self.request_export_library.emit)
        self.menu.open_settings_requested.connect(self.request_open_settings.emit)
        self.menu.help_requested.connect(self.request_help.emit)
        