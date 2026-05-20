from fastapi import FastAPI
from routes.user_routes import router

app = FastAPI(title="Zoom Automation API", version="1.0.0")

app.include_router(router)


@app.get("/")
def home():
    return {"status": "ok"}