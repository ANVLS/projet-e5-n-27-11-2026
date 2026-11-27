import os
import socket
import stripe
from flask import Flask, render_template_string, request, redirect, jsonify

app = Flask(__name__)
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_PK = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
DEMO_MODE = os.environ.get("DEMO_MODE", "True")

HTML = """
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>E-Commerce Stripe - {{ tag }}</title>
  <style>
    body { font-family: system-ui, sans-serif; background: #f4f6f9; margin: 0; padding: 2rem; }
    .container { max-width: 800px; margin: auto; background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    .badge { background: #e3f2fd; color: #0d47a1; padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; }
    .card { border: 1px solid #e0e0e0; padding: 1.5rem; border-radius: 8px; margin-top: 1.5rem; display: flex; justify-content: space-between; align-items: center; }
    button { background: #635bff; color: white; border: none; padding: 12px 24px; border-radius: 6px; font-size: 1rem; cursor: pointer; font-weight: bold; }
    button:hover { background: #4b45c6; }
  </style>
</head>
<body>
  <div class="container">
    <span class="badge">Pod : {{ pod }} | Mode Démo : {{ demo }}</span>
    <h1>Boutique E-Commerce Critique (7M€/an)</h1>
    <p>Passerelle de paiement <strong>Stripe Checkout</strong> alimentée par Kubernetes <code>Secret</code> et <code>ConfigMap</code>.</p>
    {% if status == 'success' %}
      <div style="background:#e8f5e9;color:#1b5e20;padding:1rem;border-radius:8px;">✅ Paiement Stripe validé avec succès !</div>
    {% elif status == 'cancel' %}
      <div style="background:#ffebee;color:#b71c1c;padding:1rem;border-radius:8px;">❌ Paiement annulé.</div>
    {% endif %}
    <div class="card">
      <div>
        <h3>Serveur Rack Haute Disponibilité Pro</h3>
        <p>Architecture résiliente Kubernetes &amp; Envoy Gateway</p>
        <strong>149,00 € TTC</strong>
      </div>
      <form action="/create-checkout-session" method="POST">
        <button type="submit">Payer avec Stripe</button>
      </form>
    </div>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(
        HTML,
        pod=socket.gethostname(),
        demo=DEMO_MODE,
        tag="n-27-11-2026",
        status=request.args.get("status", "")
    )

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    if not stripe.api_key or not stripe.api_key.startswith("sk_test_"):
        return jsonify({"error": "Clé STRIPE_SECRET_KEY manquante ou invalide dans le Secret Kubernetes"}), 500
    host_url = request.host_url.rstrip("/")
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "eur",
                "product_data": {"name": "Serveur Rack Haute Disponibilité Pro"},
                "unit_amount": 14900,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"{host_url}/?status=success",
        cancel_url=f"{host_url}/?status=cancel",
    )
    return redirect(session.url, code=303)
