from pathlib import Path


BACKUP_ROOT = Path("/app/backups")


def list_backups():

    if not BACKUP_ROOT.exists():
        return []

    items = []

    for path in BACKUP_ROOT.rglob("*"):
        if path.is_file():
            stat = path.stat()
            items.append(
                {
                    "filename": path.name,
                    "path": str(path),
                    "size": stat.st_size,
                    "modified_at": stat.st_mtime
                }
            )

    items.sort(
        key=lambda item: item["modified_at"],
        reverse=True
    )

    return items


