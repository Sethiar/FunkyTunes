# app/models/playlist.py


"""
Modèle de données pour une playlist musicale dans l'application FunkyTunes.
"""

from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, timezone
from sqlalchemy import Table, ForeignKey, Column, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base


if TYPE_CHECKING:
    from app.models.track import Track
    from app.models.user import User


# Table d'association many-to-many Playlist <-> Track
playlist_track_association = Table(
    "playlist_track_association",
    Base.metadata,
    Column("playlist_id", ForeignKey("playlists.id"), primary_key=True),
    Column("track_id", ForeignKey("tracks.id"), primary_key=True),
)


class Playlist(Base):
    __tablename__ = "playlists"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
    default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc),
    nullable=False
    )
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="playlists")

    tracks: Mapped[List["Track"]] = relationship(
        "Track",
        secondary=playlist_track_association,
        back_populates="playlists",
    )
    
    
    def __repr__(self) -> str:
        return f"<Playlist(name='{self.name}', user_id={self.user_id})>"

    