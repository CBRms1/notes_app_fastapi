# include routers and start app

from fastapi import FastAPI

app = FastAPI()

from routes.auth_route import auth_router
from routes.notes_route import notes_router

app.include_router(auth_router)
app.include_router(notes_router)

@app.get("/")
async def root():
    return {"message": "Hello world"}