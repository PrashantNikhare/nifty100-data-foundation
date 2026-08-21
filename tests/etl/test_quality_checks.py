import pandas as pd

from src.etl.quality_checks import run_quality_checks


def test_run_quality_checks_returns_dataframe():
    result = run_quality_checks()

    assert isinstance(result, pd.DataFrame)


def test_run_quality_checks_has_expected_columns():
    result = run_quality_checks()

    if not result.empty:
        assert list(result.columns) == [
            "rule",
            "file",
            "severity",
            "status",
        ]


def test_run_quality_checks_contains_only_valid_statuses():
    result = run_quality_checks()

    if not result.empty:
        assert set(result["status"]).issubset({"PASS", "FAIL"})


def test_run_quality_checks_contains_only_valid_severities():
    result = run_quality_checks()

    if not result.empty:
        assert set(result["severity"]).issubset(
            {"CRITICAL", "WARNING"}
        )