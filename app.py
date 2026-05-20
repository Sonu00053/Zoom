from fastapi import FastAPI
from routes.user_routes import router as user_router

app = FastAPI()

@app.get("/")
def home():
    return {"status": "alive"}

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(user_router)