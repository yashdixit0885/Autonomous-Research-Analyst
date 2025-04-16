import requests
from bs4 import BeautifulSoup
import html2text
import time

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

def get_latest_10k_url(cik: str) -> str:
    """
    Get the URL of the primary 10-K filing document.
    """
    feed_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    res = requests.get(feed_url, headers=SEC_HEADERS)
    data = res.json()

    recent_filings = data["filings"]["recent"]
    form_types = recent_filings["form"]
    accession_numbers = recent_filings["accessionNumber"]
    primary_docs = recent_filings["primaryDocument"]

    for i, form in enumerate(form_types):
        if form == "10-K":
            accession = accession_numbers[i].replace("-", "")
            primary_doc = primary_docs[i]

            doc_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/{primary_doc}"
            return doc_url

    raise ValueError("10-K primary document not found.")


def fetch_10k_text(ticker: str) -> str:
    """
    Main function: Fetch latest 10-K HTML → convert to plain text.
    """
    cik = get_cik_from_ticker(ticker)
    print(f"✅ Found CIK: {cik}")

    doc_url = get_latest_10k_url(cik)
    print(f"📄 Found 10-K URL: {doc_url}")

    html = requests.get(doc_url, headers=SEC_HEADERS).text
    soup = BeautifulSoup(html, "html.parser")
    text = html2text.html2text(soup.get_text())

    return text

if __name__ == "__main__":
    ticker = "AMD"  # or AAPL, MSFT, etc.
    text = fetch_10k_text(ticker)

    with open("rag/sample_docs/auto_fetched_10k.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("✅ 10-K saved to sample_docs/auto_fetched_10k.txt")
