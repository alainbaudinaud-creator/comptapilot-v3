def construire_cockpit_cabinet(data):

    total_clients = len(data.get("clients", []))

    dossiers_retard = len([
        x for x in data.get("clients", [])
        if x.get("retard")
    ])

    total_tva = sum(
        x.get("tva_a_declarer", 0)
        for x in data.get("clients", [])
    )

    total_pdp = sum(
        x.get("factures_pdp", 0)
        for x in data.get("clients", [])
    )

    total_alertes = sum(
        x.get("alertes", 0)
        for x in data.get("clients", [])
    )

    score_global = max(
        0,
        100
        - dossiers_retard * 5
        - total_alertes * 2
    )

    return {
        "total_clients": total_clients,
        "dossiers_retard": dossiers_retard,
        "tva_a_declarer": total_tva,
        "factures_pdp": total_pdp,
        "alertes": total_alertes,
        "score_global": score_global,
    }
