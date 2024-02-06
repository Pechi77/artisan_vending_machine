from pydantic import BaseModel, EmailStr, constr, validator

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=20)

class UserCreate(UserBase):
    email: EmailStr
    password: constr(min_length=6)
    role: str

    @validator('role')
    def validate_role(cls, role):
        if role not in ["seller", "buyer"]:
            raise ValueError('Invalid Role')
        return role

class UserUpdate(BaseModel):
    email: EmailStr = None
    password: constr(min_length=6) = None

class UserInDBBase(UserBase):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str
