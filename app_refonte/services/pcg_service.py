from app_refonte.data.pcg_france import PCG_FRANCE_BASE


def lister_pcg_base():
    return [
        {
            "numero": numero,
            "libelle": libelle,
            "classe": numero[0] if numero else "",
        }
        for numero, libelle in PCG_FRANCE_BASE
    ]


def rechercher_compte(terme: str):
    terme = (terme or "").lower().strip()
    if not terme:
        return lister_pcg_base()

    return [
        compte for compte in lister_pcg_base()
        if terme in compte["numero"].lower() or terme in compte["libelle"].lower()
    ]


def comptes_par_classe():
    classes = {}
    for compte in lister_pcg_base():
        classes.setdefault(compte["classe"], []).append(compte)
    return classes


def generer_sql_insert_pcg(table_name="ref_plan_comptable", societe_id_placeholder=":societe_id"):
    values = []
    for compte in lister_pcg_base():
        numero = compte["numero"].replace("'", "''")
        libelle = compte["libelle"].replace("'", "''")
        classe = compte["classe"].replace("'", "''")
        values.append(
            f"({societe_id_placeholder}, '{numero}', '{libelle}', '{classe}', TRUE)"
        )

    return (
        f"INSERT INTO {table_name}(societe_id, numero, libelle, classe, actif) VALUES\n"
        + ",\n".join(values)
        + "\nON CONFLICT(societe_id, numero) DO NOTHING;"
    )
