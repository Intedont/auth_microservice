
from fastapi import FastAPI, Depends, HTTPException, status
from requests import Session
import uvicorn
from pydantic import BaseModel
from jose import jwt
from database.crud import create_user, get_user
from database.db import engine, SessionLocal
from passlib.context import CryptContext
from database.schemas import User, UserCreate
from config import SECRET_KEY, ALGORITHM

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Login_form(BaseModel):
    login: str
    password: str

class Signup_form(BaseModel):
    login: str
    password: str
    name: str
    phone: int


def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


@app.get('/')
async def root():
    return {'message': 'hello world'}


@app.post('/login')
async def login(form_data: Login_form, db: Session = Depends(get_db)):
    user = get_user(db, form_data.login)
    if not user or not pwd_context.verify(form_data.password, user.hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({'username': user.login})
    return {'access_token': access_token}


@app.post("/signup", response_model=User)
def signup_user(form_data: Signup_form, db: Session = Depends(get_db)):
    return create_user(db, UserCreate.parse_obj(form_data))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)