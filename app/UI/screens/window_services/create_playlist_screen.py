# app/UI/screens/window_services/create_playlist_screen.py


from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QHBoxLayout, QSizePolicy
)

from app.UI.atoms.buttons import AppButton
from app.UI.molecules.menus.menu_playlist import PlaylistMenu


class CreateplaylistForm(QWidget):
    """
    Écran dédié à la création d'une playlist.
    Ne persiste aucune donnée.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._build_ui()
        self._connect_signals()
        
        
    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # ===== Header =====
        title = QLabel("Créer une nouvelle playlist")
        title.setObjectName("screenTitle")
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        main_layout.addWidget(title)
        
       # ===== Formulaire =====
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        name_label = QLabel("Nom de la playlist")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ex : Mes sons chill")

        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.hide()

        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.error_label)

        main_layout.addLayout(form_layout)

        # ===== Zone extensible (future : morceaux, image, etc.) =====
        main_layout.addStretch()

        # ===== Footer actions =====
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)
        
        self.playlist_menu = PlaylistMenu()

        self.btn_cancel = AppButton("Annuler")
        self.btn_validate = AppButton("Enregistrer la playlist")

        actions_layout.addStretch()
        actions_layout.addWidget(self.btn_cancel)
        actions_layout.addWidget(self.btn_validate)

        main_layout.addLayout(actions_layout)

    # -----------------
    # Signals
    # -----------------
    def _connect_signals(self):
        self.btn_validate.clicked.connect(self._on_validate)

    # -----------------
    # Validation
    # -----------------
    def _on_validate(self):
        name = self.name_input.text().strip()

        if not name:
            self._show_error("Le nom de la playlist est obligatoire")
            return

        self._clear_error()
        self.on_submit({
            "name": name
        })

    # -----------------
    # Public API
    # -----------------
    def on_submit(self, data: dict):
        """
        À surcharger ou connecter depuis le parent.
        """
        pass

    def on_cancel(self):
        """
        À connecter depuis le parent.
        """
        pass

    # -----------------
    # Error handling
    # -----------------
    def _show_error(self, message: str):
        self.error_label.setText(message)
        self.error_label.show()

    def _clear_error(self):
        self.error_label.hide()
        
        