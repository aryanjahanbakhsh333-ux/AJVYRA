from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass
class AnimationKeyframe:
    frame: int
    x: float
    y: float
    scale: float
    expression: str


@dataclass
class LipSyncEvent:
    start: float
    end: float
    intensity: float = 1.0


@dataclass
class AnimationConfig:
    fps: int = 24
    blink_interval: float = 4.2
    blink_duration: float = 0.16


class NativeAnimationEngine:
    """
    Lightweight animation layer.

    Adds deterministic motion data, blinking, lip-sync timing,
    breathing and camera movement to scene descriptions.
    """

    def __init__(
        self,
        root: str | Path = "ajvyra_projects/animation",
        config: AnimationConfig | None = None,
    ):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

        self.config = config or AnimationConfig()

    def interpolate(
        self,
        keyframes: List[AnimationKeyframe],
        total_frames: int,
    ) -> List[dict]:
        if not keyframes:
            return []

        keyframes = sorted(
            keyframes,
            key=lambda item: item.frame,
        )

        result = []

        for frame in range(total_frames):
            previous = keyframes[0]
            following = keyframes[-1]

            for i in range(len(keyframes) - 1):
                a = keyframes[i]
                b = keyframes[i + 1]

                if a.frame <= frame <= b.frame:
                    previous = a
                    following = b
                    break

            if previous.frame == following.frame:
                t = 0.0
            else:
                t = (
                    frame - previous.frame
                ) / (
                    following.frame - previous.frame
                )

            t = max(0.0, min(1.0, t))

            x = previous.x + (following.x - previous.x) * t
            y = previous.y + (following.y - previous.y) * t
            scale = (
                previous.scale
                + (following.scale - previous.scale) * t
            )

            result.append(
                {
                    "frame": frame,
                    "x": x,
                    "y": y,
                    "scale": scale,
                    "expression": (
                        following.expression
                        if t > 0.5
                        else previous.expression
                    ),
                }
            )

        return result

    def breathing_offset(self, frame: int) -> float:
        return math.sin(frame * 0.10) * 0.003

    def blink(self, time_seconds: float) -> bool:
        cycle = time_seconds % self.config.blink_interval

        return cycle < self.config.blink_duration

    def lip_strength(
        self,
        time_seconds: float,
        events: Iterable[LipSyncEvent],
    ) -> float:
        strength = 0.0

        for event in events:
            if event.start <= time_seconds <= event.end:
                progress = (
                    time_seconds - event.start
                ) / max(
                    0.001,
                    event.end - event.start,
                )

                wave = (
                    math.sin(progress * math.pi * 8)
                    * 0.5
                    + 0.5
                )

                strength = max(
                    strength,
                    wave * event.intensity,
                )

        return strength

    def create_lip_events(
        self,
        duration: float,
        density: float = 5.0,
    ) -> List[LipSyncEvent]:
        events = []

        if duration <= 0:
            return events

        step = 1.0 / max(1.0, density)

        cursor = 0.0

        while cursor < duration:
            length = min(
                0.12 + (math.sin(cursor * 8) + 1) * 0.04,
                duration - cursor,
            )

            events.append(
                LipSyncEvent(
                    start=cursor,
                    end=cursor + length,
                    intensity=0.65 + (
                        math.sin(cursor * 3) + 1
                    ) * 0.17,
                )
            )

            cursor += step

        return events

    def build_animation(
        self,
        animation_id: str,
        duration_seconds: float,
        keyframes: List[AnimationKeyframe],
        speech_duration: float | None = None,
    ) -> Path:
        total_frames = max(
            1,
            int(duration_seconds * self.config.fps),
        )

        motion = self.interpolate(
            keyframes,
            total_frames,
        )

        speech_duration = (
            speech_duration
            if speech_duration is not None
            else duration_seconds
        )

        lip_events = self.create_lip_events(
            speech_duration
        )

        frames = []

        for item in motion:
            frame = item["frame"]
            time_seconds = frame / self.config.fps

            item["breathing"] = self.breathing_offset(frame)
            item["blink"] = self.blink(time_seconds)

            item["lip_strength"] = self.lip_strength(
                time_seconds,
                lip_events,
            )

            frames.append(item)

        output = self.root / f"{animation_id}.json"

        with output.open("w", encoding="utf-8") as f:
            json.dump(
                {
                    "animation_id": animation_id,
                    "fps": self.config.fps,
                    "duration_seconds": duration_seconds,
                    "frame_count": total_frames,
                    "frames": frames,
                },
                f,
                ensure_ascii=False,
            )

        return output


if __name__ == "__main__":
    engine = NativeAnimationEngine()

    output = engine.build_animation(
        animation_id="demo_scene",
        duration_seconds=5,
        keyframes=[
            AnimationKeyframe(
                frame=0,
                x=0.45,
                y=0.91,
                scale=1.20,
                expression="sad",
            ),
            AnimationKeyframe(
                frame=120,
                x=0.55,
                y=0.91,
                scale=1.28,
                expression="neutral",
            ),
        ],
        speech_duration=5,
    )

    print(f"Animation created: {output}")
