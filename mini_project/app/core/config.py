import os
from dotenv import load_dotenv

load_dotenv()

API_KEY  = os.getenv("MLAPI_API_KEY")
MODEL    = os.getenv("MLAPI_MODEL", "openai/gpt-4o-mini")
BASE_URL = os.getenv("MLAPI_BASE_URL", "https://mlapi.run/40cc17ae-a89b-4f12-a7d6-13293180fc87/v1")

if not API_KEY:
    raise RuntimeError("MLAPI_API_KEY가 설정되어 있지 않습니다. .env 파일을 확인하세요.")
