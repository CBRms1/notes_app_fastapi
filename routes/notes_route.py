# notes route

from fastapi import APIRouter, Depends, HTTPException
from schemas import NoteSchema
from dependencies import get_session
from models.models import Note, User
from sqlalchemy.orm import Session
from dependencies import verify_token

notes_router = APIRouter(prefix="/notes", tags={"NOTES"}, dependencies=[Depends(verify_token)])

@notes_router.get("/")
async def root():
    return {"message": "notes root"}

@notes_router.post("/create")
async def create(note_schema: NoteSchema, session: Session=Depends(get_session), user: User=Depends(verify_token)):
    new_note = Note(
        title=note_schema.title,
        description=note_schema.description,
        user_id=user.id
    )

    session.add(new_note)
    session.commit()
    return {"message": f"New note created! Note id: {new_note.id}"}

@notes_router.delete("/delete")
async def delete(note_id, session: Session=Depends(get_session), user: User=Depends(verify_token)):
    note = session.query(Note).filter(Note.id==note_id).first()

    if note.user_id != user.id:
        raise HTTPException(status_code=401, detail="Access danied")
    else:
        session.delete(note)
        session.commit()

        return {"message": "note deleted"}