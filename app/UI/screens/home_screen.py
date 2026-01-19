# app/UI/screens/home_screen.py

"""
Fenêtre principale de l'application utilisant PySide6.
    - Affichage du menu principal.
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)
from PySide6.QtCore import Qt, Signal

from app.UI.atoms.search_input import SearchInput

from app.UI.molecules.menus.menu_principal import MenuPrincipal
from app.UI.molecules.player_controls import PlayerControls
from app.UI.molecules.sort_tracks import SortTracks

from app.UI.organisms.library_display_menu import LibraryDisplayMenu
from app.UI.molecules.playlist_panel import PlaylistPanel


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
    
    # ================================================= #
    #              Initialisation du widget             #
    # ================================================= #
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("FunkyTunes")
        self.resize(1000, 650)
        
        self._build_ui()
        self._connect_signals()
        
        
    # ================================================= #
    #              Construction de l'UI                 #
    # ================================================= #
    def _build_ui(self):
        """Construit l'interface utilisateur de l'écran principal."""
            
        # ===== Layout racine (menu gauche / contenu droite)
        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # ===== Menu gauche
        self.menu_container = QWidget()
        self.menu_layout = QVBoxLayout(self.menu_container)
        self.menu_layout.setContentsMargins(10, 10, 10, 10)
        
        # Menu principal
        self.menu = MenuPrincipal()
        self.menu_layout.addWidget(self.menu)
        
        # ===== Contenu droit
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(15, 15, 15, 15)
        self.content_layout.setSpacing(15)
        
        # Barre de recherche
        self.search_input = SearchInput()
        self.content_layout.addWidget(self.search_input)
        
        # ===== Zone de contenu principale
        self.inner_widget = QWidget()
        self.inner_layout = QVBoxLayout(self.inner_widget)
        self.inner_layout.setContentsMargins(0, 0, 0, 0)
        self.inner_layout.setSpacing(10)
        self.inner_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # Contrôles de tri + Contrôles du lecteur
        self.sort_controls = QHBoxLayout()
        self.sort_controls.setContentsMargins(0, 0, 0, 0)
        self.sort_controls.setSpacing(10)
        
        # Tri de la bibliothèque
        self.sort_tracks = SortTracks()
        
        # Contrôles du lecteur
        self.player_controls = PlayerControls()
        
        # Ajout des deux composants au layout horizontal
        self.sort_controls.addWidget(self.sort_tracks, alignment=Qt.AlignLeft)
        self.sort_controls.addWidget(self.player_controls, alignment=Qt.AlignRight)
        
        self.inner_layout.addLayout(self.sort_controls)
        
        # ===== Zone principale d'affichage (menu bibliothèque + pistes)
        # ===== Zone principale d'affichage (playlist + bibliothèque)
        self.main_content = QWidget()
        self.main_content_layout = QHBoxLayout(self.main_content)
        self.main_content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_content_layout.setSpacing(10)

        # Playlist panel
        self.playlist_panel = PlaylistPanel()
        self.main_content_layout.addWidget(self.playlist_panel, stretch=0)

        # Bibliothèque
        self.library_display = LibraryDisplayMenu()
        self.main_content_layout.addWidget(self.library_display, stretch=1)

        # Ajout au layout interne
        self.inner_layout.addWidget(self.main_content)
        
        # Ajout du layout interne au layout de contenu
        self.content_layout.addWidget(self.inner_widget)

        # ===== Assemblage des deux parties dans le layout principal
        self.main_layout.addWidget(self.menu_container, stretch=0)
        self.main_layout.addWidget(self.content_container, stretch=1)

        # Définition de la mise en page principale
        self.setLayout(self.main_layout)
    
    
    # ================================================= #
    #             Déclaration des signaux               #
    # ================================================= # 
    def _connect_signals(self):
        """Connecte les signaux des composants UI aux signaux du screen."""
        
        self.menu.request_import.connect(self.request_import_music.emit)
        self.menu.request_export.connect(self.request_export_library.emit)
        self.menu.open_settings_requested.connect(self.request_open_settings.emit)
        self.menu.help_requested.connect(self.request_help.emit)

        
        