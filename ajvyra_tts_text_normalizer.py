import re
import unicodedata


PERSIAN_REPLACEMENTS = {
    "ي": "ی",
    "ى": "ی",
    "ك": "ک",
    "ۀ": "ه",
    "ة": "ه",
    "ؤ": "و",
    "إ": "ا",
    "أ": "ا",
    "ـ": "",
}


def normalize_unicode(text: str) -> str:
    return unicodedata.normalize("NFKC", text)


def normalize_persian(text: str) -> str:
    text = normalize_unicode(text)

    for old, new in PERSIAN_REPLACEMENTS.items():
        text = text.replace(old, new)

    text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_japanese(text: str) -> str:
    text = normalize_unicode(text)

    text = text.replace("　", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_text(text: str, language: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    text = text.strip()

    if not text:
        raise ValueError("text cannot be empty")

    language = language.lower()

    if language == "fa":
        return normalize_persian(text)

    if language == "ja":
        return normalize_japanese(text)

    raise ValueError(f"Unsupported language: {language}")


def split_sentences(text: str, language: str) -> list[str]:
    text = normalize_text(text, language)

    if language == "ja":
        parts = re.split(r"(?<=[。！？])", text)
    else:
        parts = re.split(r"(?<=[.!؟!])", text)

    return [part.strip() for part in parts if part.strip()]
