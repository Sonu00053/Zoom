import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "server working"}

@app.get("/health")
def health():
    return {"ok": True}