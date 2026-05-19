from fastapi import APIRouter
from controllers.User.Zoom import ZoomController

router = APIRouter()

@router.get("/zoom")
def zoom():
    Thread(target=ZoomController.start, daemon=True).start()
    return {"status": "started"}