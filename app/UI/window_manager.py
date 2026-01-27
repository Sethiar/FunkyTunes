# app/UI/window_manager.py


class WindowManager:
    """
    Classe qui évite les doublons de vérification de l'ouverture unique d'une 
    fenêtre de l'application FunkyTunes.
    """
    def __init__(self):
        self._windows = {}
    
    def open_unique(self, key, factory):
        window = self._windows.get(key)
        
        if window and window.isVisible():
            window.raise_()
            window.activateWindow()
            return window
        
        window = factory()
        self._windows[key] = window
        window.show()
        
        return window
        