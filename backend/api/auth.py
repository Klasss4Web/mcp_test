from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.schemas import AuthRequest, AuthResponse
from services.auth_service import AuthService
from core.errors import AppException

router = APIRouter(prefix="/auth", tags=["auth"])

class CustomerRequest(BaseModel):
    email: str

class VerifyPinRequest(BaseModel):
    customer_id: str
    pin: str

@router.post("/login", response_model=AuthResponse)
async def login(request: AuthRequest):
    service = AuthService()
    try:
        result = await service.authenticate(request.email, request.password)
        return AuthResponse(**result)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.post("/customer")
async def get_customer(request: CustomerRequest):
    service = AuthService()
    try:
        result = await service.get_customer(request.email)
        return result
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.post("/verify-pin")
async def verify_pin(request: VerifyPinRequest):
    service = AuthService()
    try:
        result = await service.verify_customer_pin(request.customer_id, request.pin)
        return result
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
