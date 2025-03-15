import re


def clean_text(text: str) -> str:
    """Limpia el texto eliminando símbolos no deseados."""
    text = text.replace("**", "").replace("*", "").replace("_", "")
    text = re.sub(r'[`~]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
