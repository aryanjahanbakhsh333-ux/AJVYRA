"""
AJVYRA AI VOICE GENERATION ENGINE

Unified voice layer.

Priority:

1. Configured external neural TTS endpoint
2. Existing AJVYRA native TTS
3. Existing AJVYRA TTS engine
4. Local system TTS fallback

Supports:
- Persian
- Japanese
- English
- emotions
- speaker identities
- WAV output
"""

from __future__ import annotations

import json
import os
import subprocess
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict


@dataclass
class VoiceRequest:

    project_id: str
    speaker_id: str
    text: str

    language: str = "fa"

    emotion: str = "neutral"

    speed: float = 1.0

    pitch: float = 0.0

    output_name: str = "voice.wav"


class AJVYRAAIVoiceGenerationEngine:

    def __init__(
        self,
        root: Path | str,
    ) -> None:

        self.root = Path(root).resolve()

        self.output_root = (
            self.root
            / "generated"
            / "voices"
        )

        self.output_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    # =========================================================
    # GENERATE
    # =========================================================

    def generate(
        self,
        request: VoiceRequest,
    ) -> Dict[str, Any]:

        output_dir = (
            self.output_root
            / request.project_id
            / request.language
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            output_dir
            / request.output_name
        )

        backend = None

        # -----------------------------------------------------
        # 1. EXTERNAL NEURAL TTS
        # -----------------------------------------------------

        if self._external_tts(
            request,
            output_path,
        ):
            backend = "external-neural-tts"

        # -----------------------------------------------------
        # 2. AJVYRA NATIVE TTS
        # -----------------------------------------------------

        elif self._native_tts(
            request,
            output_path,
        ):
            backend = "ajvyra-native-tts"

        # -----------------------------------------------------
        # 3. EXISTING TTS ENGINE
        # -----------------------------------------------------

        elif self._legacy_tts(
            request,
            output_path,
        ):
            backend = "ajvyra-tts-engine"

        # -----------------------------------------------------
        # 4. LOCAL FALLBACK
        # -----------------------------------------------------

        elif self._system_tts(
            request,
            output_path,
        ):
            backend = "system-tts"

        else:
            raise RuntimeError(
                "No voice backend could generate audio."
            )

        metadata = {
            "request": asdict(request),
            "backend": backend,
            "path": str(output_path),
        }

        metadata_path = (
            output_path.with_suffix(
                ".json"
            )
        )

        metadata_path.write_text(
            json.dumps(
                metadata,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return {
            "status": "generated",
            "path": str(output_path),
            "backend": backend,
            "metadata": str(metadata_path),
        }

    # =========================================================
    # EXTERNAL
    # =========================================================

    def _external_tts(
        self,
        request: VoiceRequest,
        output_path: Path,
    ) -> bool:

        endpoint = os.getenv(
            "AJVYRA_TTS_MODEL_URL",
            "",
        )

        if not endpoint:
            return False

        payload = json.dumps(
            asdict(request),
            ensure_ascii=False,
        ).encode("utf-8")

        try:

            req = urllib.request.Request(
                endpoint,
                data=payload,
                headers={
                    "Content-Type":
                        "application/json"
                },
                method="POST",
            )

            with urllib.request.urlopen(
                req,
                timeout=300,
            ) as response:

                data = response.read()

            output_path.write_bytes(
                data
            )

            return (
                output_path.exists()
                and output_path.stat().st_size > 100
            )

        except Exception:
            return False

    # =========================================================
    # NATIVE
    # =========================================================

    def _native_tts(
        self,
        request: VoiceRequest,
        output_path: Path,
    ) -> bool:

        try:

            from ajvyra_native_tts_engine import (
                NativeTTSEngine,
            )

            engine = NativeTTSEngine(
                root=self.root
            )

            method = getattr(
                engine,
                "synthesize",
                None,
            )

            if not callable(method):
                return False

            result = method(
                text=request.text,
                language=request.language,
                emotion=request.emotion,
                output_path=output_path,
            )

            return (
                output_path.exists()
                if result is None
                else bool(result)
            )

        except Exception:
            return False

    # =========================================================
    # LEGACY
    # =========================================================

    def _legacy_tts(
        self,
        request: VoiceRequest,
        output_path: Path,
    ) -> bool:

        try:

            from ajvyra_anime_tts_engine import (
                AJVYRAAnimeTTSEngine,
            )

            engine = AJVYRAAnimeTTSEngine(
                root=self.root
            )

            method = getattr(
                engine,
                "synthesize",
                None,
            )

            if not callable(method):
                return False

            result = method(
                text=request.text,
                language=request.language,
                output_path=output_path,
            )

            return (
                output_path.exists()
                if result is None
                else bool(result)
            )

        except Exception:
            return False

    # =========================================================
    # SYSTEM
    # =========================================================

    def _system_tts(
        self,
        request: VoiceRequest,
        output_path: Path,
    ) -> bool:

        # macOS
        if (
            subprocess.run(
                ["which", "say"],
                capture_output=True,
            ).returncode
            == 0
        ):

            try:

                aiff = output_path.with_suffix(
                    ".aiff"
                )

                process = subprocess.run(
                    [
                        "say",
                        "-o",
                        str(aiff),
                        request.text,
                    ],
                    capture_output=True,
                    text=True,
                )

                if process.returncode != 0:
                    return False

                return self._convert_audio(
                    aiff,
                    output_path,
                )

            except Exception:
                return False

        # Linux eSpeak
        if (
            subprocess.run(
                ["which", "espeak"],
                capture_output=True,
            ).returncode
            == 0
        ):

            try:

                process = subprocess.run(
                    [
                        "espeak",
                        "-w",
                        str(output_path),
                        request.text,
                    ],
                    capture_output=True,
                    text=True,
                )

                return (
                    process.returncode == 0
                    and output_path.exists()
                )

            except Exception:
                return False

        return False

    # =========================================================
    # AUDIO CONVERSION
    # =========================================================

    def _convert_audio(
        self,
        source: Path,
        target: Path,
    ) -> bool:

        try:

            process = subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(source),
                    "-ar",
                    "48000",
                    "-ac",
                    "2",
                    str(target),
                ],
                capture_output=True,
                text=True,
            )

            return (
                process.returncode == 0
                and target.exists()
            )

        except Exception:
            return False
