# app.py
from fastapi import FastAPI
from controllers.User.Zoom import ZoomController

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
    return ZoomController.start()