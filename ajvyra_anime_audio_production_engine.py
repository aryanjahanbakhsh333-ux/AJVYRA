from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class DialogueLine:
    dialogue_id: str
    character: str
    text: str
    language: str
    start: float
    duration: float
    audio_path: Optional[str] = None


class AJVYRAAudioProvider:
    def synthesize(
        self,
        text: str,
        language: str,
        character: str,
        output_path: Path,
    ) -> Path:
        raise NotImplementedError


class AJVYRAExistingTTSAdapter(AJVYRAAudioProvider):
    """
    Adapter for the AJVYRA TTS stack already created earlier.
    """

    def __init__(self, engine=None):
        self.engine = engine

    def synthesize(
        self,
        text: str,
        language: str,
        character: str,
        output_path: Path,
    ) -> Path:

        if self.engine is None:
            raise RuntimeError(
                "AJVYRA TTS engine is not connected."
            )

        if hasattr(self.engine, "synthesize"):
            result = self.engine.synthesize(
                text=text,
                language=language,
                character=character,
                output_path=str(output_path),
            )
        elif hasattr(self.engine, "generate"):
            result = self.engine.generate(
                text=text,
                language=language,
                character=character,
                output_path=str(output_path),
            )
        else:
            raise RuntimeError(
                "Connected TTS engine has no supported method."
            )

        result_path = Path(result or output_path)

        if not result_path.exists():
            raise RuntimeError(
                "TTS engine did not create the expected audio file."
            )

        return result_path


class AJVYRAAudioProductionEngine:
    def __init__(
        self,
        root: str = "generated/anime_production",
        provider: Optional[AJVYRAAudioProvider] = None,
    ):
        self.root = Path(root)
        self.provider = provider

    def generate_episode_audio(
        self,
        anime_id: str,
        episode_id: str,
        shot_plan: Dict[str, Any],
    ) -> Dict[str, Any]:

        if self.provider is None:
            raise RuntimeError(
                "No real audio/TTS provider configured."
            )

        episode_root = (
            self.root
            / anime_id
            / "season_01"
            / episode_id
        )

        audio_dir = episode_root / "audio"
        audio_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        dialogue = self._extract_dialogue(
            shot_plan
        )

        output_lines = []

        for line in dialogue:
            filename = (
                f"{line.dialogue_id}_"
                f"{line.language}_"
                f"{self._slug(line.character)}.wav"
            )

            output = audio_dir / filename

            self.provider.synthesize(
                text=line.text,
                language=line.language,
                character=line.character,
                output_path=output,
            )

            line.audio_path = str(output)
            output_lines.append(asdict(line))

        manifest = {
            "anime_id": anime_id,
            "episode_id": episode_id,
            "dialogue": output_lines,
        }

        manifest_path = audio_dir / "audio_manifest.json"

        manifest_path.write_text(
            json.dumps(
                manifest,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return manifest

    def _extract_dialogue(
        self,
        shot_plan: Dict[str, Any],
    ) -> List[DialogueLine]:

        lines = []
        current_time = 0.0
        counter = 1

        for shot in shot_plan.get("shots", []):
            shot_dialogue = shot.get("dialogue", [])

            if isinstance(shot_dialogue, str):
                shot_dialogue = [
                    {
                        "character": "unknown",
                        "text": shot_dialogue,
                    }
                ]

            for item in shot_dialogue:
                text = str(item.get("text", "")).strip()

                if not text:
                    continue

                duration = max(
                    1.0,
                    len(text.split()) / 2.5,
                )

                for language in ("fa", "ja"):
                    lines.append(
                        DialogueLine(
                            dialogue_id=f"dialogue_{counter:05d}",
                            character=item.get(
                                "character",
                                "unknown",
                            ),
                            text=text,
                            language=language,
                            start=current_time,
                            duration=duration,
                        )
                    )

                    counter += 1

            current_time += float(
                shot.get("duration", 8)
            )

        return lines

    @staticmethod
    def _slug(value: str) -> str:
        return "".join(
            c if c.isalnum() else "_"
            for c in value
        )[:40]
