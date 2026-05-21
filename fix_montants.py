p = r"C:\Users\alain\mon-projet-agent\controllers\gestion_ecritures.py"

with open(p, encoding="utf-8") as f:
    lines = f.read().splitlines()

bloc = [
'        if montants:',
'',
'            montant_ttc_detecte = montants[-1]',
'',
'            try:',
'',
'                ttc = float(',
'                    montant_ttc_detecte.replace(",", ".")',
'                )',
'',
'                if tva_detectee:',
'',
'                    tva = float(',
'                        tva_detectee.replace(",", ".")',
'                    )',
'',
'                    ht = round(ttc - tva, 2)',
'',
'                    montant_ht_detecte = (',
'                        str(ht).replace(".", ",")',
'                    )',
'',
'            except:',
'                pass',
'',
'            score_ia += 20'
]

start = 14508
end = 14534

lines[start:end] = bloc

with open(p, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("Bloc montants réparé")
