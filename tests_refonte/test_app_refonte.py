from app_refonte.app_refonte import create_app_refonte

app = create_app_refonte()
client = app.test_client()

r = client.get("/")
assert r.status_code == 200
assert "ComptaPilot V3 premium" in r.get_data(as_text=True)

r = client.get("/health")
assert r.status_code == 200
assert r.json["success"] is True

r = client.get("/api/refonte/health")
assert r.status_code == 200
assert r.json["success"] is True

print("TEST APP REFONTE OK")
