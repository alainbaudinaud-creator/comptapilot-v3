from pathlib import Path
from app_refonte.renderers.render_cockpit_ia import render_cockpit_ia

path = render_cockpit_ia()
html = Path(path).read_text(encoding="utf-8")

assert "Supervision IA Cabinet" in html
assert "Dossiers priorisés par IA" in html
assert "Score cabinet" in html

print("TEST RENDER COCKPIT IA OK")
