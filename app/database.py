from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from artisan_vending_machine.app.constants import MYSQL_DATABASE_URL
print(MYSQL_DATABASE_URL)
engine = create_engine(MYSQL_DATABASE_URL,pool_pre_ping=True 
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()