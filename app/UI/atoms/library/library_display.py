# app/UI/atoms/library/library_display.py


from PySide6.QtWidgets import QTableView, QAbstractItemView, QHeaderView

class TracksTableView(QTableView):
    """
    Modélisation de l'affichage d'une colonne de la bibliothèque des musiques de l'application Funkytunes.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSortingEnabled(True)
        self.verticalHeader().hide()
        self.setShowGrid(True)      
        