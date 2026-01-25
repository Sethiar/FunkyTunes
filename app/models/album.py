# app/models/album.py

"""
Modèle de données pour un album dans l'application FunkyTunes.
"""

from typing import TYPE_CHECKING, Optional, List
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base


if TYPE_CHECKING:
    from app.models.artist import Artist
    from app.models.track import Track


class Album(Base):
    __tablename__ = "albums"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False, index=True)
    release_year: Mapped[Optional[int]] = mapped_column(nullable=True)
    jacket_path: Mapped[Optional[str]] = mapped_column(nullable=True)

    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"), nullable=False)

    artist: Mapped["Artist"] = relationship(back_populates="albums")
    tracks: Mapped[List["Track"]] = relationship(
        back_populates="album",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("title", "artist_id", name="uix_album_artist"),
    )

    def __repr__(self) -> str:
        return f"<Album(title='{self.title}', release_year={self.release_year})>"
    
    