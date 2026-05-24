from datetime import datetime
from pathlib import Path
import subprocess


BACKUP_ROOT = Path("/app/backups/postgres")


def main():

    BACKUP_ROOT.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.utcnow().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_file = BACKUP_ROOT / f"comptapilot_v3_{timestamp}.sql"

    command = [
        "pg_dump",
        "-h",
        "postgres",
        "-U",
        "comptapilot",
        "-d",
        "comptapilot",
        "-f",
        str(backup_file)
    ]

    result = subprocess.run(
        command,
        env={
            "PGPASSWORD": "comptapilot"
        },
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        print("BACKUP ERROR")
        print(result.stderr)

        raise SystemExit(1)

    print("BACKUP OK")
    print(backup_file)


if __name__ == "__main__":
    main()
