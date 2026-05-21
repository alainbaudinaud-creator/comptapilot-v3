from datetime import datetime


def log_http_request(request, response_status):
    try:
        log_line = (
            f"{datetime.now()} | "
            f"IP={request.remote_addr} | "
            f"METHODE={request.method} | "
            f"URL={request.path} | "
            f"STATUS={response_status}"
        )

        with open("http_requests.log", "a", encoding="utf-8") as fichier:
            fichier.write(log_line + "\n")

    except Exception as e:
        print("Erreur log HTTP :", e)
