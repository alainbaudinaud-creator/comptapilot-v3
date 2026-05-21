
import os

def statut():

    return {
        "db_size": os.path.getsize("db.sqlite"),
        "status": "OK"
    }
