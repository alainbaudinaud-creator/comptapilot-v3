from pathlib import Path

PROJECT = Path("C:/Users/alain/mon-projet-agent/controllers")

FILES = {
    "exportation.py": "ACCESS_EXPORT",
    "rgpd_controller.py": "ACCESS_RGPD",
    "registre_rgpd_controller.py": "ACCESS_RGPD",
    "audit.py": "ACCESS_JOURNAUX",
    "balance.py": "ACCESS_BILAN",
    "grand_livre.py": "ACCESS_JOURNAUX",
    "gestion_plan_comptable.py": "ACCESS_ADMIN",
}

for filename, permission in FILES.items():
    path = PROJECT / filename

    if not path.exists():
        print(f"ABSENT : {path}")
        continue

    text = path.read_text(encoding="utf-8")

    if "from services.permission_service import permission_required" not in text:
        lines = text.splitlines()
        insert_at = 0

        for i, line in enumerate(lines):
            if line.startswith("import ") or line.startswith("from "):
                insert_at = i + 1

        lines.insert(insert_at, "from services.permission_service import permission_required")
        text = "\n".join(lines)

    lines = text.splitlines()
    new_lines = []

    for i, line in enumerate(lines):
        new_lines.append(line)

        if line.strip() == "@login_required":
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""

            if not next_line.startswith("@permission_required"):
                new_lines.append(f'@permission_required("{permission}")')

    path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    print(f"PROTEGE : {filename} -> {permission}")
