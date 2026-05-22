from dataclasses import dataclass
from typing import Optional

@dataclass
class WorkflowPDP:
    id: Optional[int]
    facture_id: Optional[int]
    numero: str
    sens: str
    statut: str
    canal: str
    accuse_reception: Optional[str]
    date_action: Optional[str]
    detail: Optional[str]
