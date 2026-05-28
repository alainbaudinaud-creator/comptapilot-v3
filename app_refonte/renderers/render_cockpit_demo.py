from pathlib import Path

from app_refonte.data.demo_cockpit import DEMO_COCKPIT_DATA
from app_refonte.services.kpi_cockpit_service import calculer_kpis_cockpit, priorites_cockpit


def render_cockpit_demo(output_path: str = "previews/refonte/cockpit_kpi_demo.html") -> str:
    kpis = calculer_kpis_cockpit(DEMO_COCKPIT_DATA)
    priorites = priorites_cockpit(DEMO_COCKPIT_DATA)

    priorites_html = "\n".join(
        f"""
        <article class="priority">
          <span>{p['type']}</span>
          <strong>{p['titre']}</strong>
          <em>{p['niveau']}</em>
        </article>
        """
        for p in priorites
    )

    html = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>ComptaPilot V3 — Cockpit KPI Demo</title>
  <link rel="stylesheet" href="../../app_refonte/static/css/cockpit_premium.css">
  <style>
    .priority {{
      background:rgba(15,31,53,.86);
      border:1px solid rgba(148,163,184,.16);
      border-radius:22px;
      padding:18px;
      display:grid;
      gap:8px;
    }}
    .priority span {{ color:#38bdf8;font-weight:900;font-size:12px;letter-spacing:.08em }}
    .priority strong {{ font-size:17px }}
    .priority em {{ color:#fbbf24;font-style:normal }}
  </style>
</head>
<body>
  <div class="shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="logo">CP</div>
        <div>
          <strong>ComptaPilot V3</strong>
          <span>KPI Demo dynamique</span>
        </div>
      </div>
      <nav>
        <a class="active">Cockpit dynamique</a>
        <a>Production comptable</a>
        <a>Fiscalité française</a>
        <a>Immobilisations</a>
        <a>Emprunts</a>
        <a>PDP</a>
      </nav>
    </aside>

    <main class="main">
      <header class="topbar">
        <div>
          <p class="eyebrow">Démonstration KPI isolée</p>
          <h1>Cockpit piloté par le moteur métier ComptaPilot.</h1>
        </div>
        <div class="status"><span></span>Score production {kpis['score_production']}%</div>
      </header>

      <section class="metrics">
        <article><span>Sociétés</span><strong>{kpis['total_societes']}</strong><em>Dossiers actifs</em></article>
        <article><span>Écritures</span><strong>{kpis['total_ecritures']}</strong><em>Débit = Crédit : {kpis['equilibre_comptable']}</em></article>
        <article><span>Documents à traiter</span><strong>{kpis['documents_a_traiter']}</strong><em>OCR / IA</em></article>
        <article><span>Alertes critiques</span><strong>{kpis['alertes_critiques']}</strong><em>Supervision cabinet</em></article>
      </section>

      <section class="hero">
        <div>
          <h2>Production comptable augmentée</h2>
          <p>
            Cette page est générée à partir des services métier isolés :
            KPI, priorités, équilibre comptable, documents, tâches et alertes.
          </p>
          <div class="actions">
            <button>Valider le cockpit</button>
            <button class="secondary">Préparer intégration</button>
          </div>
        </div>
        <div class="hero-card">
          <span>Total débit / crédit</span>
          <strong>{kpis['total_debit']}</strong>
          <p>Crédit : {kpis['total_credit']} — équilibre : {kpis['equilibre_comptable']}</p>
        </div>
      </section>

      <section>
        <h2>Priorités intelligentes</h2>
        <div class="grid">
          {priorites_html}
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
    print(render_cockpit_demo())
