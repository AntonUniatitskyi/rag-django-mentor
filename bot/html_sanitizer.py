# bot/html_sanitizer.py
import re

ALLOWED_TAGS = {"b", "strong", "i", "em", "u", "ins", "s", "strike", "del", "code", "pre", "a", "span"}


def sanitize_telegram_html(text: str) -> str:
    text = re.sub(r"<li[^>]*>(.*?)</li>", r"- \1\n", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"</?(ul|ol)[^>]*>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<p[^>]*>(.*?)</p>", r"\1\n\n", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<h[1-6][^>]*>(.*?)</h[1-6]>", r"\1\n\n", text, flags=re.DOTALL | re.IGNORECASE)
    allowed_pattern = "|".join(ALLOWED_TAGS)
    text = re.sub(rf"</?(?!(?:{allowed_pattern})\b)[a-zA-Z0-9]+[^>]*>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()