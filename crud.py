from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import status
import models
import schemas
import auth


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def register_user(db: Session, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.email == user.email) .first()
    if db_user:
        raise HTTPException(status_code=400, detail="Почта уже зарегистрирована")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(nick_name=user.nick_name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_current_user(db: Session, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_service(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id).first()


def get_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_order(db: Session, order: schemas.OrderCreate, owner_id: int):
    db_order = models.Order(**order.dict(), owner_id=owner_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def create_service(db: Session, service: schemas.ServiceCreate, owner_id: int):
    db_service = models.Service(**service.dict(), owner_id=owner_id)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service
    