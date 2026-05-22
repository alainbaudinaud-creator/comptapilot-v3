import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import queue
import os
import shutil
import time
from datetime import datetime
from agent import run_agent

PROJECT_DIR = r"C:\Users\alain\mon-projet-agent"

file_attente = queue.Queue()
stop_flag = False


def quitter():
    fenetre.destroy()


def parler_windows():
    entree.focus_set()
    time.sleep(0.2)
    pyautogui.hotkey("win", "h")
    log_system("🎤 Dictée Windows activée.")


def log_system(message):
    zone.insert(tk.END, f"\n{message}\n", "system")
    zone.see(tk.END)


def envoyer():
    global stop_flag
    stop_flag = False

    question = entree.get("1.0", tk.END).strip()
    if not question:
        return

    afficher_message("Vous", question)
    entree.delete("1.0", tk.END)

    bouton_envoyer.config(state=tk.DISABLED)
    progress.start(10)

    zone.insert(tk.END, "\n🤖 Agent PRO :\n", "left_title")
    zone.insert(tk.END, "⏳ Création / modification du logiciel en cours...\n", "left_text")
    zone.see(tk.END)

    threading.Thread(target=traiter_question, args=(question,), daemon=True).start()
    lire_file()


def traiter_question(question):
    try:
        reponse = run_agent(question)
    except Exception as e:
        reponse = f"❌ Erreur : {e}"

    if not stop_flag:
        file_attente.put(reponse)

    file_attente.put("__FIN__")


def lire_file():
    try:
        while True:
            message = file_attente.get_nowait()

            if message == "__FIN__":
                bouton_envoyer.config(state=tk.NORMAL)
                progress.stop()
                return

            zone.insert(tk.END, message + "\n", "left_text")
            zone.see(tk.END)

    except queue.Empty:
        fenetre.after(100, lire_file)


def afficher_message(auteur, texte):
    if auteur == "Vous":
        zone.insert(tk.END, "\n👤 Vous :\n", "right_title")
        zone.insert(tk.END, f"{texte}\n\n", "right_text")
    else:
        zone.insert(tk.END, "\n🤖 Agent :\n", "left_title")
        zone.insert(tk.END, f"{texte}\n\n", "left_text")
    zone.see(tk.END)


def sauvegarder_chat():
    contenu = zone.get("1.0", tk.END).strip()
    if not contenu:
        return

    date = datetime.now().strftime("%Y-%m-%d_%H-%M")
    nom_fichier = f"chat_{date}.txt"
    chemin = os.path.join(PROJECT_DIR, nom_fichier)

    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)

    log_system(f"💾 Conversation sauvegardée : {nom_fichier}")


def stop_reponse():
    global stop_flag
    stop_flag = True
    bouton_envoyer.config(state=tk.NORMAL)
    progress.stop()
    log_system("🛑 Réponse arrêtée.")


def nouveau_chat():
    zone.delete("1.0", tk.END)
    log_system("✅ Agent IA PRO prêt.")


def choisir_fichier():
    fichier = filedialog.askopenfilename()

    if not fichier:
        return

    nom_fichier = os.path.basename(fichier)
    destination = os.path.join(PROJECT_DIR, nom_fichier)

    if os.path.abspath(fichier) != os.path.abspath(destination):
        shutil.copy(fichier, destination)

    entree.delete("1.0", tk.END)
    entree.insert("1.0", f"Analyse le fichier {nom_fichier} et améliore le logiciel si nécessaire.")


def ouvrir_dossier():
    os.startfile(PROJECT_DIR)


def lancer_logiciel():
    main_path = os.path.join(PROJECT_DIR, "main.py")

    if not os.path.exists(main_path):
        messagebox.showwarning("Aucun logiciel", "Aucun fichier main.py trouvé.")
        return

    os.system(f'start cmd /k "cd /d {PROJECT_DIR} && python main.py"')


def envoyer_ctrl_entree(event=None):
    envoyer()
    return "break"


def inserer_exemple_clients():
    entree.delete("1.0", tk.END)
    entree.insert(
        "1.0",
        "Crée-moi un logiciel Windows PRO de gestion de clients avec interface tkinter moderne, "
        "ajout, modification, suppression, recherche, sauvegarde SQLite, export CSV et fiche client."
    )


def inserer_exemple_facture():
    entree.delete("1.0", tk.END)
    entree.insert(
        "1.0",
        "Crée-moi un logiciel Windows de facturation avec clients, produits, TVA, total HT, total TTC, "
        "sauvegarde SQLite et export CSV."
    )


fenetre = tk.Tk()
fenetre.title("Agent IA PRO - Créateur de logiciels")
fenetre.geometry("1300x850")
fenetre.minsize(1000, 650)

style = ttk.Style()
style.theme_use("clam")

frame_principal = ttk.Frame(fenetre, padding=10)
frame_principal.pack(fill=tk.BOTH, expand=True)

titre = ttk.Label(
    frame_principal,
    text="Agent IA PRO - Créateur de logiciels",
    font=("Arial", 18, "bold")
)
titre.pack(anchor="w", pady=(0, 10))

zone = scrolledtext.ScrolledText(
    frame_principal,
    wrap=tk.WORD,
    font=("Consolas", 10),
    height=25
)
zone.pack(fill=tk.BOTH, expand=True)

zone.tag_config("left_title", foreground="#1f4e79", font=("Arial", 11, "bold"))
zone.tag_config("right_title", foreground="#2e7d32", justify="right", font=("Arial", 11, "bold"))
zone.tag_config("left_text", justify="left")
zone.tag_config("right_text", justify="right")
zone.tag_config("system", foreground="#666666", justify="center", font=("Arial", 10, "italic"))

frame_saisie = ttk.Frame(frame_principal)
frame_saisie.pack(fill=tk.X, pady=(10, 5))

entree = tk.Text(frame_saisie, height=7, wrap=tk.WORD, font=("Arial", 11))
entree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
entree.bind("<Control-Return>", envoyer_ctrl_entree)

bouton_envoyer = ttk.Button(frame_saisie, text="Envoyer", command=envoyer)
bouton_envoyer.pack(side=tk.LEFT, fill=tk.Y)

progress = ttk.Progressbar(frame_principal, mode="indeterminate")
progress.pack(fill=tk.X, pady=(0, 8))

frame_actions = ttk.Frame(frame_principal)
frame_actions.pack(fill=tk.X)

ttk.Button(frame_actions, text="🧾 Exemple Clients", command=inserer_exemple_clients).pack(side=tk.LEFT, padx=2)
ttk.Button(frame_actions, text="💶 Exemple Facture", command=inserer_exemple_facture).pack(side=tk.LEFT, padx=2)
ttk.Button(frame_actions, text="🎤 Parler", command=parler_windows).pack(side=tk.LEFT, padx=2)
ttk.Button(frame_actions, text="📂 Ajouter fichier", command=choisir_fichier).pack(side=tk.LEFT, padx=2)
ttk.Button(frame_actions, text="▶️ Lancer main.py", command=lancer_logiciel).pack(side=tk.LEFT, padx=2)
ttk.Button(frame_actions, text="📁 Dossier projet", command=ouvrir_dossier).pack(side=tk.LEFT, padx=2)
ttk.Button(frame_actions, text="💾 Sauver chat", command=sauvegarder_chat).pack(side=tk.LEFT, padx=2)
ttk.Button(frame_actions, text="🛑 Stop", command=stop_reponse).pack(side=tk.LEFT, padx=2)
ttk.Button(frame_actions, text="🆕 Reset", command=nouveau_chat).pack(side=tk.LEFT, padx=2)
ttk.Button(frame_actions, text="❌ Quitter", command=quitter).pack(side=tk.LEFT, padx=2)

log_system("✅ Agent IA PRO prêt.")
zone.insert(
    tk.END,
    "\nExemples :\n"
    "- Crée-moi un logiciel Windows de gestion de clients avec SQLite.\n"
    "- Crée-moi un logiciel de facturation avec TVA et export CSV.\n"
    "- Crée-moi un logiciel de stock avec recherche et sauvegarde.\n\n",
    "left_text"
)

fenetre.mainloop()

