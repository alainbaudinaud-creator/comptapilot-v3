from __future__ import annotations

import json
import os
import msvcrt
import tarfile
import time
from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import Path


SOURCE = Path(r"C:\Users\alain\comptapilot-v3_clean")
BACKUP_ROOT = Path(r"C:\Users\alain\comptapilot-v3_backup\auto")
ARCHIVE_DIR = BACKUP_ROOT / "archives"
LOG_FILE = BACKUP_ROOT / "auto_backup.log"
LOCK_FILE = BACKUP_ROOT / "auto_backup.lock"
RETENTION_DAYS = 15

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".cache",
    "node_modules",
    "backups",
    "build",
    "dist",
    ".venv",
    "venv",
}

EXCLUDED_FILES = {
    "auto_backup_comptapilot.log",
}

_LOCK_HANDLE = None


def log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(line + os.linesep)


def acquire_lock():
    global _LOCK_HANDLE

    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    handle = LOCK_FILE.open("a+")
    try:
        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        handle.close()
        return None

    _LOCK_HANDLE = handle
    return handle


def should_skip(path: Path) -> bool:
    if path.name in EXCLUDED_FILES:
        return True
    if path.suffix.lower() == ".tar.gz":
        return True
    return any(part in EXCLUDED_DIRS for part in path.parts)


def cleanup_old_archives() -> None:
    if not ARCHIVE_DIR.exists():
        return

    cutoff = datetime.now(timezone.utc).timestamp() - (RETENTION_DAYS * 24 * 60 * 60)

    for archive in ARCHIVE_DIR.glob("comptapilot_snapshot_*.tar.gz"):
        try:
            if archive.stat().st_mtime < cutoff:
                archive.unlink()
                manifest = archive.with_name(archive.name.replace(".tar.gz", ".json"))
                if manifest.exists():
                    manifest.unlink()
        except FileNotFoundError:
            continue


def create_backup() -> Path:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Source introuvable: {SOURCE}")

    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = ARCHIVE_DIR / f"comptapilot_snapshot_{timestamp}.tar.gz"
    manifest_path = archive_path.with_name(archive_path.name.replace(".tar.gz", ".json"))

    files_count = 0
    bytes_count = 0

    with tarfile.open(archive_path, "w:gz") as tar:
        for path in SOURCE.rglob("*"):
            if not path.is_file():
                continue
            if should_skip(path):
                continue

            arcname = path.relative_to(SOURCE)
            tar.add(path, arcname=str(arcname), recursive=False)
            files_count += 1
            try:
                bytes_count += path.stat().st_size
            except OSError:
                pass

    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": str(SOURCE),
        "archive": str(archive_path),
        "files_count": files_count,
        "bytes_count": bytes_count,
        "retention_days": RETENTION_DAYS,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    cleanup_old_archives()
    return archive_path


def run_once() -> int:
    try:
        archive_path = create_backup()
        log(f"Sauvegarde creee : {archive_path}")
        return 0
    except Exception as exc:
        log(f"Echec sauvegarde : {exc}")
        return 1


def main() -> int:
    parser = ArgumentParser(description="Sauvegarde automatique ComptaPilot")
    parser.add_argument("--once", action="store_true", help="Effectue une seule sauvegarde puis quitte")
    args = parser.parse_args()

    lock = acquire_lock()
    if lock is None:
        log("Sauvegarde deja activee ailleurs, sortie sans action")
        return 0

    if args.once:
        return run_once()

    while True:
        run_once()
        log("Prochaine sauvegarde dans 2 heures")
        time.sleep(2 * 60 * 60)


if __name__ == "__main__":
    raise SystemExit(main())
