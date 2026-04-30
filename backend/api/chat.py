from fastapi import APIRouter, Depends, HTTPException
from models.schemas import ChatRequest, ChatResponse
from services.chat_service import ChatService
from core.errors import AppException

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    service = ChatService()
    try:
        result = await service.chat(request.user_id, request.message)
        return ChatResponse(**result)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
