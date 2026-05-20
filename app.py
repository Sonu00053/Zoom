import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "alive"}

# Railway safe entrypoint
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))  # ✅ FIX FOR $PORT ERROR

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )