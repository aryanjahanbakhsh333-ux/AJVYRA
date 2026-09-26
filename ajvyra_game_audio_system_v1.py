from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AudioEvent:
    event_id: str
    kind: str
    source: str
    volume: float = 1.0
    loop: bool = False


class GameAudioSystem:
    def __init__(self):
        self.master_volume = 1.0
        self.music_volume = 0.7
        self.effects_volume = 1.0
        self.events: List[AudioEvent] = []

    def music(
        self,
        source: str,
        loop: bool = True,
    ) -> AudioEvent:
        event = AudioEvent(
            event_id=f"music_{len(self.events)}",
            kind="music",
            source=source,
            volume=self.music_volume,
            loop=loop,
        )

        self.events.append(event)
        return event

    def effect(
        self,
        source: str,
    ) -> AudioEvent:
        event = AudioEvent(
            event_id=f"sfx_{len(self.events)}",
            kind="effect",
            source=source,
            volume=self.effects_volume,
            loop=False,
        )

        self.events.append(event)
        return event

    def stop_all(self) -> None:
        self.events.clear()

    def export(self) -> Dict:
        return {
            "master_volume": self.master_volume,
            "music_volume": self.music_volume,
            "effects_volume": self.effects_volume,
            "events": [
                {
                    "id": event.event_id,
                    "kind": event.kind,
                    "source": event.source,
                    "volume": event.volume,
                    "loop": event.loop,
                }
                for event in self.events
            ],
        }
