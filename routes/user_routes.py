from flask import Blueprint
from threading import Thread
from controllers.User.Zoom import ZoomController

zoom_bp = Blueprint("zoom", __name__)

@zoom_bp.route("/zoom")
def zoom():
    print("🔥 ROUTE HIT /zoom")

    try:
        t = Thread(target=ZoomController.start)
        t.start()
        print("🚀 THREAD STARTED")
    except Exception as e:
        print("❌ THREAD ERROR:", e)

    return {"status": "started"}