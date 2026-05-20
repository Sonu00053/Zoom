import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "alive"}

@app.get("/health")
def health():
    return {"ok": True}


# 🔥 IMPORTANT: Railway safe start
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port
    )