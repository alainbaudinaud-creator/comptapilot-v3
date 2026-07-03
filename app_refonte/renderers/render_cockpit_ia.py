from pathlib import Path

from app_refonte.data.demo_supervision import CLIENTS_DEMO
from app_refonte.services.supervision_ia_service import supervision_cabinet


def render_cockpit_ia(output_path="previews/refonte/cockpit_ia_premium.html"):
    data = supervision_cabinet(CLIENTS_DEMO)

    clients_html = ""

    for client in data["clients"]:
        alertes = ", ".join(client["alertes"]) if client["alertes"] else "Aucune alerte"

        clients_html += f"""
        <article class="module">
            <h3>{client['nom']}</h3>
            <p>Score santé : <strong>{client['score']}%</strong></p>
            <p>Alertes : {alertes}</p>
            <span>Priorité IA : {client['priorite']}</span>
        </article>
        """

    html = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>ComptaPilot V3 — Cockpit IA Premium</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="../../app_refonte/static/css/cockpit_premium.css">
</head>
<body>
  <div class="shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="logo">AI</div>
        <div>
          <strong>ComptaPilot IA</strong>
          <span>Supervision cabinet</span>
        </div>
      </div>

      <nav>
        <a class="active">Cockpit IA</a>
        <a>Clients à risque</a>
        <a>TVA</a>
        <a>PDP</a>
        <a>OCR IA</a>
        <a>FEC</a>
      </nav>
    </aside>

    <main class="main">
      <header class="topbar">
        <div>
          <p class="eyebrow">Supervision IA Cabinet</p>
          <h1>Priorisez automatiquement les dossiers qui nécessitent votre attention.</h1>
        </div>
        <div class="status"><span></span>Score cabinet {data['score_cabinet']}%</div>
      </header>

      <section class="metrics">
        <article>
          <span>Score cabinet</span>
          <strong>{data['score_cabinet']}%</strong>
          <em>Santé globale portefeuille</em>
        </article>

        <article>
          <span>Alertes</span>
          <strong>{data['alertes']}</strong>
          <em>Alertes actives</em>
        </article>

        <article>
          <span>Dossiers critiques</span>
          <strong>{data['dossiers_critiques']}</strong>
          <em>À traiter en priorité</em>
        </article>

        <article>
          <span>Clients analysés</span>
          <strong>{len(data['clients'])}</strong>
          <em>Supervision IA</em>
        </article>
      </section>

      <section class="hero">
        <div>
          <h2>Assistant de pilotage cabinet</h2>
          <p>
            Cette page exploite le moteur Supervision IA pour classer automatiquement
            les clients selon leur risque, leurs retards, leurs alertes, leur TVA
            et leur activité PDP.
          </p>
          <div class="actions">
            <button>Traiter les priorités</button>
            <button class="secondary">Analyser le portefeuille</button>
          </div>
        </div>

        <div class="hero-card">
          <span>Priorité cabinet</span>
          <strong>{data['clients'][0]['nom']}</strong>
          <p>Score client : {data['clients'][0]['score']}%</p>
        </div>
      </section>

      <section>
        <h2>Dossiers priorisés par IA</h2>
        <div class="grid">
          {clients_html}
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return str(out)


if __name__ == "__main__":
    print(render_cockpit_ia())
