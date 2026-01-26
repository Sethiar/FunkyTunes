# services/file_services/library_services/library_services.py




from app.application.import_track.file_importer import FileImporter
from app.application.import_track.db_importer import DBImporter
from app.application.import_track.import_result import ImportResult, ImportStatus


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

    def __init__(self, session_factory):
        """
        Initialise le service avec une session SQLAlchemy.

        Args:
            db_session: session SQLAlchemy pour accéder aux tables Track, Album, Artist
        """
        self.session_factory = session_factory
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
        with self.session_factory() as session:
            db_importer = DBImporter(session)

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


    