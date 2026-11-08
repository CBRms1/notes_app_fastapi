from fastapi import FastAPI
from auth_route import auth_router

app = FastAPI()
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Hello world"}