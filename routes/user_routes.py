from flask import Blueprint
from threading import Thread
from controllers.User.Zoom import ZoomController

zoom_bp = Blueprint("zoom", __name__)

@zoom_bp.route("/zoom")
def zoom():
    print("ROUTE HIT /zoom")

    Thread(target=ZoomController.start).start()

    return {"status": "started"}