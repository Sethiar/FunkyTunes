# app/mappers/playlist_mapper.py


from core.entities.playlist import Playlist as PlaylistEntity
from app.models.playlist import Playlist as PlaylistORM


def orm_to_entity(playlist: PlaylistORM) -> PlaylistEntity:
    return PlaylistEntity(
        id=playlist.id,
        name=playlist.name,
        user_id=playlist.user_id,
        track_ids=[track.id for track in playlist.tracks],
        current_index=0
    )
    
    