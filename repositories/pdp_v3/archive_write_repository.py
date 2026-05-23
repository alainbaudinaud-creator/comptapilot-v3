from sqlalchemy import text
from database import engine

def insert_archive(archive: dict):
    with engine.begin() as con:
        result = con.execute(text("""
            INSERT INTO pdp_v3_archives (
                nom_archive,
                empreinte_sha256,
                date_archive,
                detail
            )
            VALUES (
                :nom_archive,
                :empreinte_sha256,
                :date_archive,
                :detail
            )
            RETURNING id
        """), {
            "nom_archive": archive.get("nom_archive"),
            "empreinte_sha256": archive.get("empreinte_sha256"),
            "date_archive": archive.get("date_archive"),
            "detail": archive.get("detail")
        })

        return result.scalar_one()
