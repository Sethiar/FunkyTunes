# app/UI/screens/window_services/playlist_panel.py


from typing import List, Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QAbstractItemView
)
from PySide6.QtCore import Qt, Signal, QSortFilterProxyModel, QModelIndex

from app.UI.atoms.buttons import AppButton
from app.UI.molecules.menus.menu_playlist import PlaylistMenu
from app.UI.atoms.library.library_display import TracksTableView
from app.view_models.model_tracks import TracksTableModel

from core.entities.track import Track


class PlaylistPanel(QWidget):
    """
    Panel principal pour gérer la bibliothèque et les playlists.

    - Affiche la table principale des pistes
    - Permet d’afficher dynamiquement des vues contextuelles
      (tri par artiste, album, genre, favoris…)
    - La table principale reste toujours disponible
    """
    
    # =========================== #
    #           Signaux           #
    # =========================== #
    request_back_to_library = Signal()
    request_reinitialized = Signal()
    track_selected = Signal(Track)
    
    
    # =========================== #
    #       Initialisation        #
    # =========================== #
    def __init__(self, parent=None):
        """
        Initialise le panneau de gestion des playlists.

        Args:
            parent (QWidget | None): widget parent Qt
        """
        super().__init__(parent)
        self.setWindowTitle("Gestion des playlists")
        self.setMinimumSize(900, 600)


        # ========================= #
        #      Models & Proxy       #
        # ========================= #
        self.tracks_model = TracksTableModel([])
        self.tracks_proxy_model = QSortFilterProxyModel()
        self.tracks_proxy_model.setSourceModel(self.tracks_model)
        self.tracks_proxy_model.setSortRole(Qt.DisplayRole)
        self.tracks_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        
        
        # ========================= #
        #         Widgets           #
        # ========================= #
        self.tracks_table_view = TracksTableView()
        self.tracks_table_view.setModel(self.tracks_proxy_model)
        self.tracks_table_view.setSortingEnabled(True)
        self.tracks_table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tracks_table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        
        
        # ========================= #
        #          Controls         #
        # ========================= #
        self.playlist_menu= PlaylistMenu()
        self.back_btn = AppButton("Retour à la bibliothèque")
        self.reset_view_btn = AppButton("Réinitialiser l’affichage")
        
        
        # ======================= #
        #          View           #
        # ======================= #
        self._build_ui()
        self._connect_signals()
        
        
        # ======================= #
        #  Vues dynamiques cache  #
        # ======================= #
        # Stockage des vues créées
        self.dynamic_views: dict[str, QWidget] = {}
        self.current_dynamic_view: Optional[QWidget] = None
        
        
    # =========================== #
    #    Construction de l'UI     #
    # =========================== #
    def _build_ui(self):
        """
        Construit le layout principal du panneau.

        Le layout est volontairement segmenté afin de faciliter
        l'évolution de l'interface (ajout de sections, vues dynamiques).
        """
        
        # Layout principal vertical
        self.main_layout = QVBoxLayout(self)
        
        # Construction
        self._build_library_section()
        self._build_dynamic_container()
        self._build_playlist_section()
        self._build_controls()


    def _build_library_section(self):
        """
        Construit la section principale d'affichage des pistes musicales.
        """
        # Section bibliothèque
        self.main_layout.addWidget(QLabel("Bibliothèque des pistes de lecture"))
        self.main_layout.addWidget(self.tracks_table_view)
        
        
    def _build_playlist_section(self):
        """
        Construit la section des contrôles utilisateur :
            - réinitialisation de l'affichage
            - retour à la bibliothèque
            - menu de gestion des playlists
        """
        # Section playlist
        self.main_layout.addWidget(QLabel("Pistes de la playlist"))
        
        
    def _build_controls(self):
        """
        Construit la section des contrôles utilisateur :
            - réinitialisation de l'affichage
            - retour à la bibliothèque
            - menu de gestion des playlists
        """
        # Menu + bouton retour
        self.main_layout.addWidget(self.reset_view_btn)
        self.main_layout.addWidget(self.back_btn)
        self.main_layout.addWidget(self.playlist_menu)

    
    def _build_dynamic_container(self):
        """Crée le container invisible pour les vues dynamiques."""
        self.dynamic_container_widget = QWidget()
        self.dynamic_container_layout = QVBoxLayout(self.dynamic_container_widget)
        self.dynamic_container_layout.setContentsMargins(0, 0, 0, 0)
        self.dynamic_container_layout.setSpacing(10)
        self.dynamic_container_widget.hide()  # cache au départ

        # insérer juste après la table
        index = self.main_layout.indexOf(self.tracks_table_view)
        self.main_layout.insertWidget(index + 1, self.dynamic_container_widget)
        
        
    # =========================== #
    #       Connexion signaux     #
    # =========================== #
    def _connect_signals(self):
        """
        Connecte les signaux Qt internes aux méthodes de la vue
        ou aux signaux exposés vers le controller.
        """
        self.back_btn.clicked.connect(self.request_back_to_library.emit)
        self.tracks_table_view.clicked.connect(self._on_track_clicked)
        self.reset_view_btn.clicked.connect(self.show_tracks_table)


    # =========================== #
    #      Méthodes publiques     #
    # =========================== #
    def display_tracks(self, tracks: List[Track]) -> None:
        """
        Met à jour la table avec une nouvelle liste de pistes.

        Cette méthode constitue le point d'entrée principal du controller
        pour rafraîchir l'affichage.

        Args:
            tracks (List[Track]): liste des pistes à afficher
        """
        self.tracks_model.set_tracks(tracks)
        self.show_tracks_table()
    
    def show_tracks_table(self):
        """Affiche la table principale et cache la vue dynamique."""
        if self.current_dynamic_view:
            self.current_dynamic_view.hide()
        self.dynamic_container_widget.hide()
        self.tracks_table_view.show()
        self.reset_table_view()
        self.request_reinitialized.emit()
    
    
    def reset_table_view(self) -> None:
        self.tracks_proxy_model.setFilterRegularExpression("")
        self.tracks_proxy_model.sort(-1)
        if self.tracks_proxy_model.rowCount() > 0:
            self.tracks_table_view.selectRow(0)
            self.tracks_table_view.scrollToTop()
            
            
    # =========================== #
    #       Slots internes        #
    # =========================== #
    def _on_track_clicked(self, index: QModelIndex) -> None:
        """
        Slot déclenché lorsqu'une piste est sélectionnée dans la table.

        La piste est récupérée via le modèle (Qt.UserRole) afin de
        ne pas dépendre de l'implémentation interne du model.

        Args:
            index (QModelIndex): index cliqué dans le proxy model
        """
        source_index = self.tracks_proxy_model.mapToSource(index)
        track: Optional[Track] = self.tracks_model.data(
            source_index, role=Qt.UserRole
        )

        if track:
            self.track_selected.emit(track)
        
    
    # =========================== #
    #     Dynamic view handling   #
    # =========================== #  
    def replace_main_view(self, view_name: str, widget: QWidget):
        """
        Affiche un widget contextuel dans le container dynamique.
        Le widget principal (tracks_table_view) est caché, jamais supprimé.

        Args:
            view_name (str): clé unique pour réutiliser le widget
            widget (QWidget): widget à afficher
        """
        # cacher la table
        self.tracks_table_view.hide()
        self.dynamic_container_widget.show()

        # si la vue existe déjà, on la réutilise
        if view_name in self.dynamic_views:
            if self.current_dynamic_view:
                self.current_dynamic_view.hide()
            self.current_dynamic_view = self.dynamic_views[view_name]
            self.current_dynamic_view.show()
            return

        # Ajout et affichage du nouveau widget
        self.dynamic_container_layout.addWidget(widget)
        self.dynamic_views[view_name] = widget
        if self.current_dynamic_view:
            self.current_dynamic_view.hide()
        
        self.current_dynamic_view = widget
        self.current_dynamic_view.show()
        
        