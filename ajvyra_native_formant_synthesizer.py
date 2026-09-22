from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class FormantProfile:
    f1: float
    f2: float
    f3: float
    bandwidth1: float
    bandwidth2: float
    bandwidth3: float


class NativeFormantSynthesizer:
    """
    Algorithmic formant/resonance synthesizer.

    No pretrained model is used.
    Vowels receive different resonance structures, while consonants
    are represented through harmonic/noise mixtures.
    """

    SAMPLE_RATE = 22050

    VOWELS: Dict[str, FormantProfile] = {
        "a": FormantProfile(730, 1090, 2440, 90, 110, 170),
        "e": FormantProfile(530, 1840, 2480, 80, 100, 160),
        "i": FormantProfile(300, 2200, 3000, 70, 90, 150),
        "o": FormantProfile(570, 840, 2410, 80, 100, 170),
        "u": FormantProfile(440, 1020, 2240, 75, 100, 160),
    }

    SYMBOL_TO_VOWEL = {
        "ا": "a",
        "آ": "a",
        "اَ": "a",
        "َ": "a",
        "ِ": "i",
        "ُ": "u",
        "ی": "i",
        "و": "u",
        "a": "a",
        "e": "e",
        "i": "i",
        "o": "o",
        "u": "u",
    }

    VOICED = {
        "b", "d", "g", "v", "z", "ʒ",
        "m", "n", "l", "ɾ", "ɹ",
        "j", "w", "r", "y",
    }

    def __init__(self, sample_rate: int = SAMPLE_RATE, seed: int = 9137):
        self.sample_rate = int(sample_rate)
        self.random = random.Random(seed)

    def synthesize_phoneme(
        self,
        symbol: str,
        duration: float,
        frequency: float = 180.0,
        energy: float = 1.0,
    ) -> List[float]:

        count = max(1, int(duration * self.sample_rate))
        vowel = self._resolve_vowel(symbol)

        if vowel:
            return self._vowel(
                self.VOWELS[vowel],
                count,
                frequency,
                energy,
            )

        return self._consonant(
            symbol,
            count,
            frequency,
            energy,
        )

    def render_sequence(
        self,
        phonemes: Iterable,
        frequency: float = 180.0,
        energy: float = 1.0,
    ) -> List[float]:

        output: List[float] = []

        for item in phonemes:
            symbol = getattr(item, "symbol", str(item))
            duration = float(getattr(item, "duration", 0.1))
            item_energy = float(getattr(item, "energy", energy))

            output.extend(
                self.synthesize_phoneme(
                    symbol,
                    duration,
                    frequency,
                    item_energy,
                )
            )

        return output

    def _resolve_vowel(self, symbol: str) -> str | None:
        if symbol in self.SYMBOL_TO_VOWEL:
            return self.SYMBOL_TO_VOWEL[symbol]

        lowered = symbol.lower()

        if lowered in self.SYMBOL_TO_VOWEL:
            return self.SYMBOL_TO_VOWEL[lowered]

        for key, value in self.SYMBOL_TO_VOWEL.items():
            if key and key in lowered:
                return value

        return None

    def _vowel(
        self,
        profile: FormantProfile,
        count: int,
        fundamental: float,
        energy: float,
    ) -> List[float]:

        result: List[float] = []

        for index in range(count):
            t = index / self.sample_rate
            progress = index / max(1, count - 1)

            envelope = self._envelope(progress)

            source = 0.0

            harmonic_count = max(
                3,
                min(18, int((self.sample_rate / 2) / fundamental)),
            )

            for harmonic in range(1, harmonic_count + 1):
                source += (
                    math.sin(
                        2.0
                        * math.pi
                        * fundamental
                        * harmonic
                        * t
                    )
                    / (harmonic ** 0.78)
                )

            source /= harmonic_count ** 0.35

            resonance = (
                self._resonance(t, profile.f1, profile.bandwidth1)
                + self._resonance(t, profile.f2, profile.bandwidth2)
                + self._resonance(t, profile.f3, profile.bandwidth3)
            ) / 3.0

            vibrato = 1.0 + (
                0.012
                * math.sin(2.0 * math.pi * 5.2 * t)
            )

            result.append(
                source
                * (0.55 + resonance * 0.45)
                * envelope
                * energy
                * vibrato
            )

        return result

    def _consonant(
        self,
        symbol: str,
        count: int,
        frequency: float,
        energy: float,
    ) -> List[float]:

        voiced = symbol in self.VOICED
        result: List[float] = []

        for index in range(count):
            progress = index / max(1, count - 1)
            envelope = self._envelope(progress)

            noise = self.random.uniform(-1.0, 1.0)

            harmonic = math.sin(
                2.0
                * math.pi
                * max(70.0, frequency)
                * index
                / self.sample_rate
            )

            if voiced:
                value = (
                    harmonic * 0.45
                    + noise * 0.30
                )
            else:
                value = noise * 0.82

            result.append(
                value * envelope * energy
            )

        return result

    @staticmethod
    def _envelope(progress: float) -> float:
        attack = min(1.0, progress / 0.12)
        release = min(1.0, (1.0 - progress) / 0.16)
        return max(0.0, min(1.0, attack * release))

    @staticmethod
    def _resonance(
        t: float,
        frequency: float,
        bandwidth: float,
    ) -> float:

        width = max(10.0, bandwidth)

        return (
            0.5
            + 0.5
            * math.sin(
                2.0
                * math.pi
                * frequency
                * t
            )
        ) * math.exp(
            -width
            * (t % (1.0 / max(frequency, 1.0)))
        )


def normalize(samples: List[float], peak: float = 0.92) -> List[float]:
    if not samples:
        return []

    maximum = max(abs(value) for value in samples)

    if maximum <= 1e-9:
        return samples[:]

    scale = peak / maximum

    return [
        max(-1.0, min(1.0, value * scale))
        for value in samples
    ]
