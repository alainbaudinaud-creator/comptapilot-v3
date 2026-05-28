from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class Cabinet:
    nom: str
    siret: Optional[str] = None
    email_contact: Optional[str] = None


@dataclass
class Collaborateur:
    nom: str
    email: str
    role: str = "COLLABORATEUR"
    actif: bool = True


@dataclass
class Societe:
    raison_sociale: str
    siret: Optional[str] = None
    forme_juridique: Optional[str] = None
    regime_tva: Optional[str] = None
    regime_fiscal: Optional[str] = None
    date_cloture: Optional[str] = None


@dataclass
class Ecriture:
    journal: str
    date_ecriture: date
    compte: str
    libelle: str
    debit: Decimal = Decimal("0.00")
    credit: Decimal = Decimal("0.00")
    piece: Optional[str] = None

    def est_equilibree_ligne(self) -> bool:
        return (self.debit > 0 and self.credit == 0) or (self.credit > 0 and self.debit == 0)


@dataclass
class Immobilisation:
    designation: str
    valeur_origine: Decimal
    duree_mois: int
    date_acquisition: Optional[date] = None
    mode_amortissement: str = "LINEAIRE"


@dataclass
class Emprunt:
    banque: str
    libelle: str
    montant_initial: Decimal
    taux_annuel: Decimal
    duree_mois: int
    date_debut: Optional[date] = None


@dataclass
class DocumentComptable:
    fichier: str
    type_document: Optional[str] = None
    statut: str = "A_ANALYSER"
    fournisseur: Optional[str] = None
    numero_facture: Optional[str] = None
    montant_ttc: Optional[Decimal] = None
    score_ia: Optional[Decimal] = None


@dataclass
class TacheWorkflow:
    titre: str
    module: str
    statut: str = "A_TRAITER"
    priorite: str = "NORMALE"
