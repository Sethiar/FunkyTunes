# app/UI/molecules/import_icons.py


from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Qt, Signal

from app.UI.atoms.icons_button import IconButton_2


class ImportSourceBar(QWidget):
    """
    Classe pour les icônes de la barre d'import de musique.
    """
    import_request_folder = Signal()
    import_request_cd = Signal()
    import_request_usb = Signal()
    
    def __init__(self):
        super().__init__()
        
        self.setProperty("component", "import-bar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        # Ajout du layout horizontal pour les icônes
        self.import_bar_layout = QHBoxLayout()
        self.import_bar_layout.setSpacing(50)
        self.import_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.import_bar_layout.setAlignment(Qt.AlignCenter)
        
        self.folder_icon = IconButton_2("icon_folder", tooltip="Importer depuis un dossier")
        self.cd_icon = IconButton_2("icon_cd", tooltip="Importer depuis CD")
        self.usb_icon = IconButton_2("icon_usb", tooltip="Importer depuis USB")
        
        for btn in (
            self.folder_icon,
            self.cd_icon,
            self.usb_icon
        ):
            self.import_bar_layout.addWidget(btn)
            
        self.setLayout(self.import_bar_layout)
        
        self._connect_signals()
        
        
    def _connect_signals(self):
        """Connexion des signaux aux boutons du menu principal."""
        self.folder_icon.clicked.connect(self.import_request_folder.emit)
        self.cd_icon.clicked.connect(self.import_request_cd.emit)
        self.usb_icon.clicked.connect(self.import_request_usb.emit)
        
    
    def _on_folder_clicked(self):
        self.import_request_folder.emit()
        
    def _on_cd(self):
        self.import_request_cd.emit()

    def _on_usb(self):
        self.import_request_usb.emit()
        
    