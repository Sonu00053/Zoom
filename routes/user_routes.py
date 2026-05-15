# routes/user_routes.py

from flask import Blueprint, request, render_template, redirect, url_for, session, flash

# ---------------- SAFE IMPORTS ---------------- #
try:
    from controllers.User.Userinfo import UserController
except Exception as e:
    print("UserController import error:", e)

    class UserController:
        @staticmethod
        def register_user(data):
            return {
                "status": False,
                "message": "UserController import failed",
                "redirect": "/register"
            }

        @staticmethod
        def profile():
            return "Profile Page"

        @staticmethod
        def get_users():
            return []

        @staticmethod
        def message():
            return "Message Page"

        @staticmethod
        def upload_status():
            return {"status": True}

        @staticmethod
        def react_message():
            return {"status": True}

        @staticmethod
        def delete_message():
            return {"status": True}

        @staticmethod
        def upload_profile():
            return {"status": True}


try:
    from controllers.User.Zoom import ZoomController
except Exception as e:
    print("ZoomController import error:", e)

    class ZoomController:
        @staticmethod
        def start():
            return "Zoom Page"


try:
    from controllers.User.Auth import LoginController
except Exception as e:
    print("LoginController import error:", e)

    class LoginController:
        @staticmethod
        def login_user(data):
            return {"status": False, "message": "LoginController import failed"}

        @staticmethod
        def logout_user():
            session.clear()


try:
    from controllers.User.Ludo import LudoController
except Exception as e:
    print("LudoController import error:", e)

    class LudoController:
        @staticmethod
        def start_game():
            return "Ludo Game"


try:
    from helpers.auth_helper import login_required
except Exception as e:
    print("login_required import error:", e)

    def login_required():
        def decorator(func):
            return func
        return decorator


# ---------------- BLUEPRINT ---------------- #
user_bp = Blueprint(
    "user_bp",
    __name__,
    template_folder="../templates/User"
)


# ---------------- BASIC TEST ROUTE ---------------- #
@user_bp.route("/register")
def register_page():
    return render_template("register.html", title="Register")


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        response = LoginController.login_user(request.form)
        if response.get("status"):
            return redirect(url_for("user_bp.dashboard"))

        return render_template(
            "login.html",
            title="Login",
            response=response
        )

    return render_template("login.html", title="Login")


@user_bp.route("/dashboard")
@login_required()
def dashboard():
    return render_template("dashboard.html", title="Dashboard")


@user_bp.route("/profile", methods=["GET", "POST"])
@login_required()
def profile_page():
    return UserController.profile()


@user_bp.route("/logout")
def logout():
    LoginController.logout_user()
    return redirect(url_for("user_bp.login"))


@user_bp.route("/users")
@login_required()
def get_users():
    return UserController.get_users()


@user_bp.route("/message", methods=["GET", "POST"])
@login_required()
def message():
    return UserController.message()


@user_bp.route("/upload_status", methods=["POST"])
@login_required()
def upload_status():
    return UserController.upload_status()


@user_bp.route("/react_message", methods=["POST"])
@login_required()
def react_message():
    return UserController.react_message()


@user_bp.route("/delete_message", methods=["POST"])
@login_required()
def delete_message():
    return UserController.delete_message()


@user_bp.route("/upload_profile", methods=["POST"])
@login_required()
def upload_profile():
    return UserController.upload_profile()


@user_bp.route("/ludo")
def ludo_game():
    return LudoController.start_game()


@user_bp.route("/zoom")
def zoom():
    return ZoomController.start()


# ---------------- DEBUG ROUTE ---------------- #
@user_bp.route("/test")
def test():
    return "user_routes.py loaded successfully"