from flask import Blueprint

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/test")
def test():
    return "Blueprint is working"

@user_bp.route("/register")
def register():
    return "Register is working"