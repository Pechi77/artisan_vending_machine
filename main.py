from fastapi import FastAPI
from app.routes import user, product, transaction

from app.database import engine, Base

app = FastAPI()

def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()

app.include_router(user.router)
app.include_router(product.router)
app.include_router(transaction.router)
