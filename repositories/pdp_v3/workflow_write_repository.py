from sqlalchemy import text
from database import engine

def insert_workflow(workflow: dict):
    with engine.begin() as con:
        result = con.execute(text("""
            INSERT INTO pdp_v3_workflows (
                facture_id,
                numero,
                sens,
                statut,
                canal,
                accuse_reception,
                date_action,
                detail
            )
            VALUES (
                :facture_id,
                :numero,
                :sens,
                :statut,
                :canal,
                :accuse_reception,
                :date_action,
                :detail
            )
            RETURNING id
        """), {
            "facture_id": workflow.get("facture_id"),
            "numero": workflow.get("numero"),
            "sens": workflow.get("sens"),
            "statut": workflow.get("statut"),
            "canal": workflow.get("canal"),
            "accuse_reception": workflow.get("accuse_reception"),
            "date_action": workflow.get("date_action"),
            "detail": workflow.get("detail")
        })

        return result.scalar_one()


