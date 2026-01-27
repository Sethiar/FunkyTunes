# app/UI/screens/window_services/playlist_panel.py

from typing import List, Optional, Dict

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QAbstractItemView, 
    QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, Signal, QModelIndex, QSortFilterProxyModel

from app.UI.atoms.buttons import AppButton
from app.UI.atoms.library.library_display import TracksTableView
from app.view_models.model_tracks import TracksTableModel
from app.UI.screens.window_services.create_playlist_dialog import CreatePlaylistDialog

from core.entities.track import Track

from core.logger import logger


class PlaylistPanel(QWidget):
    """
    Panel principal pour gérer la bibliothèque et les playlists.

    - Affiche la table principale des pistes
    - Conteneur dynamique pour les vues contextuelles (tri par album, artiste, favoris…)
    - Boutons pour créer / réinitialiser / revenir
    """
    
    # =========================== #
    #           Signaux           #
    # =========================== #
    request_new_playlist = Signal()
    request_back_to_library = Signal()
    request_reinitialized = Signal()
    track_selected = Signal(Track)
    
    
    # =========================== #
    #       Initialisation        #
    # =========================== #
    def __init__(self, parent: Optional[QWidget] = None):
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

        self.current_playlist_label = QLabel("Playlist : Aucune")
        self.new_playlist_btn = AppButton("Créer une nouvelle playlist")
        self.delete_playlist_btn = AppButton("Supprimer playlist")
        self.back_btn = AppButton("Retour à la bibliothèque")
        self.reset_view_btn = AppButton("Réinitialiser l’affichage")


        # Container pour les vues dynamiques
        self.dynamic_container_widget = QWidget()
        self.dynamic_container_layout = QVBoxLayout(self.dynamic_container_widget)
        self.dynamic_container_layout.setContentsMargins(0, 0, 0, 0)
        self.dynamic_container_layout.setSpacing(10)
        self.dynamic_container_widget.hide()

        # Stockage des vues dynamiques
        self.dynamic_views: Dict[str, QWidget] = {}
        self.current_dynamic_view: Optional[QWidget] = None
        
        # Liste des playlists
        self.playlists_list = QListWidget()
        self.playlists_list.setSelectionMode(QListWidget.SingleSelection)
        self.playlists_list.setDragDropMode(QListWidget.InternalMove)

        # Formulaire de création
        self.create_playlist_form = CreatePlaylistDialog(parent=self)
        self.create_playlist_form.setVisible(False)


        # ========================= #
        #      Layout principal     #
        # ========================= #
        self._build_ui()
        self._connect_signals()


    # =========================== #
    #       Construction UI       #
    # =========================== #
    def _build_ui(self):
        """Assemble tous les widgets dans le layout principal."""
        self.main_layout = QVBoxLayout(self)

        # Section bibliothèque
        self.main_layout.addWidget(QLabel("Bibliothèque des pistes de lecture"))
        self.main_layout.addWidget(self.tracks_table_view)
        self.main_layout.addWidget(self.dynamic_container_widget)

        # Section playlists
        self.main_layout.addWidget(QLabel("Vos playlists"))
        self.main_layout.addWidget(self.playlists_list)
        self.main_layout.addWidget(self.current_playlist_label)

        # Boutons de contrôle
        self.main_layout.addWidget(self.new_playlist_btn)
        self.main_layout.addWidget(self.delete_playlist_btn)
        self.main_layout.addWidget(self.reset_view_btn)
        self.main_layout.addWidget(self.back_btn)


    # =========================== #
    #    Connexion des signaux    #
    # =========================== #
    def _connect_signals(self):
        """Connecte les signaux Qt internes aux méthodes publiques."""
        self.new_playlist_btn.clicked.connect(self.request_new_playlist.emit)
        self.delete_playlist_btn.clicked.connect(self.delete_selected_playlist)
        self.back_btn.clicked.connect(self.request_back_to_library.emit)
        self.tracks_table_view.clicked.connect(self._on_track_clicked)
        self.reset_view_btn.clicked.connect(self.show_tracks_table)


    # =========================== #
    #      Méthodes publiques     #
    # =========================== #
    def display_tracks(self, tracks: List[Track]) -> None:
        """Met à jour la table avec une nouvelle liste de pistes."""
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
        """Réinitialise les filtres et le tri de la table."""
        self.tracks_proxy_model.setFilterRegularExpression("")
        self.tracks_proxy_model.sort(-1)
        if self.tracks_proxy_model.rowCount() > 0:
            self.tracks_table_view.selectRow(0)
            self.tracks_table_view.scrollToTop()        


    # =========================== #
    #     Slots internes          #
    # =========================== #
    def _on_track_clicked(self, index: QModelIndex) -> None:
        """Slot déclenché lorsqu'une piste est sélectionnée dans la table."""
        source_index = self.tracks_proxy_model.mapToSource(index)
        track: Optional[Track] = self.tracks_model.data(source_index, role=Qt.UserRole)
        if track:
            self.track_selected.emit(track)


    # =========================== #
    #   Dynamic view handling     #
    # =========================== #
    def replace_main_view(self, view_name: str, widget: QWidget):
        """
        Affiche un widget contextuel dans le container dynamique.

        Args:
            view_name (str): clé unique pour réutiliser le widget
            widget (QWidget): widget à afficher
        """
        self.tracks_table_view.hide()
        self.dynamic_container_widget.show()

        if view_name in self.dynamic_views:
            if self.current_dynamic_view:
                self.current_dynamic_view.hide()
            self.current_dynamic_view = self.dynamic_views[view_name]
            self.current_dynamic_view.show()
            return

        # Ajout et affichage le nouveau widget
        self.dynamic_container_layout.addWidget(widget)
        self.dynamic_views[view_name] = widget
        if self.current_dynamic_view:
            self.current_dynamic_view.hide()
        self.current_dynamic_view = widget
        self.current_dynamic_view.show()


    # =========================== #
    #    Gestion des playlists    #
    # =========================== #
    def open_create_playlist_form(self):
        logger.info("PlaylistPanel : Bouton 'Créer nouvelle playlist' cliqué")
        self.replace_main_view("create_playlist_form", self.create_playlist_form)
        self.request_new_playlist.emit()
    
    
    def add_playlist_to_list(self, playlist):
        """Ajoute une playlist dans le QListWidget."""
        item = QListWidgetItem(playlist.name)
        item.setData(Qt.UserRole, playlist)
        self.playlists_list.addItem(item)


    def delete_selected_playlist(self):
        """Supprime la playlist sélectionnée."""
        item = self.playlists_list.currentItem()
        if not item:
            return
        playlist = item.data(Qt.UserRole)
        session = self.parent().session_factory()
        session.delete(playlist)
        session.commit()
        session.close()
        self.playlists_list.takeItem(self.playlists_list.row(item))    
        
    