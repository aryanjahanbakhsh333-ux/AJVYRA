from __future__ import annotations

import importlib
from pathlib import Path
from typing import Optional

import torch


class AJVYRADigitalVoiceEngine:

    DEFAULT_MODEL = (
        "KEYHAN-A/aava-tts-persian-3b"
    )

    def __init__(
        self,
        model_id: str | None = None,
        device: str | None = None,
    ):

        self.model_id = (
            model_id
            or self.DEFAULT_MODEL
        )

        self.device = (
            device
            or self._detect_device()
        )

        self._pipeline = None

    @staticmethod
    def _detect_device() -> str:

        if torch.cuda.is_available():
            return "cuda"

        if hasattr(
            torch.backends,
            "mps",
        ) and torch.backends.mps.is_available():
            return "mps"

        return "cpu"

    def _load(self):

        if self._pipeline is not None:
            return self._pipeline

        try:
            transformers = importlib.import_module(
                "transformers"
            )
        except ImportError as exc:
            raise RuntimeError(
                "Transformers is required. "
                "Install: pip install transformers"
            ) from exc

        pipeline = getattr(
            transformers,
            "pipeline",
        )

        self._pipeline = pipeline(
            "text-to-speech",
            model=self.model_id,
            device=(
                0
                if self.device == "cuda"
                else -1
            ),
        )

        return self._pipeline

    def generate(
        self,
        text: str,
        output_path: str | Path,
    ) -> Path:

        text = text.strip()

        if not text:
            raise ValueError(
                "Cannot synthesize empty text."
            )

        output_path = Path(
            output_path
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        pipe = self._load()

        result = pipe(text)

        audio = result["audio"]
        sample_rate = int(
            result["sampling_rate"]
        )

        import soundfile as sf

        sf.write(
            str(output_path),
            audio,
            sample_rate,
        )

        if (
            not output_path.exists()
            or output_path.stat().st_size < 1024
        ):
            raise RuntimeError(
                "TTS finished but no valid audio was created."
            )

        return output_path
