# core/logger.py

"""
Logger global pour Funkytunes

Permet de centraliser l'affichage des messages et l'écriture dans un fichier.
"""


import logging
import sys
from pathlib import Path


# Répertoire des logs
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Nom du fichier
LOG_FILE = LOG_DIR / "funkytunes.log"

# Configuration globale du logger
logger = logging.getLogger("FunkyTunes")
logger.setLevel(logging.DEBUG)

# Format standard
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(name)s : %(message)s",
    datefmt="%Y-%m-%D %H:%M:%S"
)

# Handler console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


# Handler fichier
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



