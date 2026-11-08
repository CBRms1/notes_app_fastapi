from fastapi import FastAPI
from auth_route import auth_router
from notes_route import notes_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(notes_router)

@app.get("/")
async def root():
    return {"message": "Hello world"}