from fastapi import FastAPI
from routes.user_routes import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def home():
    return {"status": "alive"}