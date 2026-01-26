# app/UI/organisms/content_stack.py


from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout

from app.UI.organisms.library_display_menu import LibraryDisplayMenu
from app.UI.screens.window_services.playlist_panel import PlaylistPanel



class ContentStack(QWidget):
    def __init__(self):
        super().__init__()
        self.library_display = LibraryDisplayMenu()
        self.playlist_panel = PlaylistPanel()
        self.stack = QStackedWidget()
        
        self.stack.addWidget(self.library_display)
        self.stack.addWidget(self.playlist_panel)
        
        layout = QVBoxLayout()

        layout.addWidget(self.stack)
        self.setLayout(layout)
    
    
    def show_library(self):
        self.stack.setCurrentIndex(0)
    
    
    def show_playlist(self):
        self.stack.setCurrentIndex(1)
