
import requests
import os
from duckduckgo_search import DDGS

MEMORY_FILE = "memory.txt"
MODEL = "phi3:latest"

SYSTEM_PROMPT = """
Tu es un assistant IA professionnel.
Réponds en français, de façon claire et courte.
"""

# =========================
# MÉMOIRE
# =========================

def charger_memoire():
    chemin = os.path.join(os.path.dirname(__file__), MEMORY_FILE)

    if not os.path.exists(chemin):
        return []

    with open(chemin, "r", encoding="utf-8") as f:
        return f.read().splitlines()

def sauvegarder_memoire():
    chemin = os.path.join(os.path.dirname(__file__), MEMORY_FILE)

    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(memory))

memory = charger_memoire()

# =========================
# OUTILS
# =========================

def lire_fichier(nom_fichier):
    chemin = os.path.join(os.path.dirname(__file__), nom_fichier)

    if not os.path.exists(chemin):
        return f"❌ Fichier introuvable : {nom_fichier}"

    with open(chemin, "r", encoding="utf-8") as f:
        return f.read()

def recherche_web(query):
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=3):
            results.append(f"{r['title']} - {r['body']}")

    return "\n".join(results)

# =========================
# AGENT
# =========================

def run_agent(task):

    # 🤖 AUTO-CHOIX FICHIER
    if "document.txt" in task.lower():
        contenu = lire_fichier("document.txt")

        prompt = f"""
{SYSTEM_PROMPT}

Voici un document :
{contenu}

Résume ce document en 3 phrases.
"""

    # 🌐 WEB
    elif task.lower().startswith("web:"):
        query = task.replace("web:", "").strip()
        contenu = recherche_web(query)

        prompt = f"""
{SYSTEM_PROMPT}

Voici des informations web :
{contenu}

Fais un résumé clair.
"""

    # 🤖 MODE AUTONOME
    elif task.lower().startswith("auto:"):
        objectif = task.replace("auto:", "").strip()

        prompt = f"""
{SYSTEM_PROMPT}

Tu es en mode agent autonome.
Objectif : {objectif}

Procède en 3 étapes :
1. Analyse
2. Plan
3. Résultat final
"""

    # 📂 READ
    elif task.lower().startswith("read "):
        nom_fichier = task[5:].strip()
        contenu = lire_fichier(nom_fichier)

        prompt = f"""
{SYSTEM_PROMPT}

Voici un document :
{contenu}

Résume ce document.
"""

    # 💬 NORMAL
    else:
        memory.append(f"Utilisateur : {task}")
        conversation = "\n".join(memory[-5:])

        prompt = f"""
{SYSTEM_PROMPT}

Historique :
{conversation}

Réponds à la dernière demande.
"""

    # API OLLAMA
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    answer = data.get("response", "❌ Erreur")

    memory.append(f"Assistant : {answer}")
    sauvegarder_memoire()

    return answer

# =========================
# LOOP
# =========================

print("🚀 Agent IA PRO (mémoire + fichiers + web + auto)")

while True:
    task = input("\nTask: ")

    if task.lower() == "help":
        print("""
📌 Commandes :
- read document.txt
- web: sujet
- auto: objectif
- memory
- clear memory
- exit
""")
        continue

    if task.lower() == "memory":
        print("\n🧠 Mémoire :")
        print("\n".join(memory) if memory else "vide")
        continue

    if task.lower() == "clear memory":
        memory.clear()
        sauvegarder_memoire()
        print("🧹 Mémoire effacée")
        continue

    if task.lower() == "exit":
        break

    print("\n🤖 Réponse :\n")
    print(run_agent(task))
