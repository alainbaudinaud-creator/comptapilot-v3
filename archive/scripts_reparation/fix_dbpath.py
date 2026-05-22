p = r"C:\Users\alain\mon-projet-agent\controllers\gestion_ecritures.py"

with open(p, encoding="utf-8") as f:
    txt = f.read()

txt = txt.replace(
    "conn = sqlite3.connect(DB_PATH)",
    'conn = sqlite3.connect("db.sqlite")'
)

with open(p, "w", encoding="utf-8") as f:
    f.write(txt)

print("DB_PATH corrigé")
