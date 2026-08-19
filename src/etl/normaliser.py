def normalize_year(value):
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, int):
        return value

    if isinstance(value, float):
        return int(value)

    if isinstance(value, str):
        value = value.strip()

        if value.isdigit():
            return int(value)

        try:
            return int(float(value))
        except ValueError:
            pass

        parts = value.split()

        if len(parts) == 2 and parts[1].isdigit():
            return int(parts[1])

    return None

def normalize_ticker(ticker):
    """
    Convert ticker into a standard uppercase format.
    Returns None if the value is empty.
    """

    if ticker is None:
        return None

    ticker = str(ticker).strip()

    if ticker == "":
        return None

    return ticker.upper()