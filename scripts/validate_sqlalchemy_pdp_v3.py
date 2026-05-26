from models_sqlalchemy.base import Base
from models_sqlalchemy.pdp_v3.workflow_model import WorkflowPDPModel
from models_sqlalchemy.pdp_v3.archive_model import ArchiveProbatoireModel
from models_sqlalchemy.pdp_v3.journal_model import JournalTechniquePDPModel

print("Validation SQLAlchemy PDP V3")

tables = sorted(Base.metadata.tables.keys())

print("Tables détectées :")
for table in tables:
    print("-", table)

expected = {
    "pdp_v3_workflows",
    "pdp_v3_archives",
    "pdp_v3_journal_technique"
}

missing = expected - set(tables)

if missing:
    print("Tables manquantes :", missing)
    raise SystemExit(1)

print("Validation SQLAlchemy PDP V3 OK")

