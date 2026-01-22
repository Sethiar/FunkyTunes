# app/UI/organisms/explorer_grid_view.py

from typing import Dict, List

from PySide6.QtWidgets import (
    QVBoxLayout, QWidget, QGridLayout, 
    QScrollArea, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap

from core.logger import logger

class ExplorerGridView(QWidget):
    """
    Vue générique type Explorer (Albums, Artistes, Genres)
    """
    
    item_clicked = Signal(object)
    
    def __init__(
        self, 
        items: List[Dict[str, Dict]],
        columns: int=4,
        icon_size: int=60,
        parent=None
    ):
        super().__init__(parent)
        self.items = items
        self.columns = columns
        self.icon_size = icon_size
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(16)

        row = col = 0
        
        for item in self.items.values():
            widget = self._create_item_widget(item)
            widget.mousePressEvent = self._bind_click(item["payload"])

            grid.addWidget(widget, row, col)
            
            
            col += 1
            if col >= self.columns:
                col = 0
                row += 1

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)

        main_layout.addWidget(scroll)
    
    
    def _bind_click(self, payload):
        return lambda e: self.item_clicked.emit(payload)
       

    def _create_item_widget(self, item: dict) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(8)

        # Icône
        icon_label = QLabel()
        icon_label.setFixedSize(self.icon_size, self.icon_size)
        icon_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        icon_label.setAlignment(Qt.AlignCenter)
        
        pixmap = QPixmap(
            item.get("icon", "resources/icons/album_icon.svg")
        ).scaled(
            self.icon_size,
            self.icon_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        icon_label.setPixmap(pixmap)
        layout.addWidget(icon_label)

        # Titre
        title = QLabel(item["title"])
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        title.setFixedWidth(self.icon_size + 40)

        layout.addWidget(title)

        return widget
    
    
    