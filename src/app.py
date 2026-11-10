from flask import Flask, jsonify

from src.config.constants import DEFAULT_LOG_PATH, LEVELS
from src.repositories.log_repository import JsonFileLogRepository, LogRepository
from src.utils.utils import count_by_level, load_logs


def create_app(repository: LogRepository | None = None) -> Flask:
    app = Flask(__name__)
    app.config["LOG_REPOSITORY"] = (
        repository
        if repository is not None
        else JsonFileLogRepository(DEFAULT_LOG_PATH)
    )

    @app.get("/count_logs/<level>")
    def count_logs(level: str):
        normalized_level = level.upper()

        if normalized_level not in LEVELS:
            return (
                jsonify(
                    error=f"Unknown level: {level}",
                    valid_levels=LEVELS,
                ),
                400,
            )

        logs = load_logs(app.config["LOG_REPOSITORY"])
        counts = count_by_level(logs)
        return jsonify(level=normalized_level, count=counts[normalized_level])

    return app


app = create_app()
