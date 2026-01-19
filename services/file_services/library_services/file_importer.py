# app/file_services/library_services/file_importer.py

import os
from mutagen import File as MutagenFile
from typing import List, Dict, Optional, Callable

from core.logger import logger


class FileImporter:
    """
    Classe pour scanner un dossier et extraire les métadonnées des fichiers audio.

    Rôle :
        - Identifier les fichiers audio valides
        - Extraire les métadonnées via Mutagen
        - Fournir un callback pour suivre la progression
    """
    
    SUPPORTED_EXTENSIONS = (".mp3", ".wav", ".flac", ".aac", ".ogg")
    
    def __init__(self, progress_callback: Optional[Callable[[int], None]] = None):
        """
        Initialise le scanner de fichiers audio.

        Args:
            progress_callback: Fonction appelée avec un int (0-100) pour indiquer la progression
        """
        self.progress_callback = progress_callback  
    
    
    def scan_directory(self, root_path: str) -> List[str]:
        """
        Scanne récursivement un dossier et retourne tous les fichiers audio valides.

        Args:
            root_path: Chemin du dossier à scanner

        Returns:
            Liste des chemins complets des fichiers audio trouvés
        """
        audio_files: List[str] = []
        total_files = sum(len(files) for _, _, files in os.walk(root_path))
        scanned = 0

        for root, _, files in os.walk(root_path):
            for file in files:
                scanned += 1
                if file.lower().endswith(self.SUPPORTED_EXTENSIONS):
                    audio_files.append(os.path.join(root, file))
                # Callback de progression globale
                if self.progress_callback and total_files > 0:
                    percent = int((scanned / total_files) * 100)
                    self.progress_callback(percent)

        logger.info(f"FileImporter : {len(audio_files)} fichiers audio trouvés dans {root_path}")
        return audio_files
    
    
    def extract_metadata(self, file_path: str) -> Dict[str, object]:
        """
        Extrait les métadonnées d'un fichier audio via Mutagen.

        Args:
            file_path: Chemin complet du fichier audio

        Returns:
            Dictionnaire contenant les informations : file_path, title, artist, album,
            year, track_number, duration, format
        """
        audio = MutagenFile(file_path, easy=True)
        if audio is None:
            raise ValueError(f"Fichier audio invalide: {file_path}")
        
        # Extraction des tags avec valeurs par défaut
        title = audio.get("title", [os.path.splitext(os.path.basename(file_path))[0]])[0]
        artist = audio.get("artist", ["Artiste inconnu"])[0]
        album = audio.get("album", ["Album inconnu"])[0]
        year = audio.get("date", ["Année inconnue"])[0]
        track_number_raw = audio.get("tracknumber", [0])[0]
        try:
            track_number = int(str(track_number_raw).split("/")[0])
        except ValueError:
            track_number = 0

        duration = int(audio.info.length) if audio.info else 0
        format_ = os.path.splitext(file_path)[1].replace(".", "").lower()

        metadata = {
            "file_path": file_path,
            "title": title,
            "artist": artist,
            "album": album,
            "year": year,
            "track_number": track_number,
            "duration": duration,
            "format": format_,
        }
        
        logger.debug(f"FileImporter : Métadonnées extraites pour {file_path}: {metadata}")
        
        return metadata
    
    