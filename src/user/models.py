from sqlalchemy import Column, Integer, String, Boolean, DateTime
from src.utils.db import Base

class UserModel(Base):
    __tablename__ = "user_table"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    hash_password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)