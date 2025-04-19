import requests
from bs4 import BeautifulSoup
from app.rag.loaders.utils import get_cik_from_ticker
import html2text

SEC_HEADERS = {
    "User-Agent": "Yash Dixit yashdixit0885@gmail.com"
}

def fetch_filing_text(ticker: str, form_type: str = "10-K") -> str:
    cik = get_cik_from_ticker(ticker)
    if not cik:
        raise ValueError("CIK not found.")

    padded_cik = cik.zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{padded_cik}.json"
    print(f"📡 SEC JSON Lookup: {url}")

    res = requests.get(url, headers=SEC_HEADERS)
    if res.status_code != 200:
        raise ValueError("Failed to fetch SEC submission data.")

    data = res.json()
    filings = data.get("filings", {}).get("recent", {})

    accession_nums = filings.get("accessionNumber", [])
    form_types = filings.get("form", [])
    primary_docs = filings.get("primaryDocument", [])
    dates = filings.get("filingDate", [])

    for i, form in enumerate(form_types):
        if form.upper() == form_type:
            acc_num = accession_nums[i].replace("-", "")
            doc = primary_docs[i]
            filing_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_num}/{doc}"
            print(f"✅ Found {form_type} → {filing_url}")
            response = requests.get(filing_url, headers=SEC_HEADERS)
            return html2text.html2text(response.text)

    print(f"⚠️ No {form_type} filing found for {ticker}")
    return None