from src.db.database import Base
from sqlalchemy import Column, String,Integer,Enum,ForeignKey,Float
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


#table for the deliveries to be stored in the database
class Delivery(Base):
    __tablename__ = 'deliveries'

    id=Column(Integer,primary_key=True)
    customer_id=Column(String,nullable=False)
    customer_phone=Column(String,nullable=False)
    customer_name=Column(String,nullable=False)
    customer_address = Column(String,nullable=False)
    manager_phone=Column(String,nullable=False)
    delivery_type=Column(String,nullable=False)
    status=Column(Enum("delivered", "in-transit", "approve",name="delivery_status"),nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)           #to which user the delivery belongs to
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    predicted_eta_minutes = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)



#table for the users to be stored in the database
class User(Base):
    __tablename__ = 'users'

    id=Column(Integer,primary_key=True)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    role = Column(String, nullable=False, server_default="user")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)



