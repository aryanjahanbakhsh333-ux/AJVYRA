from dataclasses import dataclass


@dataclass(frozen=True)
class PhonemeSequence:
    language: str
    symbols: tuple[str, ...]

    @property
    def length(self) -> int:
        return len(self.symbols)


PERSIAN_CHARS = (
    "ا",
    "ب",
    "پ",
    "ت",
    "ث",
    "ج",
    "چ",
    "ح",
    "خ",
    "د",
    "ذ",
    "ر",
    "ز",
    "ژ",
    "س",
    "ش",
    "ص",
    "ض",
    "ط",
    "ظ",
    "ع",
    "غ",
    "ف",
    "ق",
    "ک",
    "گ",
    "ل",
    "م",
    "ن",
    "و",
    "ه",
    "ی",
)

JAPANESE_CHARS = (
    "あ",
    "い",
    "う",
    "え",
    "お",
    "か",
    "き",
    "く",
    "け",
    "こ",
    "さ",
    "し",
    "す",
    "せ",
    "そ",
    "た",
    "ち",
    "つ",
    "て",
    "と",
    "な",
    "に",
    "ぬ",
    "ね",
    "の",
    "は",
    "ひ",
    "ふ",
    "へ",
    "ほ",
    "ま",
    "み",
    "む",
    "め",
    "も",
    "や",
    "ゆ",
    "よ",
    "ら",
    "り",
    "る",
    "れ",
    "ろ",
    "わ",
    "を",
    "ん",
)


class PhonemeEngine:

    def encode(self, text: str, language: str) -> PhonemeSequence:
        language = language.lower()

        if language == "fa":
            symbols = self._encode_persian(text)
        elif language == "ja":
            symbols = self._encode_japanese(text)
        else:
            raise ValueError(f"Unsupported language: {language}")

        return PhonemeSequence(
            language=language,
            symbols=tuple(symbols),
        )

    def _encode_persian(self, text: str) -> list[str]:
        result = []

        for char in text:
            if char in PERSIAN_CHARS:
                result.append(char)
            elif char.isspace():
                result.append("<space>")
            elif char in ".,!?؟":
                result.append(f"<{char}>")

        return result

    def _encode_japanese(self, text: str) -> list[str]:
        result = []

        for char in text:
            if char in JAPANESE_CHARS:
                result.append(char)
            elif char.isspace():
                result.append("<space>")
            elif char in "、。！？":
                result.append(f"<{char}>")

        return result
