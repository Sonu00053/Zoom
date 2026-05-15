# app.py

# IMPORTANT: eventlet monkey patch MUST be first
import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO, emit
import threading
import time
import os
import traceback

# ---------------- SAFE IMPORTS ---------------- #
try:
    from config.constant import APP_NAME, SECRET_KEY
except Exception:
    print("Error importing config.constant:")
    traceback.print_exc()
    APP_NAME = "Zoom App"
    SECRET_KEY = "secret-key"

try:
    from routes.user_routes import user_bp
except Exception:
    print("Error importing routes.user_routes:")
    traceback.print_exc()
    user_bp = None

try:
    from routes.site_routes import site_bp
except Exception:
    print("Error importing routes.site_routes:")
    traceback.print_exc()
    site_bp = None

try:
    from controllers.User.Userinfo import UserController
except Exception:
    print("Error importing UserController:")
    traceback.print_exc()

    class DummyUserController:
        @staticmethod
        def UpdateStatus():
            print("Dummy UpdateStatus executed")

    UserController = DummyUserController


# ---------------- FLASK APP ---------------- #
app = Flask(__name__)
app.secret_key = SECRET_KEY

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)


# ---------------- AUTO CRON ---------------- #
def auto_cron_loop():
    while True:
        try:
            with app.app_context():
                print("AutoCron running...")
                UserController.UpdateStatus()
                socketio.emit("cron_update", {"msg": "Cron executed"})
        except Exception:
            print("AutoCron Error:")
            traceback.print_exc()

        eventlet.sleep(5)   # use eventlet.sleep instead of time.sleep


# ---------------- SOCKET EVENTS ---------------- #
@socketio.on("call_user")
def call_user(data):
    emit("incoming_call", data, broadcast=True)


@socketio.on("answer_call")
def answer_call(data):
    emit("call_answered", data, broadcast=True)


@socketio.on("webrtc_offer")
def webrtc_offer(data):
    emit("webrtc_offer", data, broadcast=True)


@socketio.on("webrtc_answer")
def webrtc_answer(data):
    emit("webrtc_answer", data, broadcast=True)


@socketio.on("webrtc_ice")
def webrtc_ice(data):
    emit("webrtc_ice", data, broadcast=True)


@socketio.on("start_audio_call")
def start_audio_call():
    emit("incoming_audio_call", broadcast=True, include_self=False)


@socketio.on("start_video_call")
def start_video_call():
    emit("incoming_video_call", broadcast=True, include_self=False)


# ---------------- BLUEPRINT REGISTRATION ---------------- #
if user_bp:
    app.register_blueprint(user_bp)

if site_bp:
    app.register_blueprint(site_bp)


# ---------------- TEMPLATE GLOBALS ---------------- #
@app.context_processor
def inject_constants():
    return {"APP_NAME": APP_NAME}


# ---------------- HEALTH CHECK ---------------- #
@app.route("/health")
def health():
    return {
        "status": "ok",
        "app": APP_NAME
    }


# ---------------- ROOT ROUTE ---------------- #
@app.route("/")
def home():
    return f"{APP_NAME} is running successfully!"


# ---------------- START BACKGROUND THREAD ---------------- #
socketio.start_background_task(auto_cron_loop)


# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting server on port {port}...")

    socketio.run(
        app,
        host="0.0.0.0",
        port=port,
        debug=False
    )