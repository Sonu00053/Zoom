from fastapi import FastAPI
from threading import Thread
from controllers.User.Zoom import ZoomController
import traceback

app = FastAPI(
    title="Zoom Automation API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Zoom Automation Server is Running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/zoom")
def zoom():
    try:
        Thread(
            target=ZoomController.start,
            daemon=True
        ).start()

        return {
            "status": "started",
            "message": "Zoom bot started in background"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }