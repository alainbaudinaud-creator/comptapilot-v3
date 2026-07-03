from app_refonte.data.demo_cockpit import DEMO_COCKPIT_DATA
from app_refonte.services.kpi_cockpit_service import calculer_kpis_cockpit, priorites_cockpit

kpis = calculer_kpis_cockpit(DEMO_COCKPIT_DATA)
assert kpis["total_societes"] == 3
assert kpis["total_ecritures"] == 4
assert kpis["equilibre_comptable"] is True
assert kpis["documents_a_traiter"] == 2
assert kpis["score_production"] < 100

priorites = priorites_cockpit(DEMO_COCKPIT_DATA)
assert len(priorites) > 0
assert priorites[0]["niveau"] in ["CRITIQUE", "HAUTE", "WARNING"]

print("TESTS KPI COCKPIT OK")
print(kpis)
