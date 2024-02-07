from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True)
    email = Column(String(100))
    hashed_password = Column(String(200))
    role = Column(String(6))
    balance = Column(Float, default=0.0)

    products = relationship("Product", back_populates="seller")
