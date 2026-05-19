from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "success", "message": "Railway app is running"}

@app.get("/zoom")
def zoom():
    return {"message": "Zoom endpoint working"}