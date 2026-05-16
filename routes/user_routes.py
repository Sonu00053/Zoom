# routes/user_routes.py

from flask import Blueprint
from controllers.User.Zoom import ZoomController

# Create Blueprint
user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/zoom")
def zoom():
    """
    Run Zoom automation.
    Example:
    https://your-app.onrender.com/zoom
    """
    return ZoomController.start()


@user_bp.route("/test")
def test():
    """
    Test route to verify blueprint is loaded.
    """
    return "user_routes.py loaded successfully"