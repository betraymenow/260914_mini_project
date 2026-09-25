import logging
from typing import AsyncIterator, List, Dict, Optional
from openai import AsyncOpenAI
from app.core.config import API_KEY, MODEL, BASE_URL

logger = logging.getLogger(__name__)


def get_client() -> AsyncOpenAI:
    if BASE_URL:
        return AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)
    return AsyncOpenAI(api_key=API_KEY)


_client = get_client()


async def stream_chat(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    timeout: float = 10.0,
) -> AsyncIterator[str]:
    use_model = model or MODEL
    use_temp = temperature if temperature is not None else 1.0
    logger.info("llm call start | model=%s temperature=%.2f", use_model, use_temp)

    stream = await _client.chat.completions.create(
        model=use_model,
        messages=messages,
        temperature=use_temp,
        stream=True,
        timeout=timeout,
    )
    count = 0
    async for chunk in stream:
        if not chunk.choices:
            continue
        piece = getattr(chunk.choices[0].delta, "content", None)
        if not piece:
            continue
        count += 1
        yield piece
    logger.info("llm call end | pieces=%d", count)
