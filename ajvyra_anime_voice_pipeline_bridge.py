from __future__ import annotations

import json
from pathlib import Path

from ajvyra_anime_digital_voice_producer import (
    AJVYRAAnimeDigitalVoiceProducer,
    AnimeDialogue,
)


class AJVYRAAnimeVoicePipelineBridge:

    def __init__(
        self,
        root: str | Path = "ajvyra_anime_voice_output",
    ):

        self.root = Path(root)

        self.producer = (
            AJVYRAAnimeDigitalVoiceProducer(
                root=self.root
            )
        )

    def load_dialogue(
        self,
        film_id: str,
        path: str | Path,
    ) -> list[AnimeDialogue]:

        data = json.loads(
            Path(path).read_text(
                encoding="utf-8"
            )
        )

        result = []

        for item in data:

            result.append(
                AnimeDialogue(
                    film_id=film_id,
                    segment_index=int(
                        item["segment_index"]
                    ),
                    character_id=str(
                        item["character_id"]
                    ),
                    character_name=str(
                        item["character_name"]
                    ),
                    text=str(
                        item["text"]
                    ),
                    emotion=str(
                        item.get(
                            "emotion",
                            "calm",
                        )
                    ),
                    start=float(
                        item.get(
                            "start",
                            0,
                        )
                    ),
                    end=float(
                        item.get(
                            "end",
                            0,
                        )
                    ),
                )
            )

        return result

    def produce_film_voices(
        self,
        film_id: str,
        dialogue_file: str | Path,
    ):

        dialogues = self.load_dialogue(
            film_id,
            dialogue_file,
        )

        profiles = {}

        results = []

        for dialogue in dialogues:

            if dialogue.character_id not in profiles:

                profiles[
                    dialogue.character_id
                ] = self.producer.create_character_voice(
                    character_id=dialogue.character_id,
                    character_name=dialogue.character_name,
                    personality=(
                        "cinematic anime character"
                    ),
                )

            result = (
                self.producer.produce_dialogue(
                    dialogue,
                    profiles[
                        dialogue.character_id
                    ],
                )
            )

            results.append(result)

        return results
