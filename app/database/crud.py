from sqlalchemy.orm import Session
from database.models import User
from database import schemas
import bcrypt


def get_user(db: Session, user_login: str):
    return db.query(User).filter(User.login == user_login).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(login=user.login, hashed_pass=bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
