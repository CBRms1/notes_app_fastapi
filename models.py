from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# create db
db = create_engine('sqlite:///notesdb.db')

# declarative base
Base = declarative_base()

# create class
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    #relationship
    notes = relationship("Note", back_populates="author")


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    # relationship
    author = relationship("User", back_populates="notes")


# execute metadata to db