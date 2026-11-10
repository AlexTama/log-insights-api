import json
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from pathlib import Path


class LogRepository(ABC):
    """Port for reading logs from any source."""

    @abstractmethod
    def get_logs(self) -> list[dict]:
        """Return the logs from the underlying source."""


class JsonFileLogRepository(LogRepository):
    """Read a JSON array of log entries."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def get_logs(self) -> list[dict]:
        with self.path.open(encoding="utf-8") as file:
            return json.load(file)


class JsonLinesLogRepository(LogRepository):
    """Read newline-delimited JSON, as produced by loggers like Winston."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def get_logs(self) -> list[dict]:
        with self.path.open(encoding="utf-8") as file:
            return [json.loads(line) for line in file if line.strip()]


class InMemoryLogRepository(LogRepository):
    """Read logs already available in memory, for example a Pub/Sub payload."""

    def __init__(self, logs: Iterable[dict]) -> None:
        self._logs = list(logs)

    def get_logs(self) -> list[dict]:
        return list(self._logs)


class CallableLogRepository(LogRepository):
    """Read logs through a custom loader, for example an API or message queue."""

    def __init__(self, loader: Callable[[], list[dict]]) -> None:
        self._loader = loader

    def get_logs(self) -> list[dict]:
        return self._loader()
