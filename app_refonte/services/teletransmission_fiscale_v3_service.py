from datetime import datetime
from uuid import uuid4
from sqlalchemy import text

from app_refonte.services.edi_tdfc_v3_service import generer_edi_tdfc_v3
from database import engine


def preparer_teletransmission_fiscale_v3(data):
    client = data.get("client", {})
    client_id = int(client.get("id") or 1)

    edi = generer_edi_tdfc_v3(data)

    numero = "CP-TDFC-" + datetime.now().strftime("%Y%m%d") + "-" + str(uuid4())[:8].upper()

    with engine.begin() as conn:
        depot_id = conn.execute(text("""
            INSERT INTO teletransmissions_fiscales_v3 (
                client_id,
                type_declaration,
                exercice,
                fichier_edi,
                fichier_json,
                statut,
                numero_transmission,
                message
            )
            VALUES (
                :client_id,
                'EDI_TDFC',
                :exercice,
                :fichier_edi,
                :fichier_json,
                'PRET_A_TRANSMETTRE',
                :numero_transmission,
                :message
            )
            RETURNING id
        """), {
            "client_id": client_id,
            "exercice": "2026",
            "fichier_edi": edi.get("txt_path"),
            "fichier_json": edi.get("json_path"),
            "numero_transmission": numero,
            "message": "Télétransmission fiscale V3 préparée. Envoi DGFiP réel non activé.",
        }).scalar()

    return {
        "id": depot_id,
        "client_id": client_id,
        "numero_transmission": numero,
        "statut": "PRET_A_TRANSMETTRE",
        "edi": edi,
    }


def simuler_envoi_teletransmission_fiscale_v3(depot_id):
    accuse = "AR-SIMULE-" + datetime.now().strftime("%Y%m%d%H%M%S")

    with engine.begin() as conn:
        row = conn.execute(text("""
            SELECT id, client_id, statut, numero_transmission
            FROM teletransmissions_fiscales_v3
            WHERE id = :id
        """), {"id": depot_id}).mappings().first()

        if not row:
            return {"success": False, "error": "Dépôt fiscal introuvable"}

        conn.execute(text("""
            UPDATE teletransmissions_fiscales_v3
            SET statut = 'TRANSMIS_SIMULATION',
                accuse_reception = :accuse,
                transmitted_at = NOW(),
                message = 'Simulation de transmission fiscale réalisée avec succès. Connecteur DGFiP réel à brancher.'
            WHERE id = :id
        """), {"id": depot_id, "accuse": accuse})

    return {
        "success": True,
        "id": depot_id,
        "statut": "TRANSMIS_SIMULATION",
        "accuse_reception": accuse,
    }


def historique_teletransmissions_fiscales_v3(client_id=None, limit=50):
    sql = """
        SELECT
            t.id,
            t.client_id,
            c.raison_sociale,
            t.type_declaration,
            t.exercice,
            t.statut,
            t.numero_transmission,
            t.accuse_reception,
            t.message,
            t.fichier_edi,
            t.fichier_json,
            t.created_at,
            t.transmitted_at
        FROM teletransmissions_fiscales_v3 t
        LEFT JOIN clients_v3 c ON c.id = t.client_id
    """

    params = {"limit": limit}
    if client_id:
        sql += " WHERE t.client_id = :client_id"
        params["client_id"] = client_id

    sql += " ORDER BY t.id DESC LIMIT :limit"

    with engine.begin() as conn:
        rows = conn.execute(text(sql), params).mappings().all()

    return [dict(r) for r in rows]
