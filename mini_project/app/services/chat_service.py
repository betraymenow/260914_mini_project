import asyncio
import logging
import time
from typing import AsyncIterator
from app.schemas.chat import ChatRequest
from app.clients.openai_client import stream_chat
from app.prompts.system_prompt import SYSTEM_PROMPT
from app.services import cache

logger = logging.getLogger(__name__)


def _build_messages(req: ChatRequest):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": req.message},
    ]


async def stream_chat_safe(req: ChatRequest) -> AsyncIterator[str]:
    started = time.time()
    messages = _build_messages(req)
    key = cache.make_key(messages, req.model, req.temperature)
    hit = cache.get(key)

    if hit is not None:
        logger.info("cache HIT | key=%s | size=%d", key[:8], cache.size())
        yield hit
        yield "\n[DONE]"
        logger.info("request done (cache) | elapsed=%dms", int((time.time() - started) * 1000))
        return

    logger.info("cache MISS | key=%s", key[:8])
    produced = False
    buffer = []
    try:
        async for piece in stream_chat(
            messages=messages,
            model=req.model,
            temperature=req.temperature,
        ):
            produced = True
            buffer.append(piece)
            yield piece
        if produced:
            full = "".join(buffer)
            cache.set(key, full)
            logger.info("cache STORE | key=%s | size=%d", key[:8], cache.size())
            yield "\n[DONE]"
        else:
            yield "[EMPTY]"
            yield "\n"
    except asyncio.CancelledError:
        logger.warning("cancelled by client")
        raise
    except Exception as e:
        logger.error("llm error | %s: %s", type(e).__name__, e)
        yield f"[ERROR] {type(e).__name__}: {e}"
        yield "\n"
    finally:
        logger.info("request done | elapsed=%dms", int((time.time() - started) * 1000))
