import os
import requests
from bs4 import BeautifulSoup
import html2text
from sec_edgar_downloader import Downloader
import re

# ✅ Add required SEC header to avoid 403 errors
HEADERS = {
    "User-Agent": "Yash Dixit (yashdixit0885@gmail.com)"  # <-- Use your real email here
}

def clean_sec_text(text: str) -> str:
    """Clean SEC filing text to remove unwanted content and formatting."""
    # Remove HTML entities
    text = re.sub(r'&[^;]+;', ' ', text)
    
    # Remove XML/HTML tags and their content
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,;:!?()-]', ' ', text)
    
    # Remove repeated patterns
    text = re.sub(r'\([\s\(]+M\([\s\(]+\)', ' ', text)
    text = re.sub(r'[A-Z0-9]{5,}', ' ', text)  # Remove long sequences of caps and numbers
    
    # Remove CSS styles and attributes
    text = re.sub(r'style="[^"]*"', '', text)
    text = re.sub(r'class="[^"]*"', '', text)
    
    # Remove XBRL references and metadata
    text = re.sub(r'xbrl\.sec\.gov.*?(?=\s|$)', '', text)
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def fetch_filing_text(ticker: str, form_type: str = "10-K") -> str:
    print(f"📥 Downloading latest {form_type} filing for {ticker}...")

    # ✅ Provide email in Downloader to stay compliant with SEC access rules
    dl = Downloader(company_name="Autonomous Research Analyst", email_address="yashdixit0885@gmail.com")
    dl.get(form_type, ticker, limit=1)

    base_path = f"sec-edgar-filings/{ticker}/{form_type}"
    if not os.path.exists(base_path):
        raise FileNotFoundError(f"❌ Filing folder not found at {base_path}")

    latest_dir = sorted(os.listdir(base_path))[-1]
    html_path = os.path.join(base_path, latest_dir, "full-submission.txt")

    if not os.path.exists(html_path):
        raise FileNotFoundError(f"❌ Filing document not found at {html_path}")

    print(f"📄 Fetching {form_type} HTML filing for {ticker}")

    # ✅ Read and parse HTML
    with open(html_path, "r", encoding="utf-8") as file:
        raw_html = file.read()

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(raw_html, "html.parser")
    
    # Remove unwanted elements
    for tag in soup(["script", "style", "table", "img", "svg", "math", "head", "meta", "link"]):
        tag.decompose()
    
    # Get text content
    text = soup.get_text(separator=' ', strip=True)
    
    # Clean the text
    text = clean_sec_text(text)
    
    # Validate the cleaned text
    if len(text) < 100:
        raise ValueError("Text too short after cleaning")
    if len(re.sub(r'[^A-Za-z]', '', text)) < 50:
        raise ValueError("Text contains too few alphabetic characters")
    
    return text
