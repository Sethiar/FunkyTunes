# app/models/artist.py

"""
Modèle de données pour un/une artiste dans l'application FunkyTunes.
"""

from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base


if TYPE_CHECKING:
    from app.models.album import Album
    from app.models.track import Track


class Artist(Base):
    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)

    albums: Mapped[List["Album"]] = relationship(
        back_populates="artist",
        cascade="all, delete-orphan"
    )

    tracks: Mapped[List["Track"]] = relationship(
        back_populates="artist",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Artist(name='{self.name}')>"
    
    