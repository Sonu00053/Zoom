# app.py

from flask import Flask
import os

app = Flask(__name__)
app.secret_key = "WW8jhK8V79ErRDn5pr7ic4xwe7ZldPbr"

# Register blueprint
from routes.user_routes import user_bp
app.register_blueprint(user_bp)


@app.route("/")
def home():
    return "Zoom Automation Server is Running!"


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )