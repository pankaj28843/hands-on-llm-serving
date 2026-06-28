import json
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Protocol
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field


class ModelBackend(Protocol):
    async def load(self) -> None: ...

    async def close(self) -> None: ...

    async def ready(self) -> bool: ...

    async def list_models(self) -> list[dict[str, str]]: ...

    async def generate(self, prompt: str, model: str) -> str: ...

    async def stream(self, prompt: str, model: str) -> AsyncIterator[str]: ...


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatMessage] = Field(min_length=1)
    stream: bool = False


def create_app(*, backend: ModelBackend) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        await backend.load()
        app.state.backend = backend
        try:
            yield
        finally:
            await backend.close()

    app = FastAPI(title="Mac LLM Ops Lab", lifespan=lifespan)

    @app.get("/live")
    async def live() -> dict[str, str]:
        return {"status": "alive"}

    @app.get("/ready")
    async def ready(request: Request) -> dict[str, str]:
        active_backend: ModelBackend = request.app.state.backend
        if not await active_backend.ready():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={"status": "not_ready"},
            )
        return {"status": "ready"}

    @app.get("/v1/models")
    async def models(request: Request) -> dict[str, object]:
        active_backend: ModelBackend = request.app.state.backend
        return {"object": "list", "data": await active_backend.list_models()}

    @app.post("/v1/chat/completions", response_model=None)
    async def chat_completions(
        payload: ChatCompletionRequest, request: Request
    ) -> dict[str, object] | StreamingResponse:
        active_backend: ModelBackend = request.app.state.backend
        prompt = _last_user_message(payload.messages)
        if payload.stream:
            return StreamingResponse(
                _stream_events(active_backend, prompt=prompt, model=payload.model),
                media_type="text/event-stream",
            )

        content = await active_backend.generate(prompt, payload.model)
        return _completion_response(model=payload.model, content=content)

    return app


def _last_user_message(messages: list[ChatMessage]) -> str:
    for message in reversed(messages):
        if message.role == "user":
            return message.content
    return messages[-1].content


def _completion_response(*, model: str, content: str) -> dict[str, object]:
    return {
        "id": f"chatcmpl-{uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
    }


async def _stream_events(
    backend: ModelBackend, *, prompt: str, model: str
) -> AsyncIterator[str]:
    async for chunk in backend.stream(prompt, model):
        event = {
            "id": f"chatcmpl-{uuid4().hex}",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": model,
            "choices": [{"index": 0, "delta": {"content": chunk}}],
        }
        yield f"data: {json.dumps(event)}\n\n"
    yield "data: [DONE]\n\n"
