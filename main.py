from fastapi import FastAPI
from api.routes import router

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Ad Analytics API running"}

app.include_router(router)
