from dataclasses import dataclass
from typing import Optional

@dataclass
class JournalTechniquePDP:
    id: Optional[int]
    type_evenement: str
    reference: Optional[str]
    message: str
    empreinte_sha256: Optional[str]
    date_evenement: Optional[str]
