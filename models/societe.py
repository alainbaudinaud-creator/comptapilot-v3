from extensions import db


class Societe(db.Model):
    __tablename__ = "societes"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    siret = db.Column(db.String(20))
    adresse = db.Column(db.Text)

    def serialize(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "siret": self.siret,
            "adresse": self.adresse
        }

