from app_refonte.test_app_refonte import create_test_app

app = create_test_app()
client = app.test_client()

r = client.get("/api/refonte/health")
assert r.status_code == 200
assert r.json["success"] is True

r = client.post("/api/refonte/immobilisation/amortissement", json={
    "valeur_origine": 1200,
    "duree_mois": 12
})
assert r.status_code == 200
assert len(r.json["lignes"]) == 12

r = client.post("/api/refonte/emprunt/tableau", json={
    "montant": 12000,
    "taux_annuel": 3,
    "duree_mois": 12
})
assert r.status_code == 200
assert len(r.json["lignes"]) == 12

r = client.post("/api/refonte/tva/calcul", json={
    "tva_collectee": 1000,
    "tva_deductible": 300
})
assert r.status_code == 200
assert r.json["resultat"]["tva_a_payer"] == 700

r = client.get("/api/refonte/fec/controle-demo")
assert r.status_code == 200
assert r.json["resultat"]["conforme"] is True

print("TESTS API METIER DEMO OK")
