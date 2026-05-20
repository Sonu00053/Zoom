from flask import Flask
from threading import Thread
from controllers.User.Zoom import ZoomController

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "alive"}

@app.route("/health")
def health():
    return {"ok": True}

@app.route("/zoom")
def zoom():
    Thread(target=ZoomController.start, daemon=True).start()
    return {"status": "started"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)