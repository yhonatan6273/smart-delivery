
from backend.db.database import Base
from sqlalchemy import Column, String,Integer,Float,Enum
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Delivery(Base):
    __tablename__ = 'deliveries'


    id=Column(Integer,primary_key=True)
    sender_id=Column(String,nullable=False)
    sender_phone=Column(String,nullable=False)
    sender_name=Column(String,nullable=False)
    sender_address = Column(String,nullable=False)
    receiver_phone=Column(String,nullable=False)
    receiver_id=Column(String,nullable=False)
    receiver_name=Column(String,nullable=False)
    receiver_address=Column(String,nullable=False)
    delivery_type=Column(String,nullable=False)
    price=Column(Float,nullable=False)
    status=Column(Enum("delivered", "in-transit", "approve",name="delivery_status"),nullable=False)
    time_of_created=Column(TIMESTAMP(timezone=True),server_default=text("now()"),nullable=False)


class User(Base):
    __tablename__ = 'users'
    id=Column(Integer,primary_key=True)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    time_of_created = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)


