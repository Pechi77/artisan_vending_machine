from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from artisan_vending_machine.app.database import Base



class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    price = Column(Float)
    stock = Column(Integer)
    seller_id = Column(Integer, ForeignKey("users.id"))

    seller = relationship("User", back_populates="products")
