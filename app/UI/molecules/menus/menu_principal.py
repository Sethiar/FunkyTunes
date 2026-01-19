# app/UI/molecules/menu_principal.py

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Signal

from app.UI.atoms.buttons import AppButton

class MenuPrincipal(QWidget):
    """
    Menu principal vertical de l'application.
    """
    
    # =========================================== #
    #                  Signaux                    #
    # =========================================== #
    request_import = Signal()
    request_export = Signal()
    open_settings_requested = Signal()
    help_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self.menu_principal_layout = QVBoxLayout(self)
        self.menu_principal_layout.setSpacing(10)
        
        self.import_button = AppButton("Importer ...", variant="menu")
        self.export_button = AppButton("Exporter vers USB", variant="menu")
        self.settings_button = AppButton("Paramètres", variant="menu")
        self.help_button = AppButton("Aide", variant="menu")

        self.button_menu = [
            self.import_button,
            self.export_button,
            self.settings_button,
            self.help_button
        ]
        
        for button in self.button_menu:
            self.menu_principal_layout.addWidget(button)
        
        self.menu_principal_layout.addStretch(1)    
        
        # Branchement des signaux
        self._connect_signals()
            
        
    def _connect_signals(self):
        """ Connexion des signaux aux boutons du menu principal."""
        self.import_button.clicked.connect(self.request_import.emit)
        self.export_button.clicked.connect(self.request_export.emit)
        self.settings_button.clicked.connect(self.open_settings_requested.emit)
        self.help_button.clicked.connect(self.help_requested.emit)
        
