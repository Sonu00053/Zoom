from flask import Flask
from routes.user_routes import zoom_bp

app = Flask(__name__)

app.register_blueprint(zoom_bp)

@app.route("/")
def home():
    return {"status": "alive"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)