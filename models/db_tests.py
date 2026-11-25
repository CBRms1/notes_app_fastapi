from sqlalchemy.orm import sessionmaker
from models import db, User

Session = sessionmaker(bind=db)
session = Session()

users = session.query(User).all()
session.delete_all(users)
session.commit()