
from fastapi import FastAPI
from src.router import delivery, users,login,maps
from fastapi.middleware.cors import CORSMiddleware
from src.kafka.admin import create_topic_init
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    
    create_topic_init()
    yield


app=FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",  
    "http://localhost:3000" 
]

#we are allowing cors middleware to allow requests from frontend to backend
app.add_middleware(
    CORSMiddleware,
    #access allow from the following origins
    allow_origins=origins,
    #allow the user to send cookies and auth information  
    allow_credentials=True,
    #allow all methods (GET,POST....)
    allow_methods=["*"],    
    allow_headers=["*"],   
    )

app.include_router(maps.router)
app.include_router(users.router)
app.include_router(delivery.router)
app.include_router(login.router)

@app.get("/")
def root():
    return{"message":"welcome to the smart delivery app"}