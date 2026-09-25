from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest
from app.services.chat_service import stream_chat_safe

router = APIRouter()

@router.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    return StreamingResponse(stream_chat_safe(req), media_type="text/plain")
