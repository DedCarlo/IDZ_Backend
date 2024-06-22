from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.user_id", ondelete='CASCADE'), nullable=False)
    price = Column(Integer, nullable=False)
    orders = relationship("User", back_populates="user_orders")


class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.user_id", ondelete='CASCADE'), nullable=False)
    price = Column(Integer, nullable=False)
    services = relationship("User", back_populates="user_services")


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    user_orders = relationship("Order", back_populates="orders")
    user_services = relationship("Service", back_populates="services")
