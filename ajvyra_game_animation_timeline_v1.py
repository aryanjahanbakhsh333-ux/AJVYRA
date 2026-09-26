from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class AnimationKeyframe:
    time: float
    values: Dict[str, Any]


class AnimationTimeline:
    def __init__(self):
        self.tracks: Dict[
            str,
            List[AnimationKeyframe]
        ] = {}

    def add_keyframe(
        self,
        object_id: str,
        time_position: float,
        **values: Any,
    ) -> None:
        track = self.tracks.setdefault(
            object_id,
            [],
        )

        track.append(
            AnimationKeyframe(
                time=float(time_position),
                values=values,
            )
        )

        track.sort(
            key=lambda frame: frame.time
        )

    def sample(
        self,
        object_id: str,
        time_position: float,
    ) -> Dict[str, Any]:
        track = self.tracks.get(object_id, [])

        if not track:
            return {}

        previous = track[0]
        next_frame = track[-1]

        for frame in track:
            if frame.time <= time_position:
                previous = frame

            if frame.time >= time_position:
                next_frame = frame
                break

        if previous.time == next_frame.time:
            return dict(previous.values)

        ratio = (
            time_position - previous.time
        ) / (
            next_frame.time - previous.time
        )

        result: Dict[str, Any] = {}

        keys = set(
            previous.values
        ) | set(
            next_frame.values
        )

        for key in keys:
            a = previous.values.get(key)
            b = next_frame.values.get(key)

            if (
                isinstance(a, (int, float))
                and isinstance(b, (int, float))
            ):
                result[key] = (
                    a + (b - a) * ratio
                )
            else:
                result[key] = (
                    b if ratio >= 0.5 else a
                )

        return result

    def export(self) -> Dict[str, Any]:
        return {
            object_id: [
                {
                    "time": frame.time,
                    "values": frame.values,
                }
                for frame in frames
            ]
            for object_id, frames
            in self.tracks.items()
        }
