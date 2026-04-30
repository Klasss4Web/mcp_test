from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from services.order_service import OrderService
from core.errors import AppException

router = APIRouter(prefix="/orders", tags=["orders"])

class CreateOrderRequest(BaseModel):
    customer_id: str
    product_id: str
    quantity: int

@router.post("/")
async def create_order(request: CreateOrderRequest):
    service = OrderService()
    try:
        result = await service.create_order(request.customer_id, request.product_id, request.quantity)
        return result
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.get("/history")
async def order_history(customer_id: str = Query(...)):
    service = OrderService()
    try:
        result = await service.list_orders(customer_id)
        return result
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
