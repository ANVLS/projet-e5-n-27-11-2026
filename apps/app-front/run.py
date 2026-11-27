import os
import socket
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Portail Front - n-27-11-2026</title>
  <style>
    body { font-family: system-ui, sans-serif; background: #0f172a; color: #f8fafc; padding: 2rem; }
    .box { max-width: 700px; margin: auto; background: #1e293b; padding: 2rem; border-radius: 12px; border: 1px solid #334155; }
    code { background: #334155; padding: 3px 8px; border-radius: 4px; color: #38bdf8; }
  </style>
</head>
<body>
  <div class="box">
    <h1>Portail Microservice Front (<code>/front</code>)</h1>
    <p>Application déployée dans le namespace <code>ns-apps-n-27-11-2026</code></p>
    <ul>
      <li><strong>Pod actif (Load Balancing) :</strong> <code>{{ pod }}</code></li>
      <li><strong>Environnement :</strong> <code>{{ env }}</code></li>
    </ul>
    <p>Actualise la page (F5) pour observer la répartition de charge entre les 3 réplicas.</p>
  </div>
</body>
</html>
"""

@app.route("/")
@app.route("/front")
@app.route("/front/")
def front():
    return render_template_string(
        HTML,
        pod=socket.gethostname(),
        env=os.environ.get("APP_ENV", "production")
    )
