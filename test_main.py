from collections import Counter

from src.utils.utils import count_by_level


def test_count_by_level_counts_mixed_levels():
    # Given a list of logs with 2 INFO, 1 ERROR and 1 DEBUG entries
    logs = [
        {"level": "INFO", "message": "Request received"},
        {"level": "ERROR", "message": "Database timeout"},
        {"level": "INFO", "message": "Order created"},
        {"level": "DEBUG", "message": "Cache hit"},
    ]

    # When count_by_level is called
    result = count_by_level(logs)

    # Then the result has 2 INFO, 1 ERROR and 1 DEBUG
    assert result == Counter({"INFO": 2, "ERROR": 1, "DEBUG": 1})


def test_count_by_level_returns_empty_counts_for_empty_list():
    # Given an empty list of logs
    logs = []

    # When count_by_level is called
    result = count_by_level(logs)

    # Then the result has no counts and does not raise
    assert result == Counter()
    assert len(result) == 0


def test_count_by_level_returns_zero_for_missing_level():
    # Given a list of logs that only contains INFO entries
    logs = [
        {"level": "INFO", "message": "Request received"},
        {"level": "INFO", "message": "Order created"},
    ]

    # When count_by_level is called and CRITICAL is queried
    result = count_by_level(logs)

    # Then CRITICAL counts as 0 instead of raising an error
    assert result["CRITICAL"] == 0
