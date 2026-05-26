def generate_accounting_entry(text):

    text = text.lower()

    if "carrefour" in text:
        return {
            "journal": "ACH",
            "account": "606100",
            "label": "Achats fournitures",
            "vat": "20%"
        }

    if "amazon" in text:
        return {
            "journal": "ACH",
            "account": "606300",
            "label": "Achats petit materiel",
            "vat": "20%"
        }

    return {
        "journal": "ACH",
        "account": "606000",
        "label": "Charge a categoriser",
        "vat": "20%"
    }

