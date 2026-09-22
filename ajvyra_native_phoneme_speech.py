from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Phoneme:
    symbol: str
    kind: str
    duration: float
    energy: float


class NativePhonemeSpeech:
    """
    Model-free phonetic analyzer for AJVYRA Native TTS.

    It does not use a pretrained model or external API.
    It converts text into a controllable phonetic sequence that
    later synthesis stages can render into sound.
    """

    VOWELS_FA = set("ااآایئو")
    VOWELS_EN = set("aeiouy")
    VOWELS_JA = set("あいうえおアイウエオ")

    CONSONANT_DURATION = 0.055
    VOWEL_DURATION = 0.115

    FA_MAP: Dict[str, str] = {
        "ب": "b", "پ": "p", "ت": "t", "ث": "s",
        "ج": "dʒ", "چ": "tʃ", "ح": "h", "خ": "x",
        "د": "d", "ذ": "z", "ر": "ɾ", "ز": "z",
        "ژ": "ʒ", "س": "s", "ش": "ʃ", "ص": "s",
        "ض": "z", "ط": "t", "ظ": "z", "ع": "ʔ",
        "غ": "ɣ", "ف": "f", "ق": "ɣ", "ک": "k",
        "گ": "g", "ل": "l", "م": "m", "ن": "n",
        "و": "v", "ه": "h", "ی": "j",
    }

    EN_MAP: Dict[str, str] = {
        "b": "b", "c": "k", "d": "d", "f": "f",
        "g": "g", "h": "h", "j": "dʒ", "k": "k",
        "l": "l", "m": "m", "n": "n", "p": "p",
        "q": "k", "r": "ɹ", "s": "s", "t": "t",
        "v": "v", "w": "w", "x": "ks", "y": "j",
        "z": "z",
    }

    JA_MAP: Dict[str, str] = {
        "あ": "a", "い": "i", "う": "u",
        "え": "e", "お": "o",
        "か": "ka", "き": "ki", "く": "ku",
        "け": "ke", "こ": "ko",
        "さ": "sa", "し": "shi", "す": "su",
        "せ": "se", "そ": "so",
        "た": "ta", "ち": "chi", "つ": "tsu",
        "て": "te", "と": "to",
        "な": "na", "に": "ni", "ぬ": "nu",
        "ね": "ne", "の": "no",
        "は": "ha", "ひ": "hi", "ふ": "fu",
        "へ": "he", "ほ": "ho",
        "ま": "ma", "み": "mi", "む": "mu",
        "め": "me", "も": "mo",
        "や": "ya", "ゆ": "yu", "よ": "yo",
        "ら": "ra", "り": "ri", "る": "ru",
        "れ": "re", "ろ": "ro",
        "わ": "wa", "を": "o",
        "ん": "n",
    }

    def analyze(self, text: str, language: str = "fa") -> List[Phoneme]:
        language = language.lower().strip()

        if language not in {"fa", "en", "ja"}:
            raise ValueError("Supported languages: fa, en, ja")

        if language == "fa":
            return self._persian(text)
        if language == "ja":
            return self._japanese(text)
        return self._english(text)

    def _persian(self, text: str) -> List[Phoneme]:
        result: List[Phoneme] = []

        for char in text:
            if char.isspace():
                continue

            if char in self.VOWELS_FA:
                result.append(
                    Phoneme(
                        symbol=char,
                        kind="vowel",
                        duration=self.VOWEL_DURATION,
                        energy=1.0,
                    )
                )
                continue

            symbol = self.FA_MAP.get(char)

            if symbol:
                result.append(
                    Phoneme(
                        symbol=symbol,
                        kind="consonant",
                        duration=self.CONSONANT_DURATION,
                        energy=0.72,
                    )
                )

        return result

    def _english(self, text: str) -> List[Phoneme]:
        result: List[Phoneme] = []

        for char in text.lower():
            if char.isspace():
                continue

            if char in self.VOWELS_EN:
                result.append(
                    Phoneme(
                        symbol=char,
                        kind="vowel",
                        duration=self.VOWEL_DURATION,
                        energy=1.0,
                    )
                )
                continue

            symbol = self.EN_MAP.get(char)

            if symbol:
                result.append(
                    Phoneme(
                        symbol=symbol,
                        kind="consonant",
                        duration=self.CONSONANT_DURATION,
                        energy=0.70,
                    )
                )

        return result

    def _japanese(self, text: str) -> List[Phoneme]:
        result: List[Phoneme] = []

        for char in text:
            if char.isspace():
                continue

            symbol = self.JA_MAP.get(char)

            if symbol:
                result.append(
                    Phoneme(
                        symbol=symbol,
                        kind="syllable",
                        duration=0.105,
                        energy=0.92,
                    )
                )

        return result

    def total_duration(self, phonemes: List[Phoneme]) -> float:
        return sum(item.duration for item in phonemes)

    def symbols(self, phonemes: List[Phoneme]) -> List[str]:
        return [item.symbol for item in phonemes]


_default_engine = NativePhonemeSpeech()


def text_to_phonemes(text: str, language: str = "fa") -> List[Phoneme]:
    return _default_engine.analyze(text, language)


if __name__ == "__main__":
    sample = text_to_phonemes("صدای خاموش", "fa")

    for phoneme in sample:
        print(
            phoneme.symbol,
            phoneme.kind,
            round(phoneme.duration, 3),
        )
