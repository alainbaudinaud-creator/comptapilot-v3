from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models_sqlalchemy.base import Base

class WorkflowPDPModel(Base):

    __tablename__ = "pdp_v3_workflows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    facture_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    numero: Mapped[str] = mapped_column(String(255))

    sens: Mapped[str] = mapped_column(String(50))

    statut: Mapped[str] = mapped_column(String(100))

    canal: Mapped[str] = mapped_column(String(100))

    accuse_reception: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    date_action: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    detail: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True
    )
