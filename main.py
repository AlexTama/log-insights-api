from src.config.constants import DEFAULT_LOG_PATH, LEVELS
from src.repositories.log_repository import JsonFileLogRepository
from src.utils.utils import count_by_level, count_by_service_and_level, load_logs


def main() -> None:
    repository = JsonFileLogRepository(DEFAULT_LOG_PATH)
    logs = load_logs(repository)
    counts = count_by_level(logs)
    service_counts = count_by_service_and_level(logs)

    for level in LEVELS:
        print(f"{level}: {counts[level]}")

    print("ERROR and CRITICAL by service:")
    services = sorted({service for service, _ in service_counts})
    for service in services:
        for level in ("ERROR", "CRITICAL"):
            count = service_counts[(service, level)]
            if count:
                print(f"{service}: {count}, level: {level}")

    unknown = set(counts) - set(LEVELS)
    if unknown:
        print(f"Unknown levels found: {sorted(unknown)}")


if __name__ == "__main__":
    main()
