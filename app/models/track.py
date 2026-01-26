# app/models/track.py

"""
Modèle de données pour une piste musicale dans l'application FunkyTunes.
"""

from typing import TYPE_CHECKING, Optional, List
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base
from app.models.playlist import playlist_track_association


if TYPE_CHECKING:
    from app.models.artist import Artist
    from app.models.album import Album
    from app.models.playlist import Playlist


class Track(Base):
    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False, index=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(nullable=True)
    file_path: Mapped[str] = mapped_column(unique=True, nullable=False)
    format: Mapped[Optional[str]] = mapped_column(nullable=True)
    track_number: Mapped[Optional[int]] = mapped_column(nullable=True)
    genre: Mapped[Optional[str]] = mapped_column(nullable=True)
    is_favorite: Mapped[bool] = mapped_column(default=False, nullable=False)

    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"), nullable=False)
    album_id: Mapped[int] = mapped_column(ForeignKey("albums.id"), nullable=False)

    artist: Mapped["Artist"] = relationship(back_populates="tracks")
    album: Mapped["Album"] = relationship(back_populates="tracks")
    playlists: Mapped[List["Playlist"]] = relationship(
        secondary=playlist_track_association,
        back_populates="tracks"
    )

    __table_args__ = (
        UniqueConstraint("album_id", "track_number", name="uix_album_track_number"),
    )

    def __repr__(self) -> str:
        return (
            f"<Track(title='{self.title}', "
            f"duration_seconds={self.duration_seconds}, "
            f"format='{self.format}', "
            f"track_number={self.track_number})>"
        )