from fastapi import FastAPI
from src.router import delivery, users,login,maps


app=FastAPI()



app.include_router(maps.router)
app.include_router(users.router)
app.include_router(delivery.router)
app.include_router(login.router)