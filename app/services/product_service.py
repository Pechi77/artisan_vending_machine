from fastapi import HTTPException
from sqlalchemy.orm import Session

from artisan_vending_machine.app import schemas
from artisan_vending_machine.app.models.product import Product
from artisan_vending_machine.app.models.user import User



def create_product(db: Session, product: schemas.product.ProductCreate, user_id: int):
    # Your logic to create a product
    new_product = Product(name=product.name, price=product.price, stock=product.stock, seller_id=user_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def update_product(db: Session, product_id: int, product: schemas.product.ProductUpdate, seller_id: int):
    db_product = db.query(Product).filter(Product.id == product_id, Product.seller_id == seller_id).first()
    if db_product:
        for var, value in vars(product).items():
            setattr(db_product, var, value) if value else None
        db.commit()
        db.refresh(db_product)
        return db_product
    return None

def delete_product(db: Session, product_id: int, seller_id: int):
    db_product = db.query(Product).filter(Product.id == product_id, Product.seller_id == seller_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False


def calculate_change(balance):
    # Denominations in cents
    denominations = [100, 50, 20, 10, 5]
    change = []

    for denomination in denominations:
        while balance >= denomination:
            balance -= denomination
            change.append(denomination)
    
    # Optionally, to return the change in a more structured format:
    change_summary = {denomination: change.count(denomination) for denomination in denominations if change.count(denomination) > 0}

    return change_summary


def buy_product(db: Session, user_id: int, product_id: int, quantity: int):
    user = db.query(User).filter(User.id == user_id).first()
    product = db.query(Product).filter(Product.id == product_id).first()

    if not user or user.role != "buyer":
        raise HTTPException(status_code=403, detail="Only buyers can perform this operation")

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_cost = product.price * quantity
    if user.balance < total_cost:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    user.balance -= total_cost
    

    db.commit()


    change = calculate_change(user.balance)

    return {"total_spent": total_cost, "products_purchased": [{"product_id": product_id, "quantity": quantity}], "change": change}