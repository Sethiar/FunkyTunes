# app/UI/screens/window_services/playlist_panel.py


from typing import List

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QAbstractItemView
)
from PySide6.QtCore import Qt, Signal, QSortFilterProxyModel, QModelIndex

from app.UI.atoms.buttons import AppButton
from app.UI.molecules.menus.menu_playlist import PlaylistMenu
from app.UI.molecules.sort_tracks import SortTracks
from app.UI.atoms.library.library_display import TracksTableView
from app.view_models.model_tracks import TracksTableModel
from core.entities.track import Track


class PlaylistPanel(QWidget):
    """
    Écran de gestion des playlists avec affichage multi-colonnes des pistes.

    Signaux:
        request_back_to_library: émis quand l'utilisateur souhaite revenir à la bibliothèque principale
        track_selected: émis avec une instance Track quand une piste est sélectionnée dans la table
    """

    # =========================== #
    #           Signaux           #
    # =========================== #
    request_back_to_library = Signal()
    track_selected: Signal = Signal(Track)
    
    # =========================== #
    #       Initialisation        #
    # =========================== #
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestion des playlists")
        self.setMinimumSize(900, 600)

        # ========================= #
        #   Widgets & Models       #
        # ========================= #
        self.tracks_model = TracksTableModel([])
        self.tracks_proxy_model = QSortFilterProxyModel()
        self.tracks_proxy_model.setSourceModel(self.tracks_model)
        self.tracks_proxy_model.setSortRole(Qt.DisplayRole)
        self.tracks_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.tracks_table_view: TracksTableView = TracksTableView()
        self.tracks_table_view.setModel(self.tracks_proxy_model)
        self.tracks_table_view.setSortingEnabled(True)
        self.tracks_table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tracks_table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        
        
        self.playlist_menu: PlaylistMenu = PlaylistMenu()
        self.back_btn: AppButton = AppButton("Retour à la bibliothèque")
        
        
        # ======================= #
        #          View           #
        # ======================= #
        self._build_ui()
        self._connect_signals()
        
        
    # =========================== #
    #    Construction de l'UI     #
    # =========================== #
    def _build_ui(self):
        """Construit le layout principal de l'écran."""
        # Layout principal vertical
        self.main_layout = QVBoxLayout(self)

        # Section bibliothèque
        self.main_layout.addWidget(QLabel("Bibliothèque des pistes de lecture"))
        self.main_layout.addWidget(self.tracks_table_view)

        # Section playlist
        self.main_layout.addWidget(QLabel("Pistes de la playlist"))

        # Menu + bouton retour
        self.main_layout.addWidget(self.back_btn)
        self.main_layout.addWidget(self.playlist_menu)


    # =========================== #
    #       Connexion signaux     #
    # =========================== #
    def _connect_signals(self):
        """Connecte les signaux des widgets aux signaux de l'écran ou méthodes internes."""
        self.back_btn.clicked.connect(self.request_back_to_library.emit)
        self.tracks_table_view.clicked.connect(self._on_track_clicked)


    # =========================== #
    #      Méthodes publiques     #
    # =========================== #
    def display_tracks(self, tracks: List[Track]) -> None:
        """
        Met à jour le QTableView avec une nouvelle liste de tracks.

        Args:
            tracks (List[Track]): liste de pistes à afficher
        """
        self.tracks_model.set_tracks(tracks)
    

    # =========================== #
    #       Slots internes        #
    # =========================== #
    def _on_track_clicked(self, index: QModelIndex) -> None:
        """
        Émet le signal track_selected quand une track est cliquée dans la table.

        Args:
            index (QModelIndex): index de la track cliquée
        """
        source_index = self.tracks_proxy_model.mapToSource(index)
        track: Track = self.tracks_model._tracks[source_index.row()]
        self.track_selected.emit(track)
        
    
    def replace_main_view(self, new_widget: QWidget) -> None:
        """
        Remplace la partie principale par un autre panel.
        """
        # Retirer tous les widgets existants sauf le menu et le bouton retour
        for i in reversed(range(self.main_layout.count())):
            item = self.main_layout.itemAt(i)
            widget = item.widget()
            if widget and widget not in (self.back_btn, self.playlist_menu):
                widget.setParent(None)

        # Ajouter le nouveau panel en haut (ou à l’index souhaité)
        self.main_layout.insertWidget(0, new_widget)    

        
        