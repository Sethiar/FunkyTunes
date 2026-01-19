# app/UI/organisms/library_display_menu.py

"""
Menu d'affichage de la bibliothèque musicale de l'application FunkyTunes.
"""

from PySide6.QtWidgets import QWidget, QFrame,  QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QSortFilterProxyModel

from app.UI.molecules.menus.menu_library import MenuLibrary
from app.UI.atoms.library.library_display import TracksTableView


class LibraryDisplayMenu(QWidget):
    """
    Menu d'affichage de la bibliothèque musicale vertical de l'application.
    """
    
    def __init__(self):
        super().__init__()
        
        self.tracks_table_model = None
        self.tracks_proxy_model = None
        
        self.setProperty("component", "library-display-menu")
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.library_display_menu_layout = QHBoxLayout()
        self.library_display_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.library_display_menu_layout.setSpacing(0)
        
        # Menu latéral bibliothèque
        self.menu_library = MenuLibrary()
        
        # Conteneur tracks
        self.tracks_container = QFrame()
        self.tracks_container.setObjectName("tracksContainer")
        self.tracks_container.setFrameShape(QFrame.StyledPanel)
        
        self.tracks_layout = QVBoxLayout(self.tracks_container)
        self.tracks_layout.setContentsMargins(0, 0, 0, 0)     
        
        # Vue des tracks
        self.tracks_view = TracksTableView()
        self.tracks_layout.addWidget(self.tracks_view)

        # Assemblage
        self.library_display_menu_layout.addWidget(self.menu_library)
        self.library_display_menu_layout.addWidget(self.tracks_container, stretch=1)
        
        self.setLayout(self.library_display_menu_layout)
        
    
    # --- API publique pour le Presenter ---
    def set_tracks_model(self, model):
        """
        Injecte le modèle Qt dans la vue via un proxy pour filtrage.
        """
        
        self.tracks_table_model = model
        
        self.tracks_proxy_model = QSortFilterProxyModel()
        self.tracks_proxy_model.setSourceModel(model)
        self.tracks_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.tracks_proxy_model.setFilterKeyColumn(2)  # filtrer sur colonne Artiste

        self.tracks_view.setModel(self.tracks_proxy_model)
        