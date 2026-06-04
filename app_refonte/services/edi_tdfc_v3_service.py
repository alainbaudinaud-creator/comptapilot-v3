from pathlib import Path
from datetime import datetime
import json


def generer_edi_tdfc_v3(data, output_dir="/app/app_refonte/exports/fiscal/edi"):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    client = data.get("client", {})
    kpis = data.get("kpis", {})
    formulaires = data.get("formulaires", [])
    controles = data.get("controles", {})

    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    client_id = client.get("id", "client")

    base = f"edi_tdfc_v3_client_{client_id}_{horodatage}"
    json_path = Path(output_dir) / f"{base}.json"
    txt_path = Path(output_dir) / f"{base}.txt"

    payload = {
        "format": "COMPTAPILOT_EDI_TDFC_V3_PREPARATION",
        "version": "2026.1",
        "statut": "PRET_CONTROLE_AVANT_TELETRANSMISSION",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "client": {
            "id": client.get("id"),
            "raison_sociale": client.get("raison_sociale"),
            "siren": client.get("siren"),
            "siret": client.get("siret"),
            "forme_juridique": client.get("forme_juridique"),
            "regime_fiscal": client.get("regime_fiscal"),
            "regime_tva": client.get("regime_tva"),
        },
        "kpis": kpis,
        "controles": controles,
        "formulaires": formulaires,
        "avertissement": (
            "Fichier de préparation EDI-TDFC interne ComptaPilot. "
            "Ce fichier n'est pas encore un dépôt DGFiP réel et doit être converti "
            "au format partenaire EDI-TDFC officiel avant télétransmission."
        ),
    }

    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lignes = []
    lignes.append("COMPTAPILOT|EDI_TDFC_V3|PREPARATION")
    lignes.append(f"GENERE_LE|{payload['generated_at']}")
    lignes.append(f"CLIENT_ID|{client.get('id')}")
    lignes.append(f"RAISON_SOCIALE|{client.get('raison_sociale')}")
    lignes.append(f"SIREN|{client.get('siren')}")
    lignes.append(f"SIRET|{client.get('siret')}")
    lignes.append(f"REGIME_FISCAL|{client.get('regime_fiscal')}")
    lignes.append(f"RESULTAT_FISCAL|{kpis.get('resultat_fiscal')}")
    lignes.append(f"TOTAL_ACTIF|{kpis.get('total_actif')}")
    lignes.append(f"TOTAL_PASSIF|{kpis.get('total_passif')}")
    lignes.append(f"EQUILIBRE_BILAN|{kpis.get('equilibre_bilan')}")
    lignes.append("")

    for f in formulaires:
        lignes.append(
            "FORM|{formulaire}|{rubrique}|{valeur}|{statut}".format(
                formulaire=f.get("formulaire", ""),
                rubrique=str(f.get("rubrique", "")).replace("|", "/"),
                valeur=str(f.get("valeur", "")).replace("|", "/"),
                statut=f.get("statut", ""),
            )
        )

    lignes.append("")
    for key, value in controles.items():
        lignes.append(f"CONTROLE|{key}|{'OK' if value else 'A_CONTROLER'}")

    txt_path.write_text("\n".join(lignes), encoding="utf-8")

    return {
        "json_filename": json_path.name,
        "json_path": str(json_path),
        "txt_filename": txt_path.name,
        "txt_path": str(txt_path),
    }
