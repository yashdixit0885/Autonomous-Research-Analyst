# app/rag/loaders/edgar_loader.py

import os
from bs4 import BeautifulSoup
import html2text
from sec_edgar_downloader import Downloader

USER_AGENT = "AutonomousResearchBot/1.0 yashdixit0885@gmail.com)"


def fetch_filing_text(ticker: str, form_type: str = "10-K") -> str:
    dl = Downloader(company_name="AutonomousResearchBot", email_address="yashdixit0885@gmail.com", download_folder="sec_filings")
    print(f"\U0001F4E5 Downloading latest {form_type} filing for {ticker}...")
    dl.get(form_type, ticker)

    base_path = f"sec_filings/sec-edgar-filings/{ticker}/{form_type}"
    if not os.path.exists(base_path):
        raise FileNotFoundError(f"\u274C Filing folder not found at {base_path}")

    latest_dir = sorted(os.listdir(base_path))[-1]
    html_path = os.path.join(base_path, latest_dir, "full-submission.txt")

    with open(html_path, "r", encoding="utf-8") as file:
        raw_html = file.read()

    print(f"\U0001F4C4 Parsing {form_type} HTML for {ticker}")
    soup = BeautifulSoup(raw_html, "html.parser")
    for tag in soup(["script", "style", "table"]):
        tag.decompose()

    converter = html2text.HTML2Text()
    converter.ignore_links = True
    converter.ignore_images = True
    plain_text = converter.handle(str(soup))

    return plain_text.strip()

