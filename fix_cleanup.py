p = r"C:\Users\alain\mon-projet-agent\controllers\gestion_ecritures.py"

with open(p, encoding="utf-8") as f:
    lines = f.read().splitlines()

for i in range(14534, 14550):
    lines[i] = ""

with open(p, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("Nettoyage OK")
