# models/écriture.py
import sqlite3
from datetime import datetime

class Écriture:
    def __init__(self, id_=None, date=None, compte_debit_id=None, compte_credit_id=None, montant=None, description=None):
        self.id_ = id_
        self.date = date if date else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.compte_debit_id = compte_debit_id
        self.compte_credit_id = compte_credit_id
        self.montant = montant
        self.description = description

    def save(self):
        conn = sqlite3.connect('db.sqlite')
        c = conn.cursor()
        if self.id_ is None:
            c.execute("INSERT INTO écritures (date, compte_debit_id, compte_credit_id, montant, description) VALUES (?, ?, ?, ?, ?)", (
                self.date,
                self.compte_debit_id,
                self.compte_credit_id,
                self.montant,
                self.description
            ))
        else:
            c.execute("UPDATE écritures SET date=?, compte_debit_id=?, compte_credit_id=?, montant=?, description=? WHERE id=?", (
                self.date,
                self.compte_debit_id,
                self.compte_credit_id,
                self.montant,
                self.description,
                self.id_
            ))
        conn.commit()
        conn.close()

    @staticmethod
    def all():
        conn = sqlite3.connect('db.sqlite')
        c = conn.cursor()
        c.execute("SELECT * FROM écritures")
        écritures = [Écriture(id_=row[0], date=row[1], compte_debit_id=row[2], compte_credit_id=row[3], montant=row[4], description=row[5]) for row in c.fetchall()]
        conn.close()
        return écritures

    def serialize(self):
        return {
            'id': self.id_,
            'date': self.date,
            'compte_debit_id': self.compte_debit_id,
            'compte_credit_id': self.compte_credit_id,
            'montant': self.montant,
            'description': self.description
        }

