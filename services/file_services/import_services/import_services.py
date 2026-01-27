# app/services/file_services/import_services/import_services.py


from typing import Optional, Callable

from app.application.import_track.import_worker import ImportWorker

from core.logger import logger


class ImportServices:
    """
    Service dédié à l'importation de fichiers musicaux.
    Gère le worker, la progression, l'annulation et les callbacks.
    """
    def __init__(self, library_service):
        self._library_service = library_service
        self._worker: Optional[ImportWorker] = None


    def start_import(
        self,
        path: str,
        progress_callback: Optional[Callable[[int], None]] = None,
        finished_callback: Optional[Callable] = None,
        cancelled_callback: Optional[Callable] = None
    ) -> Optional[ImportWorker]:
        """
        Lance l'import depuis le chemin donné, avec callbacks pour progression et fin.
        """
        if self._worker and self._worker.isRunning():
            logger.warning("Un import est déjà en cours")
            return None

        logger.info(f"Démarrage de l'import depuis {path}")
        self._worker = ImportWorker(library_service=self._library_service, path=path)

        # Connexion des callbacks
        if progress_callback:
            self._worker.progress.connect(progress_callback)
        if finished_callback:
            self._worker.finished.connect(finished_callback)
        if cancelled_callback:
            self._worker.cancelled.connect(cancelled_callback)

        self._worker.start()
        return self._worker

    def cancel_import(self):
        """Annule l'import en cours."""
        if self._worker and self._worker.isRunning():
            logger.info("Annulation de l'import demandée")
            self._worker.cancel()
        else:
            logger.info("Aucun import en cours à annuler")

    def cleanup_worker(self):
        """Déconnecte les signaux et supprime le worker pour éviter les memory leaks."""
        if self._worker:
            try:
                self._worker.progress.disconnect()
                self._worker.finished.disconnect()
                self._worker.cancelled.disconnect()
            except TypeError:
                pass
            self._worker = None
            
            