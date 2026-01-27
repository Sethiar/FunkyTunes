# app/UI/screens/window_services/create_playlist_screen.py


from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit,
    QSizePolicy, QListWidget,
    QComboBox, QFrame, QFormLayout
)
from PySide6.QtCore import Qt

from app.UI.atoms.buttons import AppButton
from app.UI.molecules.menus.menu_playlist import PlaylistMenu

from core.logger import logger


class CreatePlaylistDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Créer une playlist")
        self.setMinimumWidth(480)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)

        # Titre
        title = QLabel("🎶 Nouvelle playlist")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title)

        # Infos playlist
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.StyledPanel)

        info_layout = QFormLayout(info_frame)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom de la playlist (obligatoire)")
        info_layout.addRow("Nom :", self.name_input)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Description (optionnelle)")
        self.description_input.setFixedHeight(60)
        info_layout.addRow("Description :", self.description_input)

        main_layout.addWidget(info_frame)

        # Tracks
        tracks_frame = QFrame()
        tracks_frame.setFrameShape(QFrame.StyledPanel)
        tracks_layout = QVBoxLayout(tracks_frame)
        
        add_layout = QHBoxLayout()
        self.track_selector = QComboBox()
        self.track_selector.setEditable(True)
        self.track_selector.setPlaceholderText("Ajouter un morceau")

        self.add_track_btn = AppButton("➕ Ajouter")
        self.remove_track_btn = AppButton("- Supprimer")
        add_layout.addWidget(self.track_selector)
        add_layout.addWidget(self.add_track_btn)
        add_layout.addWidget(self.remove_track_btn)

        tracks_layout.addLayout(add_layout)

        self.tracks_list = QListWidget()
        tracks_layout.addWidget(self.tracks_list)

        main_layout.addWidget(tracks_frame)

        # Actions
        actions_layout = QHBoxLayout()
        actions_layout.addStretch()

        self.cancel_btn = AppButton("Annuler")
        self.cancel_btn.clicked.connect(self.reject)

        self.submit_btn = AppButton("Créer la playlist")
        self.submit_btn.setDefault(True)

        actions_layout.addWidget(self.cancel_btn)
        actions_layout.addWidget(self.submit_btn)

        main_layout.addLayout(actions_layout)

        # Signals
        self.add_track_btn.clicked.connect(self._add_track)
        self.remove_track_btn.clicked.connect(self._remove_tracks)


    def _add_track(self):
        track = self.track_selector.currentText()
        if track and track not in self._existing_tracks():
            self.tracks_list.addItem(track)


    def _remove_tracks(self):
        track = self.track_selector.currentText()
        if track and track not in self._existing_tracks():
            self.track_selector.removeItem()
        
        
    def _existing_tracks(self):
        return [
            self.tracks_list.item(i).text()
            for i in range(self.tracks_list.count())
        ]


    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "description": self.description_input.toPlainText().strip(),
            "tracks": self._existing_tracks()
        }
        
        
    def set_available_tracks(self, tracks: list[dict]):
        """
        tracks = [{ "id": int, "label": str }]
        """
        self.track_selector.clear()
        for track in tracks:
            self.track_selector.addItem(track["label"], track["id"])    
        