
import shutil
from pathlib import Path
from datetime import datetime

BASE = Path(r"C:\Users\alain\mon-projet-agent")
SOURCE = BASE / "db.sqlite"
BACKUPS = BASE / "backups"

BACKUPS.mkdir(exist_ok=True)

horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
destination = BACKUPS / f"db_backup_{horodatage}.sqlite"

shutil.copyfile(SOURCE, destination)

print(f"Sauvegarde creee : {destination}")
