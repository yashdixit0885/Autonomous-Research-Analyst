# app/rag/loaders/sec_loader.py

import os
from bs4 import BeautifulSoup


def load_sec_text(filepath: str) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ File not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as file:
        raw_html = file.read()

    soup = BeautifulSoup(raw_html, "html.parser")
    for tag in soup(["script", "style", "table"]):
        tag.decompose()

    return soup.get_text(separator="\n").strip()

