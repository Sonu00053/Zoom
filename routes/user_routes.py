from flask import Blueprint
from controllers.User.Zoom import ZoomController

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/zoom")
def zoom():
    return ZoomController.start()


@user_bp.route("/test")
def test():
    return "user_routes.py loaded successfully"