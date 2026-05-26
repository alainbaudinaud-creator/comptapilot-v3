
from datetime import datetime
from shutil import copyfile

def sauvegarde():

    fichier = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sqlite"

    copyfile("db.sqlite", fichier)

    return fichier

