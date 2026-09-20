from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
from typing import Optional


@dataclass
class VoiceRequest:
    text: str
    language: str
    voice_id: str
    output_file: Path

    speed: float = 1.0
    pitch: float = 1.0


class VoiceEngine:

    def __init__(self):
        self.engine = self.detect_engine()

    def detect_engine(self) -> Optional[str]:
        engines = [
            "espeak-ng",
            "espeak",
            "say"
        ]

        for engine in engines:
            if shutil.which(engine):
                return engine

        return None

    def available(self) -> bool:
        return self.engine is not None

    def synthesize(
        self,
        request: VoiceRequest
    ) -> Path:

        if not self.available():
            raise RuntimeError(
                "No local TTS engine is installed."
            )

        request.output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if self.engine == "say":
            command = [
                "say",
                "-o",
                str(request.output_file),
                request.text
            ]

        else:
            command = [
                self.engine,
                "-w",
                str(request.output_file),
                request.text
            ]

        subprocess.run(
            command,
            check=True
        )

        return request.output_file


def create_voice(
    text: str,
    language: str,
    voice_id: str,
    output_file: str
) -> Path:

    engine = VoiceEngine()

    request = VoiceRequest(
        text=text,
        language=language,
        voice_id=voice_id,
        output_file=Path(output_file)
    )

    return engine.synthesize(request)


if __name__ == "__main__":
    engine = VoiceEngine()

    print(
        "TTS engine:",
        engine.engine or "not available"
    )
