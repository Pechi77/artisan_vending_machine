from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.schemas import product
from app.schemas import user
from app.services import product_service
from app.database import get_db
from app.core.auth import get_current_user
router = APIRouter()

@router.post("/products/", response_model=product.Product)
def create_product_for_user(product: product.ProductCreate, db: Session = Depends(get_db), current_user: user.User = Depends(get_current_user)):
    return product_service.create_product(db=db, product=product, user_id=current_user.id)

