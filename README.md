# AI 커리큘럼 학습 도우미 챗봇

이어드림스쿨 6기 [AI 실무 기본] AI 서비스 개발자 과정 5일차 미니 프로젝트입니다.
FastAPI 기반 레이어드 아키텍처 위에, LLM 스트리밍 응답 · 캐싱 · 로깅을 갖춘 도메인 챗봇 API를 구현했습니다.

## 도메인

**이어드림스쿨 AI 서비스 개발자 커리큘럼 학습 도우미** — SQL, FastAPI, LangChain, HuggingFace, LangGraph 같은
커리큘럼 개념을 초보자도 이해하기 쉽게 비유와 짧은 예시로 설명해주는 학습 조교 챗봇입니다.

## 프로젝트 구조

```
mini_project/
  app/
    core/
      config.py            # 환경 변수 로드 (.env)
      logging_config.py    # 로깅 설정
    schemas/
      chat.py               # ChatRequest 요청 모델
    clients/
      openai_client.py      # LLM 스트리밍 호출 (OpenAI SDK)
    services/
      chat_service.py       # 캐시 조회/저장 + 안전 패턴 + 로깅
      cache.py               # SHA256 키 기반 인메모리 캐시
    prompts/
      system_prompt.py      # 도메인 시스템 프롬프트
      demo_questions.py     # 데모 질문 5개
    routers/
      chat.py                # /chat/stream 엔드포인트
    main.py                  # FastAPI 앱 조립
  requirements.txt
  requests.http              # PyCharm/VS Code HTTP Client용 테스트 요청
```

## 실행 방법

1. `mini_project/` 안에 `.env` 파일을 만들고 아래 값을 채웁니다.

   ```
   MLAPI_BASE_URL=https://api.anthropic.com/v1/
   MLAPI_API_KEY=<본인의 Claude API 키>
   MLAPI_MODEL=claude-haiku-4-5-20251001
   ```

   Anthropic의 OpenAI SDK 호환 엔드포인트를 사용하므로, `openai` 파이썬 패키지로 Claude 모델을 그대로 호출합니다.

2. 패키지 설치 후 서버 실행

   ```bash
   cd mini_project
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8003
   ```

3. 동작 확인

   ```bash
   curl http://localhost:8003/health
   curl -N -X POST http://localhost:8003/chat/stream \
     -H "Content-Type: application/json" \
     -d '{"message": "FastAPI에서 APIRouter를 쓰는 이유가 뭐야?"}'
   ```

   또는 브라우저에서 `http://localhost:8003/docs` (Swagger UI)로 바로 테스트할 수 있습니다.

## 더 읽어보기

- [API 키로 외부 LLM(Claude)을 가져와 작동시키는 과정](docs/api-key-mechanism.md) — OpenAI SDK 호환 계층이 요청/응답을 어떻게 번역하는지, 실제 코드 어느 부분이 담당하는지 정리한 문서

## 주요 기능

- **스트리밍 응답**: `/chat/stream`이 토큰을 실시간으로 흘려보내며, 응답 끝에 `[DONE]` / `[EMPTY]` / `[ERROR]` 마커를 붙입니다.
- **캐싱**: 같은 질문(메시지+모델+temperature)은 SHA256 해시 키로 캐시되어, 두 번째 호출부터는 LLM을 다시 부르지 않고 즉시 응답합니다.
- **로깅**: 요청마다 `cache MISS/HIT/STORE`, LLM 호출 시작/종료, 처리 시간(ms)이 서버 로그에 남습니다.
- **레이어드 구조**: Router(HTTP 입출력) → Service(캐시+안전 패턴) → Client(LLM 호출)로 관심사를 분리했습니다.

## 완료 기준 체크

- [x] 서버 정상 기동
- [x] `/chat/stream` 스트리밍 응답 확인
- [x] 시스템 프롬프트가 답변 톤에 반영됨
- [x] 데모 질문 5개 정상 응답
- [x] 캐시 HIT 시 응답 속도 대폭 단축 확인
- [x] 잘못된 입력에 대한 422 검증 오류 확인

## 참고 자료

- 이어드림스쿨 6기 [AI 실무 기본] AI 서비스 개발자 과정 8주차 강의
- 5일차 미니 프로젝트 가이드: [`01_프로젝트_가이드.ipynb`](01_프로젝트_가이드.ipynb)
- 시작 코드 생성 노트북: [`02_시작코드.ipynb`](02_시작코드.ipynb)
