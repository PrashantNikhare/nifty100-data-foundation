import sqlite3
from pathlib import Path

import pandas as pd

from src.etl.loader import load_excel
from src.etl.validator import (
    check_primary_key_unique,
    check_balance_sheet,
    check_positive_sales,
)


RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("output")


def run_quality_checks():
    failures = []

    files = sorted(RAW_DIR.glob("*.xlsx"))

    # DQ-01: Primary key uniqueness
    for file_path in files:
        data = load_excel(file_path)

        if "id" in data.columns:
            if not check_primary_key_unique(data, "id"):
                failures.append({
                    "rule": "DQ-01",
                    "file": file_path.name,
                    "severity": "CRITICAL",
                    "status": "FAIL",
                })

    # DQ-02: Exact duplicate rows
    for file_path in files:
        data = load_excel(file_path)

        duplicate_mask = data.duplicated(keep=False)

        if duplicate_mask.any():
            failures.append({
                "rule": "DQ-02",
                "file": file_path.name,
                "severity": "CRITICAL",
                "status": "FAIL",
            })

    # DQ-04: Balance sheet balance
    balancesheet = load_excel(
        RAW_DIR / "balancesheet.xlsx"
    )

    if not check_balance_sheet(balancesheet):
        failures.append({
            "rule": "DQ-04",
            "file": "balancesheet.xlsx",
            "severity": "WARNING",
            "status": "FAIL",
        })

    # DQ-05: OPM cross-check
    pnl = load_excel(
        RAW_DIR / "profitandloss.xlsx"
    )

    valid_opm = pnl[
        pnl["sales"].notna()
        & pnl["operating_profit"].notna()
        & pnl["opm_percentage"].notna()
        & (pnl["sales"] > 0)
    ].copy()

    calculated_opm = (
        valid_opm["operating_profit"]
        / valid_opm["sales"]
    ) * 100

    difference = (
        calculated_opm
        - valid_opm["opm_percentage"]
    ).abs()

    if (difference > 1).any():
        failures.append({
            "rule": "DQ-05",
            "file": "profitandloss.xlsx",
            "severity": "WARNING",
            "status": "FAIL",
        })

    # DQ-06: Positive sales
    if not check_positive_sales(pnl):
        failures.append({
            "rule": "DQ-06",
            "file": "profitandloss.xlsx",
            "severity": "CRITICAL",
            "status": "FAIL",
        })

    OUTPUT_DIR.mkdir(exist_ok=True)

    result = pd.DataFrame(failures)

    result.to_csv(
        OUTPUT_DIR / "validation_failures.csv",
        index=False,
    )

    return result