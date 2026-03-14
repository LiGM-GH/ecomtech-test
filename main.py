from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"whatever": "Whatever with big W"}
