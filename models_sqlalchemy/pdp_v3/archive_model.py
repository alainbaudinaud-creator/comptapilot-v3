from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models_sqlalchemy.base import Base

class ArchiveProbatoireModel(Base):

    __tablename__ = "pdp_v3_archives"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    nom_archive: Mapped[str] = mapped_column(String(255))

    empreinte_sha256: Mapped[str] = mapped_column(String(255))

    date_archive: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    detail: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True
    )
