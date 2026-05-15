from flask import Flask
from flask_socketio import SocketIO, emit
import threading
import time
import os

from config.constant import APP_NAME, SECRET_KEY
from routes.user_routes import user_bp
from routes.site_routes import site_bp
# from routes.ludo_routes import ludo_bp
from controllers.User.Userinfo import UserController

# ---------------- FLASK APP ---------------- #

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Flask-SocketIO setup
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
        except Exception as e:
            print(f"AutoCron Error: {e}")

        # Har 1 second baad run
        time.sleep(1)

# Background thread start
threading.Thread(target=auto_cron_loop, daemon=True).start()

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

# ---------------- BLUEPRINTS ---------------- #

app.register_blueprint(user_bp)
app.register_blueprint(site_bp)
# app.register_blueprint(ludo_bp)

# ---------------- TEMPLATE GLOBALS ---------------- #

@app.context_processor
def inject_constants():
    return {
        "APP_NAME": APP_NAME
    }

# ---------------- HEALTH CHECK ROUTE ---------------- #

@app.route("/health")
def health():
    return {
        "status": "ok",
        "app": APP_NAME
    }

# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))

    socketio.run(
        app,
        host="0.0.0.0",
        port=port,
        debug=False
    )