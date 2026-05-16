# routes/user_routes.py

from flask import Blueprint
from controllers.User.Zoom import ZoomController
user_bp = Blueprint("user_bp", __name__)
@user_bp.route("/zoom")
def zoom():
    return ZoomController.start()