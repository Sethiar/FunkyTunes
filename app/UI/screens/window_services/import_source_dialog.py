# app/UI/screens/window_services/import_source_dialog.py


from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtCore import Qt, Signal

from app.UI.molecules.import_icons import ImportSourceBar
from app.UI.organisms.progress_bar_complete import ProgressBarComplete
from app.application.import_track.import_result import ImportStatus


class ImportSourceDialog(QDialog):
    """
    Fenêtre de sélection du support d'import.
    """
    
    # ================================================= #
    #              Déclaration des signaux              #
    # ================================================= #
    request_import_folder = Signal()
    request_import_cd = Signal()
    request_import_usb = Signal()
    
    # ================================================= #
    #              Initialisation du widget             #
    # ================================================= #
    def __init__(self, parent=None):
       super().__init__(parent)
       
       self.setWindowTitle("Sélection du support de l'importation")
       self.resize(500, 400)
       
       self.setAttribute(Qt.WA_StyledBackground, True)
       self.setProperty("component", "import-dialog")
       
       self._build_ui()
       self._connect_signals()
       
       
    # ================================================= #
    #              Construction de l'UI                 #
    # ================================================= #
    def _build_ui(self):
        """Construit l'interface de la sélection d'import."""
        
        # Layout racine de l'écran d'import
        self.import_layout = QVBoxLayout(self)
        self.import_layout.setSpacing(30)
        self.import_layout.setContentsMargins(30, 30, 30, 30)
        
        # Label
        self.title = QLabel("Choisissez le support d’importation")
        self.title.setAlignment(Qt.AlignCenter)
        # Ajout du Label
        self.import_layout.addWidget(self.title)
        
        # Import de la barre d'icônes
        self.import_bar = ImportSourceBar()
        # Ajout de la barre au layout d'import.
        self.import_layout.addWidget(self.import_bar)
        
        # Ajout de la barre de chargement
        self.load_bar = ProgressBarComplete()
        self.import_layout.addWidget(self.load_bar)
        
    def _connect_signals(self):
        """Connecte les signaux des composants UI aux signaux du screen."""
        self.import_bar.import_request_folder.connect(self.request_import_folder.emit)
        self.import_bar.import_request_cd.connect(self.request_import_cd.emit) 
        self.import_bar.import_request_usb.connect(self.request_import_usb.emit)
    
    
    # ================================ #
    #    Méthodes pour le controller   #
    # ================================ #
    def show_import_result(self, result):
        if result.status == ImportStatus.SUCCESS:
            QMessageBox.information(
                self,
                "Import réussi", f"{result.imported} fichiers importés avec succès."
            )
            
        elif result.status == ImportStatus.EMPTY:
            QMessageBox.warning(
                self,
                "Aucun fichier",
                "Aucun fichier audio valide n'a été trouvé."
            )
            
        elif result.status == ImportStatus.PARTIAL:
            QMessageBox.warning(
                self,
                "Import partiel",
                f"{result.imported} fichiers importés.\n"
                f"{len(result.errors)} erreurs."
            )    
            
        
    def show_message(self, title, message):    
        QMessageBox.information(self, title, message)
    
    def set_progress(self, value: int):
        self.progress_bar.setValue(value)
    
    
    # ================================== #
    #    Propriétés pour le controller   #
    # ================================== #   
    @property
    def progress_bar_widget(self) -> ProgressBarComplete:
        """Retourne la barre de progression interne."""
        return self.load_bar.progress_bar   
        