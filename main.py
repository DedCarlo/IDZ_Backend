from fastapi import FastAPI
from routers import orders, users

app = FastAPI()

app.include_router(orders.router)
app.include_router(users.router)
