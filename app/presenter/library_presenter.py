# app/presenter/library_presenter.py


from contextlib import contextmanager
from typing import Generator, Callable
from sqlalchemy.orm import Session

from app.view_models.model_tracks import TracksTableModel
from core.entities.track import Track as TrackDataClass
from services.file_services.library_services.library_services import LibraryServices


from core.logger import logger


class LibraryPresenter:
    """
    Presenter de la bibliothèque musicale.

    Rôle :
        - Récupérer les tracks depuis la base de données via LibraryServices
        - Mettre à jour le modèle de la vue
        - Fournir des méthodes de rafraîchissement pour la vue
    """
    
    def __init__(self, view, session_factory):
        """
        Initialise le presenter.

        Args:
            view: Instance de LibraryDisplayMenu
            session_factory: factory SQLAlchemy pour créer une session
        """
        self.view = view
        self.session_factory = session_factory
        logger.info("LibraryPresenter : Chargement initial des tracks...")
        self.load_tracks()


    def load_tracks(self) -> None:
        """
        Charge les pistes depuis la BDD et les injecte dans la vue.

        Crée un TracksTableModel et l'assigne à la vue.
        """
        try:
            with self.session_scope() as session:
                library_service = LibraryServices(session)
                tracks: list[TrackDataClass] = library_service.get_tracks()
                model = TracksTableModel(tracks)
                self.view.set_tracks_model(model)
                logger.info(f"LibraryPresenter : {len(tracks)} tracks chargées")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des tracks: {e}", exc_info=True)
            
            
    def refresh_tracks(self) -> None:
        """
        Recharge les pistes depuis la BDD et met à jour le modèle existant.

        Si aucun modèle n'existe encore, crée un nouveau TracksTableModel.
        """
        try:
            with self.session_scope() as session:
                library_service = LibraryServices(session)
                tracks: list[TrackDataClass] = library_service.get_tracks()
                if self.view.tracks_table_model is None:
                    model = TracksTableModel(tracks)
                    self.view.set_tracks_model(model)
                    logger.info(f"LibraryPresenter : {len(tracks)} tracks rafraîchies")
                else:
                    self.view.tracks_table_model.set_tracks(tracks)
        except Exception as e:
            logger.error(f"Erreur lors du rafraîchissement des tracks: {e}", exc_info=True)


    @contextmanager
    def session_scope(self) -> Generator["Session", None, None]:
        """
        Context manager pour ouvrir et fermer proprement une session SQLAlchemy.

        Yields:
            session (Session): Session SQLAlchemy active
        """
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.exception("Erreur dans la session SQLAlchemy")
            raise
        finally:
            session.close()
            
            