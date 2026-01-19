# services/file_services/library_services/library_services.py


from typing import Callable, List, Tuple

from sqlalchemy.orm import joinedload

from services.file_services.library_services.file_importer import FileImporter
from services.file_services.library_services.db_importer import DBImporter
from services.file_services.library_services.import_result import ImportResult, ImportStatus
from core.entities.track import Track as TrackDataClass
from app.models.track import Track as TrackORM

from core.logger import logger


class LibraryServices:
    """
    Service principal pour gérer la bibliothèque musicale.

    Responsabilités :
        - Importer des fichiers depuis un dossier.
        - Suivi de progression avec callback.
        - Annulation de l'import en cours.
        - Fournir les pistes pour l'affichage.
    """

    def __init__(self, db_session):
        """
        Initialise le service avec une session SQLAlchemy.

        Args:
            db_session: session SQLAlchemy
        """
        self.db = db_session
        self._cancelled = False
        
            
    def cancel_import(self):
        """Permet d’arrêter l’import en cours."""
        logger.info("LibraryServices : Import annulé demandé")
        self._cancelled = True
        

    def import_from_directory(self, root_path: str, progress_callback=None) -> ImportResult:
        """
        Importe tous les fichiers audio d'un dossier.

        Args:
            root_path (str): Dossier à scanner
            progress_callback (callable, optional): Callback pour mettre à jour la progression

        Returns:
            ImportResult : Résultat de l'import (SUCCESS, PARTIAL, EMPTY)
        """
        self._cancelled = False
        logger.info(f"LibraryServices : Scan du dossier {root_path}")

        file_importer = FileImporter(progress_callback)
        db_importer = DBImporter(self.db)

        files = file_importer.scan_directory(root_path)
        if not files:
            logger.info("LibraryServices : Aucun fichier trouvé")
            return ImportResult(status=ImportStatus.EMPTY)

        imported = 0
        errors = []
        total = len(files)

        for i, file_path in enumerate(files, start=1):
            if self._cancelled:
                logger.info("LibraryServices : Import annulé en cours")
                break

            try:
                metadata = file_importer.extract_metadata(file_path)
                db_importer.import_track(metadata)
                imported += 1
                if progress_callback:
                    percent = int((i / total) * 100)
                    progress_callback(percent)
            except Exception as e:
                logger.exception(f"Erreur sur le fichier {file_path}")
                errors.append((file_path, str(e)))

        status = ImportStatus.SUCCESS if not errors else (
            ImportStatus.PARTIAL if imported else ImportStatus.EMPTY
        )
        logger.info(f"LibraryServices : Import terminé ({status.name}), {imported}/{total} fichiers importés")
        return ImportResult(status=status, imported=imported, errors=errors)

    def get_tracks(self):
        """Retourne toutes les pistes sous forme de dataclasses prêtes à l'affichage."""
        orm_tracks = (
            self.db.query(TrackORM)
            .options(joinedload(TrackORM.artist), joinedload(TrackORM.album))
            .order_by(TrackORM.album_id, TrackORM.track_number)
            .all()
        )

        tracks = [
            TrackDataClass(
                counttrack=i,
                title=t.title,
                artist=t.artist.name,
                album=t.album.title,
                duration=t.duration_seconds or 0,
                year=t.album.year if hasattr(t.album, "year") else "Indisponible"
            )
            for i, t in enumerate(orm_tracks, start=1)
        ]
        logger.info(f"LibraryServices : {len(tracks)} tracks chargées depuis la BDD")
        return tracks
    
    
    def get_track_file_paths(self) -> list[str]:
        """Retourne les chemins complets pour le PlayerServices"""
        orm_tracks = self.db.query(TrackORM).order_by(TrackORM.album_id, TrackORM.track_number).all()
        paths = [t.file_path for t in orm_tracks]
        logger.info(f"LibraryServices : {len(paths)} tracks pour le PlayerServices")
        
        return paths
    
    