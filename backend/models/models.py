from backend.db.database import Base
from sqlalchemy import Column, String,Integer,Float,Enum,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


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
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time_of_created = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)



class User(Base):
    __tablename__ = 'users'

    id=Column(Integer,primary_key=True)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    role = Column(String, nullable=False, server_default="user")
    time_of_created = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)


