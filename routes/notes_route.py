# notes route

from fastapi import APIRouter, Depends
from schemas import NoteSchema
from dependencies import get_session
from models import Note
from sqlalchemy.orm import Session

notes_router = APIRouter(prefix="/notes", tags={"NOTES"})

@notes_router.get("/")
async def root():
    return {"message": "notes root"}

@notes_router.post("/create")
async def create(note_schema: NoteSchema, session: Session=Depends(get_session)):
    new_note = Note(
        title=note_schema.title,
        description=note_schema.description,
        user_id=note_schema.user_id
    )

    session.add(new_note)
    session.commit()
    return {"message": f"New note created! Note id: {new_note.id}"}