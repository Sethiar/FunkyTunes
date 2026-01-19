# services/file_sevices/library_services/import_worker.py


from PySide6.QtCore import QThread, Signal
from services.file_services.library_services.library_services import LibraryServices
from services.file_services.library_services.import_result import ImportResult

from core.logger import logger


class ImportWorker(QThread):
    """
    Worker dédié à l'import des fichiers audio.

    Rôle :
        - Exécuter l'import dans un thread séparé
        - Émettre la progression
        - Permettre l'annulation propre via LibraryServices
    """

    progress = Signal(int)
    finished = Signal(ImportResult)
    cancelled = Signal()

    def __init__(self, library_service: LibraryServices, path: str):
        super().__init__()
        self._library_service = library_service
        self._path = path

    def run(self):
        """Méthode exécutée dans le thread."""
        logger.info(f"ImportWorker : Démarrage de l'import pour {self._path}")

        def progress_callback(percent: int):
            self.progress.emit(percent)

        try:
            result = self._library_service.import_from_directory(
                self._path, progress_callback=progress_callback
            )

            if getattr(self._library_service, "_cancelled", False):
                logger.info("ImportWorker : Import annulé, signal émis")
                self.cancelled.emit()
            else:
                logger.info("ImportWorker : Import terminé, signal finished émis")
                self.finished.emit(result)
        except Exception as e:
            logger.exception(f"ImportWorker : Erreur critique lors de l'import de {self._path}")


    def cancel(self):
        """Demande l'annulation de l'import en cours."""
        logger.info("ImportWorker : Annulation demandée")
        self._library_service.cancel_import()

        
                    