import pandas as pd

from src.etl.validator import (
    validate_columns,
    validate_required_columns,
    check_primary_key_unique,
    check_company_year_unique,
    check_foreign_key,
    check_balance_sheet,
    check_operating_profit_margin,
    check_positive_sales,
    run_validation_rule,
)

def test_validate_columns_success():
    data = pd.DataFrame(columns=["id", "company_name", "website"])

    expected = ["id", "company_name", "website"]

    assert validate_columns(data, expected) is True


def test_validate_columns_fail():
    data = pd.DataFrame(columns=["id", "website", "company_name"])

    expected = ["id", "company_name", "website"]

    assert validate_columns(data, expected) is False


def test_validate_required_columns_success():
    data = pd.DataFrame(
        columns=["id", "company_name", "website", "face_value"]
    )

    required = ["id", "company_name", "website"]

    assert validate_required_columns(data, required) is True


def test_validate_required_columns_missing():
    data = pd.DataFrame(columns=["id", "company_name"])

    required = ["id", "company_name", "website"]

    assert validate_required_columns(data, required) is False


def test_check_primary_key_unique():
    data = pd.DataFrame({"id": [1, 2, 3]})

    assert check_primary_key_unique(data, "id") is True


def test_check_primary_key_duplicate():
    data = pd.DataFrame({"id": [1, 2, 2]})

    assert check_primary_key_unique(data, "id") is False


def test_check_company_year_unique():
    data = pd.DataFrame({
        "company_id": ["ABB", "ABB"],
        "year": [2020, 2021]
    })

    assert check_company_year_unique(data) is True


def test_check_company_year_duplicate():
    data = pd.DataFrame({
        "company_id": ["ABB", "ABB"],
        "year": [2020, 2020]
    })

    assert check_company_year_unique(data) is False


def test_check_foreign_key():
    data = pd.DataFrame({
        "company_id": ["ABB", "TCS"]
    })

    reference = pd.DataFrame({
        "company_id": ["ABB", "TCS", "INFY"]
    })

    assert check_foreign_key(data, reference, "company_id") is True


def test_check_foreign_key_invalid():
    data = pd.DataFrame({
        "company_id": ["ABB", "XYZ"]
    })

    reference = pd.DataFrame({
        "company_id": ["ABB", "TCS"]
    })

    assert check_foreign_key(data, reference, "company_id") is False


def test_check_balance_sheet():
    data = pd.DataFrame({
        "total_assets": [1000],
        "total_liabilities": [995]
    })

    assert check_balance_sheet(data) is True


def test_check_operating_profit_margin():
    data = pd.DataFrame({
        "sales": [1000],
        "operating_profit": [100],
        "opm_percentage": [10]
    })

    assert check_operating_profit_margin(data) is True


def test_check_positive_sales():
    data = pd.DataFrame({
        "sales": [100, 200, 300]
    })

    assert check_positive_sales(data) is True

def test_check_positive_sales_with_missing_values():
    data = pd.DataFrame({
        "sales": [100, None, 300]
    })

    assert check_positive_sales(data) is True


def test_check_positive_sales_negative_value():
    data = pd.DataFrame({
        "sales": [100, -50, 300]
    })

    assert check_positive_sales(data) is False


def test_run_validation_rule_pass():
    data = pd.DataFrame({"sales": [100, 200]})

    result = run_validation_rule(
        data,
        "DQ-06",
        lambda df: (df["sales"] > 0).all(),
        "CRITICAL",
    )

    assert result["rule"] == "DQ-06"
    assert result["severity"] == "CRITICAL"
    assert result["status"] == "PASS"


def test_run_validation_rule_fail():
    data = pd.DataFrame({"sales": [100, -50]})

    result = run_validation_rule(
        data,
        "DQ-06",
        lambda df: (df["sales"] > 0).all(),
        "CRITICAL",
    )

    assert result["rule"] == "DQ-06"
    assert result["severity"] == "CRITICAL"
    assert result["status"] == "FAIL"

def test_check_positive_sales_zero_allowed():
    data = pd.DataFrame({
        "sales": [100, 0, 300]
    })

    assert check_positive_sales(data) is True