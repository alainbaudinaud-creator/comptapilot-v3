from pathlib import Path

def render_portail_demo(output_path="previews/refonte/index.html"):
    html = """<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>ComptaPilot V3 — Portail Démo Premium</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="../../app_refonte/static/css/cockpit_premium.css">
</head>
<body>
  <div class="shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="logo">CP</div>
        <div>
          <strong>ComptaPilot V3</strong>
          <span>Portail démo premium</span>
        </div>
      </div>
      <nav>
        <a class="active">Accueil démo</a>
        <a href="cockpit_kpi_demo.html">Cockpit KPI</a>
        <a href="cockpit_ia_premium.html">Cockpit IA</a>
      </nav>
    </aside>

    <main class="main">
      <header class="topbar">
        <div>
          <p class="eyebrow">SaaS cabinet comptable français</p>
          <h1>Une plateforme premium pour piloter toute la production comptable.</h1>
        </div>
        <div class="status"><span></span>Refonte testée</div>
      </header>

      <section class="hero">
        <div>
          <h2>Vision produit</h2>
          <p>
            ComptaPilot V3 combine cockpit cabinet, IA documentaire, TVA, FEC,
            PDP, immobilisations, emprunts, rapprochement bancaire et supervision intelligente.
          </p>
          <div class="actions">
            <button>Voir cockpit KPI</button>
            <button class="secondary">Voir cockpit IA</button>
          </div>
        </div>
        <div class="hero-card">
          <span>Modules testés</span>
          <strong>19</strong>
          <p>Pipeline qualité global opérationnel.</p>
        </div>
      </section>

      <section class="grid">
        <article class="module"><h3>Cockpit KPI</h3><p>Vue cabinet dynamique.</p><span><a href="cockpit_kpi_demo.html">Ouvrir →</a></span></article>
        <article class="module"><h3>Cockpit IA</h3><p>Priorisation automatique des dossiers.</p><span><a href="cockpit_ia_premium.html">Ouvrir →</a></span></article>
        <article class="module"><h3>Conformité France</h3><p>TVA, FEC, PDP, audit et traçabilité.</p><span>Prêt</span></article>
        <article class="module"><h3>Production cabinet</h3><p>Workflow, OCR IA, rapprochement bancaire.</p><span>Prêt</span></article>
        <article class="module"><h3>Gestion financière</h3><p>Immobilisations, amortissements, emprunts.</p><span>Prêt</span></article>
        <article class="module"><h3>Pipeline qualité</h3><p>Tests automatisés avant intégration.</p><span>OK</span></article>
      </section>
    </main>
  </div>
</body>
</html>"""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return str(out)

if __name__ == "__main__":
    print(render_portail_demo())
