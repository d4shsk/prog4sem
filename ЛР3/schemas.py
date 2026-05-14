from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class CurrencyBase(BaseModel):
    code: str
    name: str

class CurrencyOut(CurrencyBase):
    id: int
    rate: Optional[float] = None

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class UserOut(UserBase):
    id: int
    created_at: datetime
    subscribed_currencies: List[CurrencyOut] = []

    class Config:
        from_attributes = True

class SubscriptionCreate(BaseModel):
    user_id: int
    currency_code: str
