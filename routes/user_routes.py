# routes/user_routes.py
# Minimal version: only /zoom route

from flask import Blueprint

# ---------------- BLUEPRINT ---------------- #
user_bp = Blueprint("user_bp", __name__)

# ---------------- SAFE IMPORT ---------------- #
try:
    from controllers.User.Zoom import ZoomController
except Exception as e:
    print("ZoomController import error:", e)

    class ZoomController:
        @staticmethod
        def start():
            return "ZoomController failed to load"

# ---------------- ZOOM ROUTE ---------------- #
@user_bp.route("/zoom")
def zoom():
    return ZoomController.start()

# ---------------- TEST ROUTE ---------------- #
@user_bp.route("/test")
def test():
    return "user_routes.py loaded successfully"