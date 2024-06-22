from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import auth
import crud
import models
import schemas
from dependencies import get_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    register_user = crud.register_user(db, user)
    return register_user


# Здесь может быть ошибка
@router.post("/token/", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неправильный_логин_или_пароль")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not auth.verify_password(password, user.hashed_password):
        return False
    return user


@router.get("/users/me", response_model=schemas.User)
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = crud.get_current_user(db, token)
    return current_user


def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user
