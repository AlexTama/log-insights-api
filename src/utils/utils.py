from collections import Counter

from src.config.constants import SERVICE_COUNT_LEVELS
from src.repositories.log_repository import LogRepository


def load_logs(repository: LogRepository) -> list[dict]:
    return repository.get_logs()


def count_by_level(logs: list[dict]) -> Counter[str]:
    return Counter(log["level"] for log in logs)


def count_by_service_and_level(logs: list[dict]) -> Counter:
    return Counter(
        (log["service"], log["level"])
        for log in logs
        if log["level"] in SERVICE_COUNT_LEVELS
    )
