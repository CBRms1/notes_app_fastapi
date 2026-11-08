from fastapi import APIRouter

notes_router = APIRouter(prefix="/notes", tags={"NOTES"})

@notes_router.get("/")
async def root():
    return {"message": "notes root"}