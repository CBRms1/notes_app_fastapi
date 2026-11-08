from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags={"AUTH"})

@auth_router.get("/")
async def root():
    return {"message": "auth root"}