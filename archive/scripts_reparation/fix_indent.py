p = r"C:\Users\alain\mon-projet-agent\controllers\gestion_ecritures.py"

with open(p, encoding="utf-8") as f:
    lines = f.read().splitlines()

lines[14178] = '    c.execute("""'

with open(p, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("Correction OK")
