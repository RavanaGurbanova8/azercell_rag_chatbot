# backend/app/routes/chat.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
from app.services.bedrock_runtime import stream_deltas, invoke_non_stream
from app.services.kb_runtime import get_kb_context

router = APIRouter()

@router.get("/test")
async def test():
    return {"msg": "Chat router works"}

class ChatIn(BaseModel):
    prompt: str
    system: Optional[str] = None
    temperature: float = 0.5
    max_tokens: int = 1024
    use_kb: bool = True
    stream: bool = True

@router.post("/chat")
async def chat(inp: ChatIn):
    context = ""
    if inp.use_kb:
        kb_text = get_kb_context(inp.prompt)
        if kb_text:
            context = f"\n\nRelevant context from Knowledge Base:\n{kb_text}\n\n"

    messages = [{"role": "user", "content": f"{context}{inp.prompt}"}]

    text = invoke_non_stream(
        messages=messages,
        system=inp.system,
        temperature=inp.temperature,
        max_tokens=inp.max_tokens,
    )
    return JSONResponse({"answer": text})

@router.post("/chat/stream")
async def chat_stream(inp: ChatIn):
    context = ""
    if inp.use_kb:
        kb_text = get_kb_context(inp.prompt)
        if kb_text:
            context = f"\n\nRelevant context from Knowledge Base:\n{kb_text}\n\n"

    messages = [{"role": "user", "content": f"{context}{inp.prompt}"}]

    generator = stream_deltas(
        messages=messages,
        system=inp.system,
        temperature=inp.temperature,
        max_tokens=inp.max_tokens,
    )
    return StreamingResponse(generator, media_type="text/plain; charset=utf-8")
