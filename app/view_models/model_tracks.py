# app/view_models/model_tracks.py

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex


from core.entities.track import Track


class TracksTableModel(QAbstractTableModel):
    """
    Modélisation de l'affichage des tarcks de funkytunes
    """
    
    HEADERS = ["Pistes", "Titre", "Artiste", "Album", "Durée", "Année"]
    
    def __init__(self, tracks: list[Track] | None = None, parent = None):
        super().__init__(parent)
        self._tracks: list[Track] = tracks or []
        
        
    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._tracks)
    
    
    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.HEADERS)

    
    def track_at(self, row: int) -> Track:
        return self._tracks[row]


    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        track = self._tracks[index.row()]
        column = index.column()
        
        if role == Qt.TextAlignmentRole:
        
            if column == 3:  # Durée
                return Qt.AlignRight | Qt.AlignVCenter
        
            if column == 4:  # Année
                return Qt.AlignCenter        
        
        if role == Qt.DisplayRole:
            return self._data_for_column(track, column)
        
        return None
    
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        
        if orientation == Qt.Horizontal:
            if 0 <= section < len(self.HEADERS):
                return self.HEADERS[section]
            return None
        
        return section + 1
    
    
    # ================ #
    #      Helpers     #
    # ================ #
    def _data_for_column(self, track: Track, column: int):
        match column:
            case 0: return track.counttrack
            case 1: return track.title
            case 2: return track.artist
            case 3: return track.album
            case 4: return self._format_duration(track.duration)
            case 5: return track.year
            case _: return None


    @staticmethod
    def _format_duration(seconds: int) -> str:
        minutes, sec = divmod(seconds, 60)
        return f"{minutes}:{sec:02d}"
    
    
    # Mise à jour de la bibliothèque
    def set_tracks(self, tracks: list[Track]):
        self.beginResetModel()
        self._tracks = tracks
        self.endResetModel()
        
        
 
