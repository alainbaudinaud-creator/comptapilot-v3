from repositories.pdp_v3.supervision_repository import fetch_supervision_stats

def get_supervision_stats():
    try:
        return fetch_supervision_stats()
    except Exception as e:
        print("PDP V3 SERVICE SUPERVISION WARNING:", e)

    return {
        "workflows": 0,
        "archives": 0,
        "journal": 0
    }


