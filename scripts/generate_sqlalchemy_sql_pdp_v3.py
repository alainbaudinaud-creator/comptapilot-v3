from sqlalchemy.schema import CreateTable

from models_sqlalchemy.pdp_v3.workflow_model import WorkflowPDPModel
from models_sqlalchemy.pdp_v3.archive_model import ArchiveProbatoireModel
from models_sqlalchemy.pdp_v3.journal_model import JournalTechniquePDPModel

models = [
    WorkflowPDPModel,
    ArchiveProbatoireModel,
    JournalTechniquePDPModel
]

print("=== SQL PostgreSQL PDP V3 ===")
print()

for model in models:
    print(f"-- TABLE: {model.__tablename__}")
    sql = str(CreateTable(model.__table__).compile())
    print(sql)
    print()
