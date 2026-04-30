from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    user_id: Optional[str]
    message: str

class ChatResponse(BaseModel):
    response: str
    context: Optional[dict] = None

class AuthRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    user_id: str
    token: str

class ProductQuery(BaseModel):
    product_id: Optional[str] = None
    name: Optional[str] = None

class ProductInfo(BaseModel):
    product_id: str
    name: str
    available: bool
    price: float

class OrderRequest(BaseModel):
    user_id: str
    product_id: str
    quantity: int

class OrderResponse(BaseModel):
    order_id: str
    status: str
    details: Optional[dict] = None
