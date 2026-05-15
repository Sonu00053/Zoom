# app.py
# Minimal version: only website + /zoom route

import eventlet
eventlet.monkey_patch()

from flask import Flask
import os
import traceback

# ---------------- APP CONFIG ---------------- #
APP_NAME = "uufDlinITqq0N044urKq2g"
SECRET_KEY = "dhWopMNouuQkXAm79M54f82mEhUv7wk7"

# ---------------- SAFE IMPORT ---------------- #
try:
    from routes.user_routes import user_bp
except Exception:
    print("Error importing routes.user_routes:")
    traceback.print_exc()
    user_bp = None

# ---------------- FLASK APP ---------------- #
app = Flask(__name__)
app.secret_key = SECRET_KEY

# ---------------- REGISTER BLUEPRINT ---------------- #
if user_bp:
    app.register_blueprint(user_bp)

# ---------------- ROOT ROUTE ---------------- #
@app.route("/")
def home():
    return f"{APP_NAME} is running successfully!"

# ---------------- HEALTH ROUTE ---------------- #
@app.route("/health")
def health():
    return {
        "status": "ok",
        "app": APP_NAME
    }

# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)