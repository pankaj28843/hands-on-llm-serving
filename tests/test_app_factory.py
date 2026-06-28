from collections.abc import AsyncIterator

from fastapi.testclient import TestClient

from mac_llm_ops_lab.app import create_app


class FakeBackend:
    def __init__(self) -> None:
        self.loaded = 0
        self.closed = 0
        self.generated_prompts: list[str] = []

    async def load(self) -> None:
        self.loaded += 1

    async def close(self) -> None:
        self.closed += 1

    async def ready(self) -> bool:
        return self.loaded == 1 and self.closed == 0

    async def list_models(self) -> list[dict[str, str]]:
        return [{"id": "fake-local-model", "object": "model"}]

    async def generate(self, prompt: str, model: str) -> str:
        self.generated_prompts.append(f"{model}:{prompt}")
        return f"fake response to {prompt}"

    async def stream(self, prompt: str, model: str) -> AsyncIterator[str]:
        self.generated_prompts.append(f"{model}:{prompt}")
        yield "fake "
        yield "stream"


def test_app_constructs_with_fake_backend_and_no_external_services() -> None:
    backend = FakeBackend()
    app = create_app(backend=backend)

    with TestClient(app) as client:
        live_response = client.get("/live")
        ready_response = client.get("/ready")
        models_response = client.get("/v1/models")
        generation_response = client.post(
            "/v1/chat/completions",
            json={
                "model": "fake-local-model",
                "messages": [{"role": "user", "content": "hello"}],
                "stream": False,
            },
        )

    assert live_response.status_code == 200
    assert live_response.json() == {"status": "alive"}
    assert ready_response.status_code == 200
    assert ready_response.json() == {"status": "ready"}
    assert models_response.status_code == 200
    assert models_response.json()["data"] == [
        {"id": "fake-local-model", "object": "model"}
    ]
    assert generation_response.status_code == 200
    assert generation_response.json()["choices"][0]["message"] == {
        "role": "assistant",
        "content": "fake response to hello",
    }
    assert backend.loaded == 1
    assert backend.closed == 1
    assert backend.generated_prompts == ["fake-local-model:hello"]
