# models/plan_comptable.py
import sqlite3

class PlanComptable:
    def __init__(self, id_=None, code=None, name=None, type_=None):
        self.id_ = id_
        self.code = code
        self.name = name
        self.type_ = type_

    def save(self):
        conn = sqlite3.connect('db.sqlite')
        c = conn.cursor()
        if self.id_ is None:
            c.execute("INSERT INTO plan_comptable (code, name, type_) VALUES (?, ?, ?)", (self.code, self.name, self.type_))
        else:
            c.execute("UPDATE plan_comptable SET code=?, name=?, type=? WHERE id=?", (
                self.code,
                self.name,
                self.type_,
                self.id_
            ))
        conn.commit()
        conn.close()

    @staticmethod
    def all():
        conn = sqlite3.connect('db.sqlite')
        c = conn.cursor()
        c.execute("SELECT * FROM plan_comptable")
        comptes = [PlanComptable(id_=row[0], code=row[1], name=row[2], type_=row[3]) for row in c.fetchall()]
        conn.close()
        return comptes

    def serialize(self):
        return {
            'id': self.id_,
            'code': self.code,
            'name': self.name,
            'type': self.type_
        }

