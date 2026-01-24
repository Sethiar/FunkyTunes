# ===================================== #
# FunkyTunes - Architecture logicielle  #
# ===================================== #

Ce projet sert à démontrer ma maîtrise des architectures logicielles, du découplage UI/métier, 
et des bonnes pratiques sur une application desktop réelle.


## TODO : Prochaine étape API pour compléter les informations de la base de données. :

1️⃣ On conçoit l’architecture exacte du module metadata
2️⃣ On choisit MusicBrainz + fallback Last.fm


















## 1. Couche UI
- `app/UI/atoms/` : composants de base (boutons, labels)
- `app/UI/molecules/` : combinaisons d’atomes (menus, barres)
- `app/UI/organisms/` : sections complètes (LibraryDisplayMenu)
- `app/UI/screens/` : fenêtres complètes / dialogs

## 2. Couche Présenters
- `app/presenters/` : Presenter = liaison entre UI et application logic

## 3. Couche Application (Use Cases)
- `app/application/` : logique métier (ex: importation bibliothèque, refresh)

## 4. Couche Domaine / Core
- `core/entities/` : objets métier purs (Dataclass Track)
- `core/utils/` : outils globaux (styles, thèmes, gestion app)

## 5. Couche ORM
- `app/models/` : SQLAlchemy ORM uniquement

## 6. Services / Infrastructure
- `services/file_services/` : accès au système de fichiers
- `services/api_services/` : communication API externe
- `services/player_services/` : lecture audio

## 7. Database
- `database/` : base, engine, init

Funkytunes/
├─ run.py                            # Point d'entrée unique
├─ README.md
├─ requirements.txt
├─ venv/                             # Environnement virtuel (gitignore)
├─ funkytunes.db                     # Base de données (enregistrement)
├─ app/                              # Application principale
│   ├─ application
│   │   ├─ __init__.py
│   │   ├─ import_library.py
│   │   ├─ refresh_library.py
│   │   ├─ 
│   │   ├─ 

│   ├─ controllers/                  
│   │   ├─ __init__.py               
│   │   ├─ home_screen_controller.py
│   │   ├─ import_source_controller.py
│   │   ├─ library_navigation_controller.py
│   │   ├─ player_service_controller.py
│   │   ├─ playlist_controller.py
│   │   ├─ tracks_sort_controller.py   
│   │ 
│   ├─ models/                       # Objets métiers ORM (Track, Album, Artist)
│   │   ├─ __init__.py 
│   │   ├─ album.py
│   │   ├─ artist.py
│   │   ├─ playlist.py
│   │   ├─ track.py
│   │
│   ├─ presenter
│   │   ├─ __init__.py 
│   │   ├─ library_presenter.py
│   │   ├─
│   │
│   ├─ UI/                           # Atomic design (atomes, molécules, organismes)
│   │   ├─ __init__.py
│   │   ├─ atoms/ 
│   │   ├─ molecules/                # combinaisons d’atomes
│   │   ├─ organisms/                # sections complètes
│   │   └─ screens/                  # Présentation en screens
│   │ 
│   └─ view_models/
│       ├─ __init__.py
│       ├─ model_tracks.py           # Modèles Qt
│   
├─ core/                             # Gestion globale
│   ├─ utils/
│   │   ├─ app_manager.py
│   │   ├─ style_manager.py
│   │   └─ theme_manager.py          # Thèmes clair/foncé, couleurstypographies
│   │
│   ├─ entities
│   │   ├─ tracks.py
│   │   └─
│   │
│   ├─ styles/                       # Fichiers de styles qss
│   │   ├─ atoms/
│   │   ├─ molecules/
│   │   ├─ organisms/
│   │   ├─ base.qss
│   │   ├─ dark.qss
│   │   └─
│   │ 
│   ├─ icon_loader.py                # Fichiers comportant le code pour mettre à disposition les icônes          
│   └─ logger.py         
│
├─ database
│   ├─ __init__.py
│   ├─ base.py
│   ├─ engine.py
│   ├─ init_db.py
│   └─
│   
├─ ressources/
│   └─ icons                         # Bibliothèque des icônes de l'application
│                      
└─ services/                         # Tout ce qui interagit avec l’extérieur
    ├─ api_services/                 # APIs externes (jaquettes, titres, artistes)
    └─ file_services/                # Manipulation de fichiers (copie, renommage)
        ├─ library_services/
        │   ├─ db_importer.py        # Création Artist/Album/Track en DB
        │   ├─ file_importer.py      # Scan et lecture fichiers audio
        │   ├─ import_result         # Status import
        │   ├─ import_worker.py        
        │   └─ library_services.py   # Façade + gestion progression
        │
        ├─ player_services/
        │   └─ player_services.py       
        │
        ├─ playlist_services
            └─ playlist_services.py 