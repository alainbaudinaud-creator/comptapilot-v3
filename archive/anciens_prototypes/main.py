import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from openpyxl import Workbook
import csv

def main():
    root = Tk()
    root.title("Logiciel de Comptabilité Multisociétés")
    
    style = ttk.Style(root)
    style.theme_use('clam')
    
    notebook = ttk.Notebook(root, padding=5)
    notebook.pack(fill=BOTH, expand=True)

    def save_database():
        try:
            conn.commit()
            messagebox.showinfo("Succès", "Données sauvegardées avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de sauvegarde : {e}")
    
    def export_to_csv(table_name, file_path):
        query = f"SELECT * FROM {table_name}"
        conn.execute(query)
        data = conn.fetchall()
        
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            columns = [desc[0] for desc in conn.description]
            writer.writerow(columns)
            writer.writerows(data)
    
    conn = sqlite3.connect('comptabilité.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS sociétés (id INTEGER PRIMARY KEY, nom TEXT, adresse TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS écritures (id INTEGER PRIMARY KEY, date TEXT, compte_from TEXT, compte_to TEXT, montant REAL)")
    
    # Onglet Sociétés
    tab1 = Frame(notebook)
    notebook.add(tab1, text="Sociétés")
    
    tree_sociétés = ttk.Treeview(tab1, columns=("ID", "Nom", "Adresse"), show='headings')
    tree_sociétés.heading("ID", text="ID")
    tree_sociétés.heading("Nom", text="Nom")
    tree_sociétés.heading("Adresse", text="Adresse")
    tree_sociétés.pack(fill=BOTH, expand=True)
    
    btn_ajouter_société = Button(tab1, text="Ajouter Société", command=lambda: print("Société ajoutée"))
    btn_ajouter_société.pack(side=LEFT)
    
    # Onglet Plan Comptable
    tab2 = Frame(notebook)
    notebook.add(tab2, text="Plan Comptable")
    
    tree_plan_comptable = ttk.Treeview(tab2, columns=("ID", "Code", "Libellé"), show='headings')
    tree_plan_comptable.heading("ID", text="ID")
    tree_plan_comptable.heading("Code", text="Code")
    tree_plan_comptable.heading("Libellé", text="Libellé")
    tree_plan_comptable.pack(fill=BOTH, expand=True)
    
    btn_ajouter_compte = Button(tab2, text="Ajouter Compte", command=lambda: print("Compte ajouté"))
    btn_ajouter_compte.pack(side=LEFT)
    
    # Onglet Écritures
    tab3 = Frame(notebook)
    notebook.add(tab3, text="Écritures")
    
    tree_écritures = ttk.Treeview(tab3, columns=("ID", "Date", "Compte From", "Compte To", "Montant"), show='headings')
    tree_écritures.heading("ID", text="ID")
    tree_écritures.heading("Date", text="Date")
    tree_écritures.heading("Compte From", text="Compte From")
    tree_écritures.heading("Compte To", text="Compte To")
    tree_écritures.heading("Montant", text="Montant")
    tree_écritures.pack(fill=BOTH, expand=True)
    
    btn_ajouter_écriture = Button(tab3, text="Ajouter Écriture", command=lambda: print("Écriture ajoutée"))
    btn_ajouter_écriture.pack(side=LEFT)
    
    # Onglet TVA
    tab4 = Frame(notebook)
    notebook.add(tab4, text="TVA")
    
    tree_tva = ttk.Treeview(tab4, columns=("ID", "Montant", "Base", "Taux"), show='headings')
    tree_tva.heading("ID", text="ID")
    tree_tva.heading("Montant", text="Montant")
    tree_tva.heading("Base", text="Base")
    tree_tva.heading("Taux", text="Taux")
    tree_tva.pack(fill=BOTH, expand=True)
    
    btn_ajouter_tva = Button(tab4, text="Ajouter TVA", command=lambda: print("TVA ajoutée"))
    btn_ajouter_tva.pack(side=LEFT)
    
    # Onglet Balance
    tab5 = Frame(notebook)
    notebook.add(tab5, text="Balance")
    
    tree_balance = ttk.Treeview(tab5, columns=("Compte", "Debit", "Crédit"), show='headings')
    tree_balance.heading("Compte", text="Compte")
    tree_balance.heading("Debit", text="Débit")
    tree_balance.heading("Crédit", text="Crédit")
    tree_balance.pack(fill=BOTH, expand=True)
    
    btn_calculer_balance = Button(tab5, text="Calculer Balance", command=lambda: print("Balance calculée"))
    btn_calculer_balance.pack(side=LEFT)
    
    # Onglet Grand Livre
    tab6 = Frame(notebook)
    notebook.add(tab6, text="Grand Livre")
    
    tree_grand_livre = ttk.Treeview(tab6, columns=("Date", "Compte From", "Compte To", "Montant"), show='headings')
    tree_grand_livre.heading("Date", text="Date")
    tree_grand_livre.heading("Compte From", text="Compte From")
    tree_grand_livre.heading("Compte To", text="Compte To")
    tree_grand_livre.heading("Montant", text="Montant")
    tree_grand_livre.pack(fill=BOTH, expand=True)
    
    btn_exporter_grand_livre = Button(tab6, text="Exporter Grand Livre", command=lambda: export_to_csv('écritures', 'grand_livre.csv'))
    btn_exporter_grand_livre.pack(side=LEFT)
    
    # Onglet Bilan Simplifié
    tab7 = Frame(notebook)
    notebook.add(tab7, text="Bilan Simplifié")
    
    tree_bilan_simplifié = ttk.Treeview(tab7, columns=("Compte", "Solde"), show='headings')
    tree_bilan_simplifié.heading("Compte", text="Compte")
    tree_bilan_simplifié.heading("Solde", text="Solde")
    tree_bilan_simplifié.pack(fill=BOTH, expand=True)
    
    btn_calculer_bilan = Button(tab7, text="Calculer Bilan", command=lambda: print("Bilan calculé"))
    btn_calculer_bilan.pack(side=LEFT)
    
    # Onglet Compte de Résultat
    tab8 = Frame(notebook)
    notebook.add(tab8, text="Compte de Résultat")
    
    tree_compte_de_résultat = ttk.Treeview(tab8, columns=("Compte", "Débit", "Crédit"), show='headings')
    tree_compte_de_résultat.heading("Compte", text="Compte")
    tree_compte_de_résultat.heading("Débit", text="Débit")
    tree_compte_de_résultat.heading("Crédit", text="Crédit")
    tree_compte_de_résultat.pack(fill=BOTH, expand=True)
    
    btn_calculer_compte_de_résultat = Button(tab8, text="Calculer Compte de Résultat", command=lambda: print("Compte de Résultat calculé"))
    btn_calculer_compte_de_résultat.pack(side=LEFT)
    
    # Onglet Clôture d'Exercice
    tab9 = Frame(notebook)
    notebook.add(tab9, text="Clôture d'Exercice")
    
    btn_clôturer_exercice = Button(tab9, text="Clôturer l'exercice", command=lambda: print("Exercice clôturé"))
    btn_clôturer_exercice.pack()
    
    btn_sauvegarder = Button(tab9, text="Sauvegarder", command=save_database)
    btn_sauvegarder.pack(side=RIGHT)
    
    root.mainloop()

if __name__ == "__main__":
    main()
