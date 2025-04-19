from fastapi import FastAPI
from backend.router import delivery, users,login


app=FastAPI()


app.include_router(users.router)
app.include_router(delivery.router)
app.include_router(login.router)





