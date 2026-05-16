from flask import Flask
import os
from controllers.User.Zoom import ZoomController

app = Flask(__name__)

@app.route("/")
def home():
    return "Server Running"

@app.route("/zoom")
def zoom():
    return ZoomController.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))