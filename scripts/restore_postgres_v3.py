import subprocess
import sys
from pathlib import Path


def main():

    if len(sys.argv) < 2:
        print("Usage: restore_postgres_v3.py <backup.sql>")
        raise SystemExit(1)

    backup_file = Path(sys.argv[1])

    if not backup_file.exists():
        print("Backup introuvable")
        raise SystemExit(1)

    command = [
        "psql",
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

        print("RESTORE ERROR")
        print(result.stderr)

        raise SystemExit(1)

    print("RESTORE OK")


if __name__ == "__main__":
    main()
