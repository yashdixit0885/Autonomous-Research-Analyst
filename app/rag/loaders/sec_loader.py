from bs4 import BeautifulSoup
import html2text

def load_sec_text(filepath):
    """Load a 10-K or earnings call document from file."""
    with open(filepath, "r", encoding="utf-8") as file:
        raw = file.read()

    # If HTML, convert to plain text
    if "<html" in raw.lower():
        soup = BeautifulSoup(raw, "html.parser")
        raw = html2text.html2text(soup.get_text())

    return raw
