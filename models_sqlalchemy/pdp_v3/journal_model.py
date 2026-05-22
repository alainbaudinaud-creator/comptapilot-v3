from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models_sqlalchemy.base import Base

class JournalTechniquePDPModel(Base):

    __tablename__ = "pdp_v3_journal_technique"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    type_evenement: Mapped[str] = mapped_column(String(255))

    reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    message: Mapped[str] = mapped_column(String(2000))

    empreinte_sha256: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    date_evenement: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
