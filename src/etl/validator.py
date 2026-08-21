def validate_columns(data, expected_columns):
    """
    Check if DataFrame columns exactly match expected columns.
    """

    return list(data.columns) == expected_columns


def validate_required_columns(data, required_columns):
    """
    Check whether all required columns are present.
    """

    for column in required_columns:
        if column not in data.columns:
            return False

    return True


def check_primary_key_unique(data, column):
    """
    Check whether values in a column are unique.
    """

    return data[column].is_unique


def check_company_year_unique(data):
    """
    Check whether company_id and year combinations are unique.
    """

    return not data.duplicated(subset=["company_id", "year"]).any()


def check_foreign_key(data, reference_data, column):
    """
    Check whether all foreign key values exist in reference data.
    """

    return bool(data[column].isin(reference_data[column]).all())


def check_balance_sheet(data):
    """
    Check whether total assets and total liabilities are within 1%.
    """

    difference = (data["total_assets"] - data["total_liabilities"]).abs()

    return bool(
        (difference <= data["total_assets"].abs() * 0.01).all()
    )


def check_operating_profit_margin(data):
    """
    Check operating profit margin against sales and operating profit.

    Rows with missing values or non-positive sales are ignored because
    OPM cannot be calculated reliably for those records.
    """

    valid_data = data[
        data["sales"].notna()
        & data["operating_profit"].notna()
        & data["opm_percentage"].notna()
        & (data["sales"] > 0)
    ].copy()

    if valid_data.empty:
        return True

    calculated_opm = (
        valid_data["operating_profit"]
        / valid_data["sales"]
    ) * 100

    difference = (
        calculated_opm
        - valid_data["opm_percentage"]
    ).abs()

    return bool((difference <= 1).all())


def check_positive_sales(data):
    """
    Check that non-missing sales values are non-negative.
    """

    sales = data["sales"].dropna()

    return bool((sales >= 0).all())

def run_validation_rule(data, rule_name, validation_function, severity):
    """
    Run a validation rule and return its result.
    """

    result = validation_function(data)

    return {
        "rule": rule_name,
        "severity": severity,
        "status": "PASS" if result else "FAIL",
    }