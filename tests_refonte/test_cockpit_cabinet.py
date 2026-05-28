from app_refonte.data.demo_cabinet import CABINET_DEMO
from app_refonte.services.cockpit_cabinet_service import construire_cockpit_cabinet

kpi = construire_cockpit_cabinet(CABINET_DEMO)

assert kpi["total_clients"] == 3
assert kpi["dossiers_retard"] == 1
assert kpi["tva_a_declarer"] == 3070
assert kpi["factures_pdp"] == 67

print("TESTS COCKPIT CABINET OK")
print(kpi)
