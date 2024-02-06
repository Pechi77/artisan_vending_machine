from sqlalchemy.orm import Session
from app import models, schemas

def create_product(db: Session, product: schemas.product.ProductCreate, user_id: int):
    # Your logic to create a product
    new_product = models.product.Product(name=product.name, price=product.price, stock=product.stock, seller_id=user_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# Other service functions...
