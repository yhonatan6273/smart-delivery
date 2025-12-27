from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os
from dotenv import load_dotenv


load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOSTNAME")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DB}"


if not SQLALCHEMY_DATABASE_URL:
    raise Exception("DATABASE_URL not found")
# Engine will manage the connection pool to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal  will create new Session objects when called
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# base will be the base class for all our models
# he will inherit from all our models
Base = declarative_base()
#this function will be used as a dependency in the routes to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()