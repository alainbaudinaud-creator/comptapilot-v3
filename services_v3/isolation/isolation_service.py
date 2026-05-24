from repositories.isolation.isolation_repository import (
    list_societes_summary,
    get_societe_object_counts,
    list_user_societe_access
)


def get_isolation_dashboard():

    societes = list_societes_summary()
    counts = get_societe_object_counts()
    access = list_user_societe_access()

    diagnostics = build_diagnostics(
        societes,
        counts,
        access
    )

    return {
        "societes_count": len(societes),
        "access_count": len(access),
        "societes": societes,
        "object_counts": counts,
        "access": access,
        "diagnostics": diagnostics
    }


def build_diagnostics(societes, counts, access):

    warnings = []

    societes_ids = {
        item.get("societe_id")
        for item in societes
    }

    access_societes = {
        item.get("societe_id")
        for item in access
    }

    for societe_id in access_societes:
        if societe_id not in societes_ids:
            warnings.append(
                {
                    "level": "critique",
                    "message": f"Accès lié à une société inexistante : {societe_id}"
                }
            )

    for item in counts:
        if (
            item.get("documents_count", 0) == 0
            and item.get("precompta_count", 0) == 0
            and item.get("ecritures_count", 0) == 0
        ):
            warnings.append(
                {
                    "level": "normal",
                    "message": f"Société sans production détectée : {item.get('nom')}"
                }
            )

    return {
        "warnings_count": len(warnings),
        "warnings": warnings,
        "status": "ok" if not warnings else "attention"
    }
