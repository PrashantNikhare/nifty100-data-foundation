from src.etl.loader import load_excel


def test_load_companies():
    data = load_excel("data/raw/companies.xlsx")

    assert data.shape == (92, 12)
    assert "id" in data.columns
    assert "company_name" in data.columns


def test_load_profitandloss():
    data = load_excel("data/raw/profitandloss.xlsx")

    assert "company_id" in data.columns
    assert "year" in data.columns
    assert len(data) == 1276

def test_load_financial_ratios():
    data = load_excel("data/raw/financial_ratios.xlsx")

    assert "id" in data.columns
    assert "company_id" in data.columns
    assert "year" in data.columns
    assert "net_profit_margin_pct" in data.columns
    assert len(data) == 1184