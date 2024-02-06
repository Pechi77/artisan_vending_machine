from pydantic import BaseModel, validator

class Deposit(BaseModel):
    amount: int

    @validator('amount')
    def validate_amount(cls, v):
        if v not in [5, 10, 20, 50, 100]:
            raise ValueError('Invalid coin denomination')
        return v
