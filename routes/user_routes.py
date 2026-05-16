# routes/user_routes.py
from fastapi import APIRouter
from controllers.User.Zoom import ZoomController

router = APIRouter()


@router.get("/zoom")
def zoom():
    return ZoomController.start()