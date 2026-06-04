from sqlalchemy import Integer,String,Column,ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from datetime import datetime
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    email = Column(String)
    hashed_password = Column(String)
    expenses = relationship("Expenses",back_populates="user")
class Expenses(Base):
    __tablename__="expenses"
    id = Column(Integer,primary_key=True)
    title = Column(String)
    amount = Column(Integer)
    category = Column(String)
    created_at = Column(DateTime,default=datetime.utcnow)
    owner_id = Column(Integer,ForeignKey("users.id"))
    user = relationship("Users",back_populates="expenses")
    