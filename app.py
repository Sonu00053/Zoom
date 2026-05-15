# app.py
from flask import Flask
import os

app = Flask(__name__)
app.secret_key = "zdhWopMNouuQkXAm79M54f82mEhUv7wk7"

# Import blueprint safely
try:
    from routes.user_routes import user_bp
    app.register_blueprint(user_bp)
except Exception as e:
    print("Blueprint import error:", e)

# Home route
@app.route("/")
def home():
    return "Zoom Automation Server is Running!"

# Health route
@app.route("/health")
def health():
    return {"status": "ok"}

# Required for local testing
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)