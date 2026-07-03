from pathlib import Path
from app_refonte.renderers.render_portail_demo import render_portail_demo

path = render_portail_demo()
html = Path(path).read_text(encoding="utf-8")

assert "ComptaPilot V3" in html
assert "Cockpit KPI" in html
assert "Cockpit IA" in html
assert "Pipeline qualité" in html

print("TEST PORTAIL DEMO OK")
