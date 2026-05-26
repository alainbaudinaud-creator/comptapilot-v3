
import requests
import re
import threading
import py_compile
import subprocess
import os
import time
import json
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, scrolledtext

PROJECT_DIR = Path(r"C:\Users\alain\mon-projet-agent")
GENERATED_FILE = PROJECT_DIR / "main.py"
VERSIONS_DIR = PROJECT_DIR / "versions"
MEMORY_FILE = PROJECT_DIR / "agent_memory.json"
MODEL = "qwen2.5-coder:7b"

stop_requested = False
pause_requested = False
generation_running = False


def log(message):
    output.insert(tk.END, message + "\n")
    output.see(tk.END)
    root.update_idletasks()


def ask_ollama(prompt, timeout=420):
    try:
        r = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Tu es un développeur Python senior. "
                            "Tu réponds uniquement avec du code Python brut. "
                            "Aucun markdown. Aucune explication."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            },
            timeout=timeout
        )
        r.raise_for_status()
        return r.json()["message"]["content"]
    except Exception as e:
        return f"ERREUR_OLLAMA: {e}"


def extract_code(text):
    text = text.strip()
    match = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    if match:
        text = match.group(1).strip()
    if text.startswith("python"):
        text = text[6:].strip()
    return text


def save_memory(task, result):
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    data = []
    if MEMORY_FILE.exists():
        try:
            data = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = []
    data.append({
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "task": task,
        "result": result
    })
    MEMORY_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_memory():
    if not MEMORY_FILE.exists():
        return []
    try:
        return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def backup_version():
    if not GENERATED_FILE.exists():
        return None

    VERSIONS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_path = VERSIONS_DIR / f"main_{timestamp}.py"
    shutil.copy2(GENERATED_FILE, backup_path)
    return backup_path


def is_valid_python(path):
    try:
        py_compile.compile(str(path), doraise=True)
        return True, ""
    except Exception as e:
        return False, str(e)


def demander_stop():
    global stop_requested
    stop_requested = True
    log("🛑 Stop demandé. Arrêt après l’étape en cours.")


def pause_reprise():
    global pause_requested
    if not generation_running:
        return

    pause_requested = not pause_requested

    if pause_requested:
        btn_pause.config(text="Reprendre")
        log("⏸️ Pause demandée.")
    else:
        btn_pause.config(text="Pause")
        log("▶️ Reprise.")


def attendre_si_pause():
    while pause_requested and not stop_requested:
        time.sleep(0.3)


def check_stop():
    attendre_si_pause()
    return stop_requested


def build_prompt(task):
    memory = load_memory()[-3:]

    return f"""
Crée un logiciel Windows complet en Python.

Demande utilisateur :
{task}

Historique récent :
{json.dumps(memory, ensure_ascii=False, indent=2)}

RÈGLES STRICTES :
- Réponds uniquement avec du code Python brut
- Aucun markdown
- Aucune explication
- Un seul fichier main.py
- Bibliothèques standards uniquement
- tkinter + ttk obligatoires
- sqlite3 obligatoire si le logiciel gère des données importantes
- csv obligatoire si export demandé
- json autorisé pour paramètres simples
- Interface propre avec ttk.Notebook si plusieurs modules
- ttk.Treeview pour les tableaux
- Boutons visibles : ajouter, modifier, supprimer, enregistrer, exporter, rechercher si utile
- Gestion d’erreurs utilisateur
- Aucun grand espace vide inutile
- Code directement exécutable
- Fonction main()
- Fin exacte :
if __name__ == "__main__":
    main()

Si comptabilité française :
- outil d’aide uniquement
- ne remplace pas expert-comptable
- ne télétransmet pas officiellement les déclarations fiscales
- inclure plan comptable simplifié, écritures, journaux, TVA, balance, grand livre, bilan simplifié, résultat
"""


def repair_code(task, code, error):
    prompt = f"""
Corrige ce logiciel Python.

Demande initiale :
{task}

Erreur :
{error}

Code :
{code}

Règles :
- code Python brut uniquement
- aucun markdown
- aucune explication
- un seul fichier main.py
- code complet exécutable
"""
    return extract_code(ask_ollama(prompt))


def improve_ui(task, code):
    prompt = f"""
Améliore fortement cette interface tkinter.

Demande :
{task}

Code :
{code}

Objectifs :
- interface professionnelle
- ttk.Notebook si plusieurs sections
- ttk.Treeview pour tableaux
- boutons utiles visibles
- pas d’espace vide inutile
- sauvegarde sqlite3 si données importantes
- exports CSV si utile
- code complet exécutable

Réponds uniquement avec le code Python final.
"""
    return extract_code(ask_ollama(prompt))


def final_review(task, code):
    prompt = f"""
Relis et finalise ce logiciel Python.

Demande :
{task}

Code :
{code}

Corrige :
- imports manquants
- boutons non connectés
- erreurs tkinter
- mainloop absent
- sauvegarde absente
- export absent
- interface vide
- erreurs sqlite
- erreurs csv

Réponds uniquement avec le code Python complet.
"""
    return extract_code(ask_ollama(prompt))


def modifier_code_existant(task, current_code):
    prompt = f"""
Modifie le logiciel Python existant selon cette demande.

Demande de modification :
{task}

Code actuel :
{current_code}

Règles :
- conserve les fonctionnalités existantes
- améliore le code sans tout casser
- code Python brut uniquement
- aucun markdown
- aucune explication
- un seul fichier main.py
- code complet exécutable
"""
    return extract_code(ask_ollama(prompt))


def valider_et_corriger(task, code):
    GENERATED_FILE.write_text(code, encoding="utf-8")
    valid, error = is_valid_python(GENERATED_FILE)

    if valid:
        return True, code, ""

    log("🔧 Correction automatique...")
    code = repair_code(task, code, error)
    GENERATED_FILE.write_text(code, encoding="utf-8")
    valid, error = is_valid_python(GENERATED_FILE)

    return valid, code, error


def run_generation(task):
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)

    old_backup = backup_version()
    if old_backup:
        log(f"💾 Ancienne version sauvegardée : {old_backup.name}")

    log("🤖 Étape 1/6 : génération initiale...")
    answer = ask_ollama(build_prompt(task))

    if "ERREUR_OLLAMA" in answer:
        return "❌ Ollama ne répond pas. Lance : ollama run qwen2.5-coder:7b"

    if check_stop():
        return "🛑 Génération arrêtée."

    code = extract_code(answer)

    log("🔍 Étape 2/6 : validation syntaxe...")
    valid, code, error = valider_et_corriger(task, code)
    if not valid:
        return f"❌ Erreur persistante :\n{error}"

    if check_stop():
        return "🛑 Génération arrêtée."

    log("🎨 Étape 3/6 : amélioration interface...")
    code = improve_ui(task, code)
    valid, code, error = valider_et_corriger(task, code)
    if not valid:
        return f"❌ Erreur après amélioration UI :\n{error}"

    if check_stop():
        return "🛑 Génération arrêtée."

    log("🧠 Étape 4/6 : revue finale...")
    code = final_review(task, code)
    valid, code, error = valider_et_corriger(task, code)
    if not valid:
        return f"❌ Erreur finale :\n{error}"

    log("💾 Étape 5/6 : mémoire...")
    save_memory(task, f"Création : {GENERATED_FILE}")

    log("✅ Étape 6/6 : terminé.")
    return f"✅ Logiciel créé avec succès.\n\n📁 {GENERATED_FILE}"


def run_modification(task):
    if not GENERATED_FILE.exists():
        return "❌ Aucun logiciel existant à modifier."

    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    old_backup = backup_version()
    if old_backup:
        log(f"💾 Version sauvegardée : {old_backup.name}")

    current_code = GENERATED_FILE.read_text(encoding="utf-8")

    log("🛠️ Modification du logiciel actuel...")
    code = modifier_code_existant(task, current_code)

    if check_stop():
        return "🛑 Modification arrêtée."

    log("🔍 Validation...")
    valid, code, error = valider_et_corriger(task, code)
    if not valid:
        return f"❌ Erreur après modification :\n{error}"

    log("🧠 Revue finale...")
    code = final_review(task, code)

    valid, code, error = valider_et_corriger(task, code)
    if not valid:
        return f"❌ Erreur finale :\n{error}"

    save_memory(task, f"Modification : {GENERATED_FILE}")
    return f"✅ Logiciel modifié avec succès.\n\n📁 {GENERATED_FILE}"


def lancer_logiciel():
    if not GENERATED_FILE.exists():
        messagebox.showwarning("Erreur", "Aucun logiciel généré.")
        return

    try:
        subprocess.Popen(
            ["cmd", "/k", "python", str(GENERATED_FILE)],
            cwd=str(PROJECT_DIR)
        )
        log("▶️ Logiciel lancé dans une nouvelle fenêtre.")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))
        log(f"❌ Erreur lancement : {e}")


def creer_exe():
    if not GENERATED_FILE.exists():
        messagebox.showwarning("Erreur", "Aucun logiciel généré.")
        return

    log("📦 Création EXE avec PyInstaller...")

    try:
        subprocess.Popen(
            ["cmd", "/k", "pyinstaller", "--onefile", "--windowed", str(GENERATED_FILE)],
            cwd=str(PROJECT_DIR)
        )
        log("✅ Commande PyInstaller lancée.")
        log("Si PyInstaller n'est pas installé : pip install pyinstaller")
    except Exception as e:
        messagebox.showerror("Erreur EXE", str(e))
        log(f"❌ Erreur EXE : {e}")


def ouvrir_dossier():
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    os.startfile(PROJECT_DIR)


def afficher_memoire():
    output.delete("1.0", tk.END)
    memory = load_memory()

    if not memory:
        log("Aucune mémoire.")
        return

    log("🧠 Mémoire Agent PRO :\n")
    for item in memory[-12:]:
        log(f"{item.get('date', '')}")
        log(f"Demande : {item.get('task', '')}")
        log(f"Résultat : {item.get('result', '')}")
        log("")


def afficher_versions():
    output.delete("1.0", tk.END)
    if not VERSIONS_DIR.exists():
        log("Aucune version sauvegardée.")
        return

    files = sorted(VERSIONS_DIR.glob("*.py"), reverse=True)

    if not files:
        log("Aucune version sauvegardée.")
        return

    log("💾 Versions sauvegardées :\n")
    for f in files[:20]:
        log(str(f))


def lancer_creation():
    global stop_requested, pause_requested, generation_running

    if generation_running:
        messagebox.showwarning("Déjà en cours", "Une opération est déjà en cours.")
        return

    task = text_task.get("1.0", tk.END).strip()
    if not task:
        messagebox.showwarning("Attention", "Écris une demande.")
        return

    stop_requested = False
    pause_requested = False
    generation_running = True

    btn_create.config(state=tk.DISABLED)
    btn_modify.config(state=tk.DISABLED)
    btn_pause.config(state=tk.NORMAL, text="Pause")
    btn_stop.config(state=tk.NORMAL)

    output.delete("1.0", tk.END)
    log("⏳ Agent PRO Niveau 4 : création...")

    def travail():
        global generation_running, pause_requested
        result = run_generation(task)
        log("")
        log(result)
        generation_running = False
        pause_requested = False
        btn_create.config(state=tk.NORMAL)
        btn_modify.config(state=tk.NORMAL)
        btn_pause.config(state=tk.DISABLED, text="Pause")
        btn_stop.config(state=tk.DISABLED)

    threading.Thread(target=travail, daemon=True).start()


def lancer_modification():
    global stop_requested, pause_requested, generation_running

    if generation_running:
        messagebox.showwarning("Déjà en cours", "Une opération est déjà en cours.")
        return

    task = text_task.get("1.0", tk.END).strip()
    if not task:
        messagebox.showwarning("Attention", "Écris la modification souhaitée.")
        return

    stop_requested = False
    pause_requested = False
    generation_running = True

    btn_create.config(state=tk.DISABLED)
    btn_modify.config(state=tk.DISABLED)
    btn_pause.config(state=tk.NORMAL, text="Pause")
    btn_stop.config(state=tk.NORMAL)

    output.delete("1.0", tk.END)
    log("⏳ Agent PRO Niveau 4 : modification du logiciel actuel...")

    def travail():
        global generation_running, pause_requested
        result = run_modification(task)
        log("")
        log(result)
        generation_running = False
        pause_requested = False
        btn_create.config(state=tk.NORMAL)
        btn_modify.config(state=tk.NORMAL)
        btn_pause.config(state=tk.DISABLED, text="Pause")
        btn_stop.config(state=tk.DISABLED)

    threading.Thread(target=travail, daemon=True).start()


root = tk.Tk()
root.title("Agent PRO Niveau 4")
root.geometry("1080x780")

tk.Label(root, text="🤖 Agent PRO Niveau 4", font=("Arial", 24, "bold")).pack(pady=10)
tk.Label(root, text="Créer un logiciel ou modifier le logiciel actuel :", font=("Arial", 12)).pack()

text_task = scrolledtext.ScrolledText(root, height=10, font=("Arial", 11))
text_task.pack(fill=tk.BOTH, padx=20, pady=10)

text_task.insert(
    tk.END,
    "Crée-moi un logiciel de comptabilité multisociétés pour entreprises françaises, "
    "avec SQLite, sociétés, plan comptable, écritures, journaux, TVA, balance, grand livre, "
    "bilan simplifié, compte de résultat, clôture d'exercice, sauvegarde et exports CSV."
)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_create = tk.Button(frame_buttons, text="Créer nouveau", font=("Arial", 11, "bold"), command=lancer_creation)
btn_create.grid(row=0, column=0, padx=4)

btn_modify = tk.Button(frame_buttons, text="Modifier actuel", font=("Arial", 11, "bold"), command=lancer_modification)
btn_modify.grid(row=0, column=1, padx=4)

btn_pause = tk.Button(frame_buttons, text="Pause", font=("Arial", 11), command=pause_reprise, state=tk.DISABLED)
btn_pause.grid(row=0, column=2, padx=4)

btn_stop = tk.Button(frame_buttons, text="Stop", font=("Arial", 11), command=demander_stop, state=tk.DISABLED)
btn_stop.grid(row=0, column=3, padx=4)

btn_launch = tk.Button(frame_buttons, text="Lancer logiciel", font=("Arial", 11), command=lancer_logiciel)
btn_launch.grid(row=0, column=4, padx=4)

btn_exe = tk.Button(frame_buttons, text="Créer EXE", font=("Arial", 11), command=creer_exe)
btn_exe.grid(row=0, column=5, padx=4)

btn_folder = tk.Button(frame_buttons, text="Dossier", font=("Arial", 11), command=ouvrir_dossier)
btn_folder.grid(row=0, column=6, padx=4)

btn_versions = tk.Button(frame_buttons, text="Versions", font=("Arial", 11), command=afficher_versions)
btn_versions.grid(row=0, column=7, padx=4)

btn_memory = tk.Button(frame_buttons, text="Mémoire", font=("Arial", 11), command=afficher_memoire)
btn_memory.grid(row=0, column=8, padx=4)

output = scrolledtext.ScrolledText(root, height=22, font=("Consolas", 10))
output.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

root.mainloop()

