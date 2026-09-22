from __future__ import annotations

import importlib
import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class VoiceRequest:
    film_id: str
    segment_index: int
    character_id: str
    text: str
    language: str
    emotion: str
    output_path: str


@dataclass
class VoiceResult:
    success: bool
    output_path: Optional[str]
    error: Optional[str] = None


class AJVYRAFinalVoiceBridge:

    def __init__(
        self,
        output_root: str | Path = "ajvyra_final_audio",
        external_command: str | None = None,
    ):

        self.root = Path(output_root)

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.external_command = external_command

    def _validate_output(
        self,
        path: Path,
    ) -> bool:

        return (
            path.exists()
            and path.is_file()
            and path.stat().st_size > 1024
        )

    def _try_existing_native_engine(
        self,
        request: VoiceRequest,
    ) -> VoiceResult:

        candidates = [
            (
                "ajvyra_anime_tts_engine",
                "AJVYRATTSengine",
            ),
            (
                "ajvyra_native_tts_engine",
                "AJVYRANativeTTSEngine",
            ),
            (
                "ajvyra_native_tts_bridge",
                "AJVYRANativeTTSBridge",
            ),
        ]

        last_error = None

        for module_name, class_name in candidates:

            try:
                module = importlib.import_module(
                    module_name
                )

                cls = getattr(
                    module,
                    class_name,
                )

                engine = cls()

                methods = [
                    "synthesize",
                    "generate",
                    "speak",
                    "create_audio",
                ]

                for method_name in methods:

                    method = getattr(
                        engine,
                        method_name,
                        None,
                    )

                    if not callable(method):
                        continue

                    try:
                        result = method(
                            text=request.text,
                            language=request.language,
                            emotion=request.emotion,
                            output_path=request.output_path,
                        )
                    except TypeError:

                        result = method(
                            request.text,
                            request.output_path,
                        )

                    output = Path(
                        request.output_path
                    )

                    if isinstance(result, str):
                        possible = Path(result)

                        if possible.exists():
                            output = possible

                    if self._validate_output(output):
                        return VoiceResult(
                            success=True,
                            output_path=str(output),
                        )

            except Exception as exc:
                last_error = str(exc)

        return VoiceResult(
            success=False,
            output_path=None,
            error=(
                last_error
                or "No compatible AJVYRA TTS engine was found."
            ),
        )

    def _run_external_tts(
        self,
        request: VoiceRequest,
    ) -> VoiceResult:

        if not self.external_command:
            return VoiceResult(
                success=False,
                output_path=None,
                error="No external TTS command configured.",
            )

        executable = self.external_command.split()[0]

        if shutil.which(executable) is None:
            return VoiceResult(
                success=False,
                output_path=None,
                error=f"TTS executable not found: {executable}",
            )

        command = self.external_command.format(
            text=request.text,
            language=request.language,
            emotion=request.emotion,
            output=request.output_path,
        )

        completed = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if completed.returncode != 0:
            return VoiceResult(
                success=False,
                output_path=None,
                error=completed.stderr[-3000:],
            )

        output = Path(
            request.output_path
        )

        if not self._validate_output(output):
            return VoiceResult(
                success=False,
                output_path=None,
                error="TTS completed but produced no valid audio file.",
            )

        return VoiceResult(
            success=True,
            output_path=str(output),
        )

    def synthesize(
        self,
        request: VoiceRequest,
    ) -> VoiceResult:

        output = Path(
            request.output_path
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if self._validate_output(output):
            return VoiceResult(
                success=True,
                output_path=str(output),
            )

        if self.external_command:
            return self._run_external_tts(
                request
            )

        return self._try_existing_native_engine(
            request
        )

    def save_manifest(
        self,
        film_id: str,
        requests: list[VoiceRequest],
    ) -> Path:

        path = (
            self.root
            / film_id
            / "voice_manifest.json"
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                [
                    request.__dict__
                    for request in requests
                ],
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return path
