# routes/user_routes.py
from flask import Blueprint

# Blueprint must be created before using @user_bp.route
user_bp = Blueprint("user_bp", __name__)

# Safe import for Zoom controller
try:
    from controllers.User.Zoom import ZoomController
except Exception as e:
    print("ZoomController import error:", e)

    class ZoomController:
        @staticmethod
        def start():
            return "ZoomController import failed"

# Zoom route
@user_bp.route("/zoom")
def zoom():
    return ZoomController.start()

# Test route
@user_bp.route("/test")
def test():
    return "user_routes.py loaded successfully"