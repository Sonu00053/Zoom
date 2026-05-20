from fastapi import APIRouter
from threading import Thread
from controllers.User.Zoom import ZoomController

router = APIRouter()

@app.route("/zoom")
def zoom():
    import threading

    print("ROUTE HIT /zoom")

    try:
        t = threading.Thread(target=ZoomController.start)
        t.start()
        print("THREAD STARTED")
    except Exception as e:
        print("THREAD ERROR:", e)

    return {"status": "started"}