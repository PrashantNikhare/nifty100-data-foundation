from src.etl.normaliser import normalize_year, normalize_ticker


def test_normalize_year_integer():
    assert normalize_year(2022) == 2022


def test_normalize_year_string():
    assert normalize_year("2022") == 2022


def test_normalize_year_with_spaces():
    assert normalize_year(" 2022 ") == 2022


def test_normalize_year_float():
    assert normalize_year(2022.0) == 2022


def test_normalize_year_empty():
    assert normalize_year("") is None


def test_normalize_year_none():
    assert normalize_year(None) is None


def test_normalize_year_invalid():
    assert normalize_year("hello") is None


def test_normalize_year_decimal_string():
    assert normalize_year("2022.0") == 2022


def test_normalize_year_spaces_inside():
    assert normalize_year(" 2022") == 2022


def test_normalize_year_float_string_with_spaces():
    assert normalize_year(" 2022.0 ") == 2022


def test_normalize_year_zero():
    assert normalize_year(0) == 0


def test_normalize_year_negative():
    assert normalize_year(-2022) == -2022


def test_normalize_year_text():
    assert normalize_year("abc") is None


def test_normalize_year_special_character():
    assert normalize_year("@2022") is None


def test_normalize_year_decimal():
    assert normalize_year(2022.5) == 2022


def test_normalize_year_boolean_true():
    assert normalize_year(True) is None


def test_normalize_year_boolean_false():
    assert normalize_year(False) is None


def test_normalize_year_only_spaces():
    assert normalize_year("   ") is None


def test_normalize_year_none_again():
    assert normalize_year(None) is None


def test_normalize_year_float_string():
    assert normalize_year("2020.0") == 2020

def test_normalize_ticker_uppercase():
    assert normalize_ticker("tcs") == "TCS"


def test_normalize_ticker_spaces():
    assert normalize_ticker(" TCS ") == "TCS"


def test_normalize_ticker_mixed_case():
    assert normalize_ticker("TcS") == "TCS"


def test_normalize_ticker_none():
    assert normalize_ticker(None) is None


def test_normalize_ticker_empty():
    assert normalize_ticker("") is None


def test_normalize_ticker_number():
    assert normalize_ticker(123) == "123"


def test_normalize_ticker_lowercase_with_spaces():
    assert normalize_ticker(" reliance ") == "RELIANCE"

def test_normalize_ticker_empty_spaces():
    assert normalize_ticker("   ") is None


def test_normalize_ticker_lowercase():
    assert normalize_ticker("infy") == "INFY"


def test_normalize_ticker_mixed_case_with_spaces():
    assert normalize_ticker(" InFy ") == "INFY"


def test_normalize_ticker_special_character():
    assert normalize_ticker("TCS@") == "TCS@"


def test_normalize_ticker_number_string():
    assert normalize_ticker("123") == "123"


def test_normalize_ticker_zero():
    assert normalize_ticker(0) == "0"


def test_normalize_ticker_none_again():
    assert normalize_ticker(None) is None


def test_normalize_ticker_already_uppercase():
    assert normalize_ticker("RELIANCE") == "RELIANCE"