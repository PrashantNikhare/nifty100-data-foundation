import pandas as pd
from src.etl.normaliser import normalize_year, normalize_ticker


def load_excel(file_path):
    """
    Read an Excel file and return it as a DataFrame.
    """

    data = pd.read_excel(file_path, header=1)

    if "year" in data.columns:
        data["year"] = data["year"].apply(normalize_year)

    if "company_id" in data.columns:
        data["company_id"] = data["company_id"].apply(normalize_ticker)

    return data