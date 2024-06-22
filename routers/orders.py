from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import crud
import schemas
from dependencies import get_db

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/orders/all", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders


@router.post("/order/create/", response_model=schemas.OrderCreate)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = crud.get_current_user(db, token)
    return crud.create_order(db, order=order, owner_id=user.user_id)


@router.get("/orders/me", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders