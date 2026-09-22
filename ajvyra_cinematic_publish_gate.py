from __future__ import annotations

import json
import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

from ajvyra_cinematic_production_qc import (
    AJVYRACinematicProductionQC,
    QCResult,
)


@dataclass
class PublishDecision:
    film_id: str
    approved: bool
    source_file: Optional[str] = None
    public_file: Optional[str] = None
    checksum: Optional[str] = None
    reason: Optional[str] = None


class AJVYRACinematicPublishGate:

    def __init__(
        self,
        public_root: str | Path = "public/cinematic_anime",
    ):
        self.public_root = Path(
            public_root
        )

        self.qc = (
            AJVYRACinematicProductionQC()
        )

    def evaluate(
        self,
        film_id: str,
        movie_path: str | Path,
    ) -> PublishDecision:

        qc = self.qc.inspect(
            film_id,
            movie_path,
        )

        if not qc.passed:
            return PublishDecision(
                film_id=film_id,
                approved=False,
                source_file=str(
                    movie_path
                ),
                reason=(
                    "QC failed: "
                    + "; ".join(qc.issues)
                ),
            )

        return PublishDecision(
            film_id=film_id,
            approved=True,
            source_file=str(
                movie_path
            ),
        )

    def publish(
        self,
        decision: PublishDecision,
    ) -> PublishDecision:

        if not decision.approved:
            return decision

        if not decision.source_file:
            raise ValueError(
                "Approved publication requires "
                "a source file."
            )

        source = Path(
            decision.source_file
        )

        if not source.exists():
            raise FileNotFoundError(
                source
            )

        destination_dir = (
            self.public_root
            / decision.film_id
        )

        destination_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = (
            destination_dir / "movie.mp4"
        )

        destination.write_bytes(
            source.read_bytes()
        )

        checksum = self._sha256(
            destination
        )

        metadata = {
            "film_id": decision.film_id,
            "status": "READY",
            "file": "movie.mp4",
            "sha256": checksum,
        }

        (
            destination_dir / "metadata.json"
        ).write_text(
            json.dumps(
                metadata,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        decision.public_file = str(
            destination
        )

        decision.checksum = checksum

        return decision

    @staticmethod
    def _sha256(
        path: Path,
    ) -> str:

        digest = hashlib.sha256()

        with path.open("rb") as handle:
            while chunk := handle.read(
                1024 * 1024
            ):
                digest.update(chunk)

        return digest.hexdigest()
