# app/controllers/import_source_controller.py


from typing import Optional
from PySide6.QtWidgets import QFileDialog

from services.file_services.library_services.library_services import LibraryServices
from app.application.import_track.import_worker import ImportWorker

from core.logger import logger


class ImportSourceController:
    """
    Contrôleur de la fenêtre d'import de musique.

    Rôle :
        - Relier les actions utilisateur (UI) au service d'import.
        - Gérer le worker d'import dans un thread séparé.
        - Fournir la progression et gérer l'annulation.
    """
    
    def __init__(self, dialog, library_service: LibraryServices, presenter):
        """
        Initialise le controller d'import.

        Args:
            dialog: Vue ImportSourceDialog.
            library_service: Service métier de gestion de la bibliothèque.
            presenter: Presenter chargé de rafraîchir l'affichage des pistes.
        """
        self._dialog = dialog
        self._library_service = library_service
        self._presenter = presenter
        
        self._worker: Optional[ImportWorker] = None

        logger.info("ImportSourceController : initialisé")
        self._bind_signals()

    def _bind_signals(self):
        """Connecte les signaux de la vue aux slots du controller."""
        self._dialog.request_import_folder.connect(self._import_folder)
        self._dialog.request_import_usb.connect(self._import_usb)
        self._dialog.request_import_cd.connect(self._import_cd)
        
        # Annulation de l'import en cours
        self._dialog.load_bar.cancel_requested.connect(self._library_service.cancel_import)


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
        """
        Lance l'import de musique depuis un dossier sélectionné par l'utilisateur.

        Args:
            title: Titre de la boîte de dialogue de sélection.
        """
        if self._worker and self._worker.isRunning():
            logger.warning("Un import est déjà en cours")
            return

        path = QFileDialog.getExistingDirectory(self._dialog, title)
        if not path:
            logger.info("Aucun dossier sélectionné pour l'import")
            return
 
        # Création du worker
        logger.info(f"Démarrage de l'import depuis {path}")
        self._worker = ImportWorker(
            library_service=self._library_service,
            path=path
        )
        
        # Connexion des signaux du worker
        self._worker.progress.connect(self._dialog.progress_bar_widget.set_progress)
        self._worker.finished.connect(self._on_import_finished)
        self._worker.cancelled.connect(self._on_import_cancelled)
        
        # Connexion du bouton Annuler
        self._dialog.load_bar.cancel_requested.connect(self._worker.cancel)
        
        # Lancement du thread
        self._worker.start()
        
        
    def cancel_import(self) -> None:
        """Annule l'import en cours."""
        if self._worker and self._worker.isRunning():
            logger.info("Annulation de l'import demandée")
            self._worker.cancel()
        else:
            logger.info("Aucun import en cours à annuler")
        
    def _on_import_finished(self, result) -> None:
        logger.info("Import terminé")
        self._dialog.show_import_result(result)
        self._presenter.refresh_tracks()
        
        # Nettoyage
        self._cleanup_worker()
        
        # Ferme la fenêtre d'import automatiquement
        if self._dialog.isVisible():
            self._dialog.close()
            logger.info("Fenêtre d'import fermée automatiquement")

    def _on_import_cancelled(self) -> None:
        logger.info("Import annulé par l'utilisateur")
        self._dialog.show_message(
            "Import annulé",
            "L'import a été interrompu par l'utilisateur."
        )
        
        # Nettoyage
        self._cleanup_worker()
        
        if self._dialog.isVisible():
            self._dialog.close()
            logger.info("Fenêtre d'import fermée après annulation")
            
            
    def _cleanup_worker(self):
        """
        Déconnexion des signaux après l’import pour éviter 
        les références persistantes et potentiels memory leaks.
        """
        if self._worker:
            self._worker.progress.disconnect()
            self._worker.finished.disconnect()
            self._worker.cancelled.disconnect()
            self._worker = None    
            
            