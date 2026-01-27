# app/controllers/import_source_controller.py


from typing import Optional
from PySide6.QtWidgets import QFileDialog

from services.file_services.library_services.library_services import LibraryServices
from services.file_services.import_services.import_services import ImportServices
from app.application.import_track.import_worker import ImportWorker

from core.logger import logger


class ImportSourceController:
    """
    Contrôleur de la fenêtre d'import de musique.

    Rôle :
        - Lancement du service et passe les callbacks.
    """
    
    def __init__(self, dialog, library_service: LibraryServices, presenter):
        self._dialog = dialog
        self._library_service = library_service
        self._presenter = presenter

        # Service dédié à l'import
        self._import_service = ImportServices(library_service=self._library_service)

        logger.info("ImportSourceController : initialisé")
        self._bind_signals()

    def _bind_signals(self):
        """Connecte les signaux de la vue aux méthodes du controller."""
        self._dialog.request_import_folder.connect(self._import_folder)
        self._dialog.request_import_usb.connect(self._import_usb)
        self._dialog.request_import_cd.connect(self._import_cd)
        logger.info("Connexion des signaux de la vue aux slots du controller.")

        # Annulation de l'import via le bouton
        self._dialog.load_bar.cancel_requested.connect(self._import_service.cancel_import)

    # ============================= #
    #   Slots pour chaque support   #
    # ============================= #
    def _import_folder(self):
        """Importe la musique depuis un dossier local."""
        self._import_from_directory("Choisir un dossier musical")
        

    def _import_usb(self):
        """Importe la musique depuis un support USB."""
        self._import_from_directory("Choisir le dossier USB")
        
        
    def _import_cd(self):
        """Affiche un message indiquant que l'import CD n'est pas disponible."""
        self._dialog.show_message(
            "Pas encore disponible",
            "L'import depuis un CD n'est pas encore implémenté."
        )
    
    
    # ====================== #
    #   Méthode utilitaire   #
    # ====================== #
    def _import_from_directory(self, title: str):
        path = QFileDialog.getExistingDirectory(self._dialog, title)
        if not path:
            logger.info("Aucun dossier sélectionné pour l'import")
            return
    
       # Lancement de l'import via le service, avec callbacks pour UI
        worker = self._import_service.start_import(
            path=path,
            progress_callback=self._dialog.progress_bar_widget.set_progress,
            finished_callback=lambda result: self._on_import_finished(result),
            cancelled_callback=self._on_import_cancelled
        )

        if not worker:
            logger.warning("Import non lancé : un autre import est en cours")


    # ============================= #
    # Callbacks
    # ============================= #
    def _on_import_finished(self, result):
        """Callback quand l'import est terminé."""
        logger.info("Import terminé")
        self._dialog.show_import_result(result)
        self._presenter.refresh_tracks()
        self._import_service.cleanup_worker()
        if self._dialog.isVisible():
            self._dialog.close()
            logger.info("Fenêtre d'import fermée automatiquement")

    def _on_import_cancelled(self):
        """Callback quand l'import est annulé."""
        logger.info("Import annulé")
        self._dialog.show_message("Import annulé", "L'import a été interrompu par l'utilisateur.")
        self._import_service.cleanup_worker()
        if self._dialog.isVisible():
            self._dialog.close()
            logger.info("Fenêtre d'import fermée après annulation")
            
            