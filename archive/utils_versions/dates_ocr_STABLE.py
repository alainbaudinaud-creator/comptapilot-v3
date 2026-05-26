import re


def normaliser_date_ocr(texte_ocr):

    mois_map = {
        "janv.": "01",
        "janvier": "01",
        "févr.": "02",
        "fevr.": "02",
        "février": "02",
        "fevrier": "02",
        "mars": "03",
        "avr.": "04",
        "avril": "04",
        "mai": "05",
        "juin": "06",
        "juil.": "07",
        "juillet": "07",
        "août": "08",
        "aout": "08",
        "sept.": "09",
        "septembre": "09",
        "oct.": "10",
        "octobre": "10",
        "nov.": "11",
        "novembre": "11",
        "déc.": "12",
        "dec.": "12",
        "décembre": "12",
        "decembre": "12"
    }

    # 15 avr. 2026
    match_fr = re.search(
        r"([0-9]{1,2})\s+(janv\.|janvier|févr\.|fevr\.|février|fevrier|mars|avr\.|avril|mai|juin|juil\.|juillet|août|aout|sept\.|septembre|oct\.|octobre|nov\.|novembre|déc\.|dec\.|décembre|decembre)\s+([0-9]{4})",
        texte_ocr,
        re.IGNORECASE
    )

    if match_fr:

        jour = match_fr.group(1).zfill(2)

        mois_txt = (
            match_fr.group(2)
            .lower()
            .strip()
        )

        annee = match_fr.group(3)

        mois_num = mois_map.get(mois_txt)

        if mois_num:
            return f"{jour}/{mois_num}/{annee}"

    # janv. 13, 2026
    match_us = re.search(
        r"(janv\.|janvier|févr\.|fevr\.|février|fevrier|mars|avr\.|avril|mai|juin|juil\.|juillet|août|aout|sept\.|septembre|oct\.|octobre|nov\.|novembre|déc\.|dec\.|décembre|decembre)\s+([0-9]{1,2}),\s*([0-9]{4})",
        texte_ocr,
        re.IGNORECASE
    )

    if match_us:

        mois_txt = (
            match_us.group(1)
            .lower()
            .strip()
        )

        jour = match_us.group(2).zfill(2)

        annee = match_us.group(3)

        mois_num = mois_map.get(mois_txt)

        if mois_num:
            return f"{jour}/{mois_num}/{annee}"

    return ""

