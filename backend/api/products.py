
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.schemas import ProductQuery, ProductInfo
from services.product_service import ProductService
from core.errors import AppException

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_class=JSONResponse)
async def list_products():
    service = ProductService()
    try:
        products = await service.list_products()
        return products
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
