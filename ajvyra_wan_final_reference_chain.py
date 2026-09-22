from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


@dataclass
class ReferenceFrame:
    film_id: str
    segment_index: int
    frame_path: str
    source: str
    sha256: str


@dataclass
class ContinuitySnapshot:
    film_id: str
    segment_index: int

    previous_frame: Optional[str]

    characters: list[dict]
    locations: list[dict]

    costume_state: dict
    lighting_state: dict

    continuity_hash: str


class AJVYRAWanFinalReferenceChain:

    def __init__(
        self,
        root: str | Path = "ajvyra_final_references",
    ):

        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def sha256(
        path: str | Path,
    ) -> str:

        digest = hashlib.sha256()

        with Path(path).open("rb") as handle:
            while True:
                block = handle.read(1024 * 1024)

                if not block:
                    break

                digest.update(block)

        return digest.hexdigest()

    def register_frame(
        self,
        film_id: str,
        segment_index: int,
        frame_path: str,
        source: str = "previous_segment",
    ) -> ReferenceFrame:

        path = Path(frame_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Reference frame not found: {path}"
            )

        reference = ReferenceFrame(
            film_id=film_id,
            segment_index=segment_index,
            frame_path=str(path),
            source=source,
            sha256=self.sha256(path),
        )

        output = (
            self.root
            / film_id
            / f"reference_{segment_index:04d}.json"
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            json.dumps(
                asdict(reference),
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return reference

    def latest_reference(
        self,
        film_id: str,
    ) -> Optional[ReferenceFrame]:

        directory = self.root / film_id

        if not directory.exists():
            return None

        files = sorted(
            directory.glob("reference_*.json")
        )

        if not files:
            return None

        data = json.loads(
            files[-1].read_text(
                encoding="utf-8"
            )
        )

        return ReferenceFrame(**data)

    def create_snapshot(
        self,
        film_id: str,
        segment_index: int,
        characters: list[dict],
        locations: list[dict],
        costume_state: dict,
        lighting_state: dict,
    ) -> ContinuitySnapshot:

        previous = self.latest_reference(
            film_id
        )

        payload = {
            "film_id": film_id,
            "segment_index": segment_index,
            "previous_frame": (
                previous.frame_path
                if previous
                else None
            ),
            "characters": characters,
            "locations": locations,
            "costume_state": costume_state,
            "lighting_state": lighting_state,
        }

        raw = json.dumps(
            payload,
            sort_keys=True,
            ensure_ascii=False,
        )

        continuity_hash = hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()

        return ContinuitySnapshot(
            film_id=film_id,
            segment_index=segment_index,
            previous_frame=(
                previous.frame_path
                if previous
                else None
            ),
            characters=characters,
            locations=locations,
            costume_state=costume_state,
            lighting_state=lighting_state,
            continuity_hash=continuity_hash,
        )

    def build_prompt(
        self,
        base_prompt: str,
        snapshot: ContinuitySnapshot,
    ) -> str:

        character_text = " ".join(
            str(item)
            for item in snapshot.characters
        )

        location_text = " ".join(
            str(item)
            for item in snapshot.locations
        )

        return (
            f"{base_prompt}\n\n"
            "CONTINUITY LOCK:\n"
            f"Characters: {character_text}\n"
            f"Locations: {location_text}\n"
            f"Costume state: {snapshot.costume_state}\n"
            f"Lighting state: {snapshot.lighting_state}\n"
            f"Continuity hash: {snapshot.continuity_hash}\n"
            "Preserve identity, facial structure, hairstyle, "
            "clothing, age, proportions, environment and "
            "cinematic visual language from the preceding shot."
        )
