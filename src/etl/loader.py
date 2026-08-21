import sqlite3
from pathlib import Path

import pandas as pd

from src.etl.normaliser import normalize_year, normalize_ticker


HEADER_ROW_0_FILES = {
    "financial_ratios.xlsx",
    "market_cap.xlsx",
    "peer_groups.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx",
}


def load_excel(file_path):
    """
    Read an Excel file and return a cleaned DataFrame.
    """

    file_name = Path(file_path).name

    header = 0 if file_name in HEADER_ROW_0_FILES else 1

    data = pd.read_excel(file_path, header=header)

    if "year" in data.columns:
        data["year"] = data["year"].apply(normalize_year)

    if "company_id" in data.columns:
        data["company_id"] = data["company_id"].apply(normalize_ticker)

    return data


def load_table(
    connection,
    file_path,
    table_name,
    reference_table="companies",
    audit_file="output/load_audit.csv",
):
    """
    Load one Excel file into SQLite.

    Rows whose company_id does not exist in the companies table
    are rejected and recorded in the load audit.
    """

    data = load_excel(file_path)

    rejected_rows = 0

    if "company_id" in data.columns and reference_table:
        reference = pd.read_sql_query(
            f"SELECT id FROM {reference_table}",
            connection,
        )

        valid_company_ids = set(reference["id"].astype(str))

        data["company_id"] = data["company_id"].astype(str)

        valid_mask = data["company_id"].isin(valid_company_ids)

        rejected_rows = int((~valid_mask).sum())

        data = data.loc[valid_mask].copy()

    if not data.empty:
        data.to_sql(
            table_name,
            connection,
            if_exists="append",
            index=False,
        )

    audit_path = Path(audit_file)
    audit_path.parent.mkdir(parents=True, exist_ok=True)

    audit_row = pd.DataFrame(
        [{
            "table": table_name,
            "source_file": Path(file_path).name,
            "source_rows": len(load_excel(file_path)),
            "loaded_rows": len(data),
            "rejected_rows": rejected_rows,
        }]
    )

    if audit_path.exists():
        audit_row.to_csv(
            audit_path,
            mode="a",
            header=False,
            index=False,
        )
    else:
        audit_row.to_csv(
            audit_path,
            index=False,
        )

    return len(data)


def create_database(db_path="db/nifty100.db", schema_path="db/schema.sql"):
    """
    Create the SQLite database using schema.sql.
    """

    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)

    connection.execute("PRAGMA foreign_keys = ON")

    with open(schema_path, "r", encoding="utf-8") as file:
        connection.executescript(file.read())

    return connection


def load_all_tables(
    db_path="db/nifty100.db",
    schema_path="db/schema.sql",
):
    """
    Load all source files into the SQLite database.
    """

    connection = create_database(db_path, schema_path)

    raw_path = Path("data/raw")

    audit_path = Path("output/load_audit.csv")

    if audit_path.exists():
        audit_path.unlink()

    load_order = [
        ("companies.xlsx", "companies", None),
        ("profitandloss.xlsx", "profitandloss", "companies"),
        ("balancesheet.xlsx", "balancesheet", "companies"),
        ("cashflow.xlsx", "cashflow", "companies"),
        ("analysis.xlsx", "analysis", "companies"),
        ("documents.xlsx", "documents", "companies"),
        ("prosandcons.xlsx", "prosandcons", "companies"),
        ("sectors.xlsx", "sectors", "companies"),
        ("stock_prices.xlsx", "stock_prices", "companies"),
        ("financial_ratios.xlsx", "financial_ratios", "companies"),
        ("peer_groups.xlsx", "peer_groups", "companies"),
    ]

    results = []

    try:
        for file_name, table_name, reference_table in load_order:

            file_path = raw_path / file_name

            if not file_path.exists():
                continue

            loaded = load_table(
                connection=connection,
                file_path=file_path,
                table_name=table_name,
                reference_table=reference_table,
                audit_file=audit_path,
            )

            results.append(
                {
                    "table": table_name,
                    "loaded_rows": loaded,
                }
            )

        connection.commit()

    finally:
        connection.close()

    return pd.DataFrame(results)