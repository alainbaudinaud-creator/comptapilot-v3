from app_refonte.data.demo_supervision import CLIENTS_DEMO
from app_refonte.services.supervision_ia_service import supervision_cabinet

resultat = supervision_cabinet(CLIENTS_DEMO)

assert resultat["score_cabinet"] > 0
assert resultat["alertes"] > 0
assert len(resultat["clients"]) == 3

print("TESTS SUPERVISION IA OK")
print(resultat)
