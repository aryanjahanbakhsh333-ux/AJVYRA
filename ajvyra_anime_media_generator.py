from pathlib import Path
from typing import List

from ajvyra_anime_voice_engine import (
    VoiceEngine,
    VoiceRequest
)


class MediaGenerator:

    def __init__(self, output_root="anime_assets"):
        self.output_root = Path(output_root)
        self.voice_engine = VoiceEngine()

    def generate_dialogue_audio(
        self,
        anime_id: int,
        dialogue_id: str,
        voice_id: str,
        text: str,
        language: str
    ) -> Path:

        output = (
            self.output_root
            / f"anime_{anime_id:02d}"
            / "voice"
            / language
            / f"{dialogue_id}.wav"
        )

        request = VoiceRequest(
            text=text,
            language=language,
            voice_id=voice_id,
            output_file=output
        )

        return self.voice_engine.synthesize(request)

    def generate_batch(
        self,
        anime_id: int,
        dialogue_items: List[dict]
    ) -> List[Path]:

        outputs = []

        for item in dialogue_items:
            outputs.append(
                self.generate_dialogue_audio(
                    anime_id=anime_id,
                    dialogue_id=item["dialogue_id"],
                    voice_id=item["voice_id"],
                    text=item["text"],
                    language=item["language"]
                )
            )

        return outputs


if __name__ == "__main__":
    generator = MediaGenerator()

    print(
        "Voice engine available:",
        generator.voice_engine.available()
    )
