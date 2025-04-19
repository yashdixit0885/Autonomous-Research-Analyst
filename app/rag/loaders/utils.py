import requests

SEC_HEADERS = {
    "User-Agent": "Yash Dixit yashdixit0885@gmail.com"
}


def get_cik_from_ticker(ticker: str) -> str:
    """
    Convert stock ticker to SEC CIK (with zero padding).
    """
    url = f"https://www.sec.gov/files/company_tickers.json"
    res = requests.get(url, headers=SEC_HEADERS)
    data = res.json()
    ticker = ticker.upper()

    for entry in data.values():
        if entry["ticker"] == ticker:
            cik_str = str(entry["cik_str"]).zfill(10)
            return cik_str
    raise ValueError(f"CIK not found for ticker {ticker}")
