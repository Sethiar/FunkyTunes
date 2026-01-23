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
        - Importer des fichiers audio depuis un dossier
        - Suivi de progression via callback
        - Annulation de l'import en cours
        - Fournir les pistes pour l'affichage ou le player
    """

    def __init__(self, db_session):
        """
        Initialise le service avec une session SQLAlchemy.

        Args:
            db_session: session SQLAlchemy pour accéder aux tables Track, Album, Artist
        """
        self.db = db_session
        self._cancelled = False
        
    
    # ========================== #
    #       Importation          #
    # ========================== #     
    def cancel_import(self):
        """Annulation de l'importation en cours."""
        logger.info("LibraryServices : Import annulé demandé")
        self._cancelled = True
        

    def import_from_directory(self, root_path: str, progress_callback=None) -> ImportResult:
        """
        Importation de tous les fichiers audio depuis un dossier donné.

        Args:
            root_path (str): dossier racine à scanner
            progress_callback (Callable, optional): fonction appelée avec un entier % pour la progression

        Returns:
            ImportResult : contient le statut (SUCCESS, PARTIAL, EMPTY), le nombre de fichiers importés et les erreurs éventuelles
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
                # Extraction des métadonnées (titre, artiste, album, durée, etc.)
                metadata = file_importer.extract_metadata(file_path)
                # Import en BDD
                db_importer.import_track(metadata)
                imported += 1
                
                # Callback de progression
                if progress_callback:
                    percent = int((i / total) * 100)
                    progress_callback(percent)
            except Exception as e:
                logger.exception(f"Erreur sur le fichier {file_path}")
                errors.append((file_path, str(e)))

        # Déterminer le statut final
        if errors and imported:
            status = ImportStatus.PARTIAL
        elif not errors:
            status = ImportStatus.SUCCESS
        else:
            status = ImportStatus.EMPTY

        logger.info(f"LibraryServices : Import terminé ({status.name}), {imported}/{total} fichiers importés")
        return ImportResult(status=status, imported=imported, errors=errors)


    # ========================== #
    #       Accès aux pistes      #
    # ========================== #
    def get_tracks(self) -> List[TrackDataClass]:
        """
        Retourne toutes les pistes sous forme de dataclasses pour affichage UI.

        Returns:
            List[TrackDataClass]: liste des pistes avec titre, artiste, album, durée, année
        """
        orm_tracks = (
            self.db.query(TrackORM)
            .options(joinedload(TrackORM.artist), joinedload(TrackORM.album))
            .order_by(TrackORM.album_id, TrackORM.track_number)
            .all()
        )

        tracks = [
            TrackDataClass(
                id=t.id,
                counttrack=i,
                title=t.title or "",
                artist_name=t.artist.name if t.artist else "",
                
                album_title=t.album.title if t.album else "",
                album_jacket_path=t.album.jacket_path if t.album else None,
                
                genre=t.genre or "",
                duration=t.duration_seconds or 0,
                year=t.album.release_year if t.album else 0
            )
            for i, t in enumerate(orm_tracks, start=1)
        ]

        logger.info(f"LibraryServices : {len(tracks)} tracks chargées depuis la BDD")
        return tracks
    
    
    def get_track_file_paths(self) -> list[str]:
        """
        Retourne la liste des chemins complets pour le PlayerServices.

        Returns:
            list[str]: chemins des fichiers audio
        """
        orm_tracks = self.db.query(TrackORM).order_by(TrackORM.album_id, TrackORM.track_number).all()
        paths = [t.file_path for t in orm_tracks]

        logger.info(f"LibraryServices : {len(paths)} tracks pour le PlayerServices")
        return paths
    
    