from dataclasses import dataclass
from typing import Optional

@dataclass
class ArchiveProbatoire:
    id: Optional[int]
    nom_archive: str
    empreinte_sha256: str
    date_archive: Optional[str]
    detail: Optional[str]
