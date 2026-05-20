import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "alive"}

# Railway safe entry
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))  # FIX for $PORT issue

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port
    )