# app/models/user.py


"""
Modèle de données pour un album dans l'application FunkyTunes.
"""

from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base


if TYPE_CHECKING:
    from app.models.playlist import Playlist


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)

    playlists: Mapped[List["Playlist"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


    def __repr__(self) -> str:
        return f"<User(username='{self.username}')>"