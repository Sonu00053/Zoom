import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "alive"}

if __name__ == "__main__":
    import uvicorn

    # 🔥 IMPORTANT FIX
    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port
    )