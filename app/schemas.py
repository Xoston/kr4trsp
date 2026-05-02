from pydantic import BaseModel, EmailStr, constr, ConfigDict
from typing import Optional

# ---------- Product схемы ----------
class ProductBase(BaseModel):
    title: str
    price: float
    count: int

class ProductCreate(ProductBase):
    description: str

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    count: Optional[int] = None
    description: Optional[str] = None

class Product(ProductBase):
    id: int
    description: str

    model_config = ConfigDict(from_attributes=True)

# ---------- User схемы ----------
class User(BaseModel):
    username: str
    age: int                     # теперь без ограничения, проверяем в эндпоинте
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = 'Unknown'

class UserOut(BaseModel):
    username: str
    age: int
    email: str
    phone: str