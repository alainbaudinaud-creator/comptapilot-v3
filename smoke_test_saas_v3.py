import requests


ROUTES = [
    "/audit-v3",
    "/history",
    "/relances",
    "/notifications",
    "/alerts",
    "/production",
    "/journal-v3",
    "/validation/precompta",
    "/client-portal",
    "/onboarding/client",
]


def main():

    base_url = "http://localhost:5001"

    print("=== SMOKE TEST SAAS V3 ===")

    errors = []

    for route in ROUTES:

        url = base_url + route

        try:
            response = requests.head(
                url,
                timeout=5,
                allow_redirects=False
            )

            print(
                route,
                response.status_code,
                response.headers.get("Location")
            )

            if response.status_code not in [200, 302]:
                errors.append(
                    {
                        "route": route,
                        "status": response.status_code
                    }
                )

        except Exception as exc:

            print(route, "ERROR", exc)

            errors.append(
                {
                    "route": route,
                    "error": str(exc)
                }
            )

    if errors:
        print("SMOKE TEST FAILED")
        raise SystemExit(1)

    print("SMOKE TEST OK")


if __name__ == "__main__":
    main()
