import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import csv

class ComptaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Logiciel de comptabilité multisociétés")
        self.geometry("800x600")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.pages = {
            "Sociétés": ttk.Frame(self.notebook),
            "Plan Comptable": ttk.Treeview(self.notebook, columns=("Code", "Libellé"), show="headings"),
            "Écritures": ttk.Treeview(self.notebook, columns=("Date", "Libellé", "Débit", "Crédit"), show="headings"),
            "Journaux": ttk.Treeview(self.notebook, columns=("Date", "Compte Débiteur", "Montant Débit", "Compte Créditeur", "Montant Crédit", "Libellé"), show="headings"),
            "TVA": ttk.Treeview(self.notebook, columns=("Date", "Type TVA", "Base Imposable", "Montant TVA"), show="headings"),
            "Balance": ttk.Treeview(self.notebook, columns=("Compte", "Solde Débit", "Solde Crédit"), show="headings"),
            "Grand Livre": ttk.Treeview(self.notebook, columns=("Date", "Libellé", "Débit", "Crédit"), show="headings"),
            "Bilan Simplifié": ttk.Treeview(self.notebook, columns=("Compte", "Solde Débit", "Solde Crédit"), show="headings"),
            "Compte de Résultat": ttk.Treeview(self.notebook, columns=("Compte", "Libellé", "Débit", "Crédit"), show="headings"),
            "Clôture d'Exercice": ttk.Frame(self.notebook)
        }

        for title, frame in self.pages.items():
            self.notebook.add(frame, text=title)

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        buttons = {
            "Ajouter Société": self.ajouter_societe,
            "Exporter Balance": lambda: self.exporter("balance"),
            "Exporter Bilan": lambda: self.exporter("bilan"),
            "Exporter Compte de Résultat": lambda: self.exporter("compte_de_resultat")
        }

        for text, command in buttons.items():
            ttk.Button(button_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)

        # Populate sample data
        self.populate_sample_data()

    def populate_sample_data(self):
        sample_data = {
            "Sociétés": ["Société A", "Société B"],
            "Plan Comptable": [("1000", "Actif"), ("2000", "Passif")],
            "Écritures": [("2023-04-01", "Achat d'ordinateur", 500, 0), ("2023-04-01", "Rachat de machine ancienne", 0, 200)],
            "Journaux": [],
            "TVA": [("2023-04-01", "TVA 20%", 1000, 200)],
            "Balance": [],
            "Grand Livre": [],
            "Bilan Simplifié": [],
            "Compte de Résultat": []
        }

        for section, data in sample_data.items():
            frame = self.pages[section]
            if isinstance(frame, ttk.Treeview):
                frame.heading("#0", text="ID")
                for col in frame["columns"]:
                    frame.heading(col, text=col)
                for item in data:
                    if section == "Sociétés":
                        frame.insert("", tk.END, values=(item,))
                    else:
                        frame.insert("", tk.END, values=item)

    def ajouter_societe(self):
        nom = simpledialog.askstring("Nouvelle Société", "Nom de la société :")
        if nom:
            sociétés_frame = self.pages["Sociétés"]
            sociétés_frame.insert("", tk.END, values=(nom,))
            messagebox.showinfo("Success", f"Société {nom} ajoutée avec succès")

    def exporter(self, section):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                tree = self.pages[section]
                header = [col["text"] for col in tree["columns"]]
                writer.writerow(header)
                for item in tree.get_children():
                    row = [tree.item(item, "values")[i] for i in range(len(tree["columns"])) if i < len(tree["columns"])]
                    writer.writerow(row)
            messagebox.showinfo("Success", f"Données de la section {section} exportées avec succès")

if __name__ == "__main__":
    app = ComptaApp()
    app.mainloop()

