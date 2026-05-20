import os
from fastapi import FastAPI
from routes.user_routes import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def home():
    return {"status": "alive"}

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port
    )