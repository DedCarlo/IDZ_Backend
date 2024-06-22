from pydantic import BaseModel, EmailStr


class OrderBase(BaseModel):
    title: str
    description: str | None = None
    price: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    order_id: int
    owner_id: int

    class Config:
        orm_mode = True


class ServiceBase(BaseModel):
    title: str
    description: str | None = None
    price: int


class ServiceCreate(ServiceBase):
    pass


class Service(ServiceBase):
    service_id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: int
    orders: list[Order] = []
    services: list[Service] = []

    class Config:
        orm_mode = True


class TokenBase(BaseModel):
    pass


class Token(TokenBase):
    access_token: str
    token_type: str


class TokenData(TokenBase):
    username: str | None = None
