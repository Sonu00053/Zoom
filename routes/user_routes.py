from fastapi import APIRouter
from threading import Thread
from controllers.User.Zoom import ZoomController

router = APIRouter()

@router.get("/zoom")
def zoom():
    Thread(target=ZoomController.start, daemon=True).start()
    return {"status": "started"}