# app/rag/utils.py

def clean_text(text: str) -> str:
    """Remove excessive newlines and whitespace"""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)
