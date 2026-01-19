# services/file_services/library_services/import_result.py


from enum import Enum
from dataclasses import dataclass

from typing import List, Tuple


class ImportStatus(Enum):
    """
    Docstring pour ImportStatus
    """
    SUCCESS = "success"
    EMPTY = "empty"
    PARTIAL = "partial"
    ERROR = "error"
    
    
@dataclass
class ImportResult:
    status: ImportStatus
    imported: int = 0
    errors: List[Tuple[str, Exception]] = None    
