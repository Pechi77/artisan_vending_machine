from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from artisan_vending_machine.app.schemas import product
from artisan_vending_machine.app.schemas import user
from artisan_vending_machine.app.services import product_service
from artisan_vending_machine.app.database import get_db
from typing import List
from artisan_vending_machine.app.core.auth import get_current_user
router = APIRouter()


@router.get("/products/", response_model=List[product.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = product_service.get_products(db, skip=skip, limit=limit)
    return products


@router.post("/products/", response_model=product.Product)
def create_product_for_user(product: product.ProductCreate, db: Session = Depends(get_db), current_user: user.User = Depends(get_current_user)):
    return product_service.create_product(db=db, product=product, user_id=current_user.id)


@router.put("/products/{product_id}", response_model=product.Product)
def update_product(product_id: int, product: product.ProductUpdate, db: Session = Depends(get_db), current_user: user.User = Depends(get_current_user)):
    updated_product = product_service.update_product(db, product_id, product, current_user.id)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found or not authorized to update")
    return updated_product

@router.delete("/products/{product_id}", response_model=product.Product)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: user.User = Depends(get_current_user)):
    success = product_service.delete_product(db, product_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found or not authorized to delete")
    return {"detail": "Product deleted successfully"}