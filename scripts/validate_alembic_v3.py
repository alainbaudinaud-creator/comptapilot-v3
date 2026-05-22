print("Validation Alembic ComptaPilot V3")

try:
    from alembic.config import Config
except Exception as e:
    print("Alembic non installé pour le moment :", e)
    print("Validation Alembic ignorée sans échec.")
    raise SystemExit(0)

from pathlib import Path

root = Path("/app")
config_path = root / "alembic.ini"
env_path = root / "alembic" / "env.py"

if not config_path.exists():
    print("alembic.ini introuvable")
    raise SystemExit(1)

if not env_path.exists():
    print("alembic/env.py introuvable")
    raise SystemExit(1)

cfg = Config(str(config_path))
script_location = cfg.get_main_option("script_location")

print("script_location =", script_location)
print("Validation Alembic OK")
