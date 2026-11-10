import pytest

from src.app import create_app
from src.repositories.log_repository import InMemoryLogRepository


@pytest.fixture
def client():
    logs = [
        {"level": "INFO", "service": "api-gateway"},
        {"level": "INFO", "service": "orders-service"},
        {"level": "ERROR", "service": "payments-api"},
        {"level": "DEBUG", "service": "auth-service"},
    ]
    app = create_app(repository=InMemoryLogRepository(logs))
    app.config.update(TESTING=True)
    return app.test_client()


def test_count_logs_returns_count_for_level(client):
    response = client.get("/count_logs/ERROR")

    assert response.status_code == 200
    assert response.get_json() == {"level": "ERROR", "count": 1}


def test_count_logs_is_case_insensitive(client):
    response = client.get("/count_logs/info")

    assert response.status_code == 200
    assert response.get_json() == {"level": "INFO", "count": 2}


def test_count_logs_returns_zero_when_level_is_absent(client):
    response = client.get("/count_logs/CRITICAL")

    assert response.status_code == 200
    assert response.get_json() == {"level": "CRITICAL", "count": 0}


def test_count_logs_rejects_unknown_level(client):
    response = client.get("/count_logs/TRACE")

    assert response.status_code == 400
    payload = response.get_json()
    assert payload["error"] == "Unknown level: TRACE"
    assert payload["valid_levels"] == [
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ]


def test_count_logs_returns_zero_for_empty_logs():
    app = create_app(repository=InMemoryLogRepository([]))
    app.config.update(TESTING=True)

    response = app.test_client().get("/count_logs/INFO")

    assert response.status_code == 200
    assert response.get_json() == {"level": "INFO", "count": 0}
