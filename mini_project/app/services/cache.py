import hashlib
import json
from typing import List, Dict, Optional

_store: Dict[str, str] = {}


def make_key(
    messages: List[Dict[str, str]],
    model: Optional[str],
    temperature: Optional[float],
) -> str:
    payload = json.dumps(
        {"messages": messages, "model": model, "temperature": temperature},
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def get(key: str) -> Optional[str]:
    return _store.get(key)


def set(key: str, value: str) -> None:
    _store[key] = value


def size() -> int:
    return len(_store)
