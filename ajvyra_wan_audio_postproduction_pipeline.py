from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


@dataclass
class AudioAsset:
    path: str
    kind: str
    start_seconds: float = 0.0
    volume: float = 1.0


@dataclass
class AudioPostProductionResult:
    video_input: str
    audio_assets: list[str]
    output_video: str
    success: bool
    error: str | None = None


class AJVYRAWanAudioPostProductionPipeline:

    VALID_AUDIO_EXTENSIONS = {
        ".wav",
        ".mp3",
        ".m4a",
        ".aac",
        ".flac",
        ".ogg",
    }

    def __init__(self, root: str | Path = "ajvyra_wan_audio") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _require_tool(tool: str) -> None:
        if shutil.which(tool) is None:
            raise RuntimeError(
                f"Required executable not found in PATH: {tool}"
            )

    def discover_assets(
        self,
        film_id: str,
    ) -> list[AudioAsset]:

        directory = self.root / film_id

        if not directory.exists():
            return []

        assets = []

        for path in sorted(directory.iterdir()):
            if path.suffix.lower() not in self.VALID_AUDIO_EXTENSIONS:
                continue

            assets.append(
                AudioAsset(
                    path=str(path),
                    kind="audio",
                )
            )

        return assets

    def write_manifest(
        self,
        film_id: str,
        assets: Iterable[AudioAsset],
    ) -> Path:

        path = self.root / film_id / "audio_manifest.json"
        path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "film_id": film_id,
            "assets": [asdict(asset) for asset in assets],
        }

        path.write_text(
            json.dumps(
                payload,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return path

    def mux(
        self,
        video_input: str | Path,
        output_video: str | Path,
        assets: list[AudioAsset] | None = None,
        require_audio: bool = True,
    ) -> AudioPostProductionResult:

        self._require_tool("ffmpeg")

        video_input = Path(video_input)
        output_video = Path(output_video)

        if not video_input.exists():
            raise FileNotFoundError(video_input)

        assets = assets or []

        if require_audio and not assets:
            return AudioPostProductionResult(
                video_input=str(video_input),
                audio_assets=[],
                output_video=str(output_video),
                success=False,
                error="No real audio assets were found.",
            )

        output_video.parent.mkdir(parents=True, exist_ok=True)

        if not assets:
            shutil.copy2(video_input, output_video)

            return AudioPostProductionResult(
                video_input=str(video_input),
                audio_assets=[],
                output_video=str(output_video),
                success=True,
            )

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(video_input),
        ]

        for asset in assets:
            asset_path = Path(asset.path)

            if not asset_path.exists():
                raise FileNotFoundError(asset_path)

            command.extend([
                "-i",
                str(asset_path),
            ])

        filter_parts = []

        for index, asset in enumerate(assets, start=1):
            volume = max(0.0, min(float(asset.volume), 3.0))

            filter_parts.append(
                f"[{index}:a]volume={volume}[a{index}]"
            )

        if len(assets) == 1:
            audio_map = "[a1]"
        else:
            inputs = "".join(
                f"[a{i}]"
                for i in range(1, len(assets) + 1)
            )

            filter_parts.append(
                f"{inputs}amix=inputs={len(assets)}:"
                f"duration=longest:dropout_transition=2[aout]"
            )

            audio_map = "[aout]"

        filter_complex = ";".join(filter_parts)

        command.extend([
            "-filter_complex",
            filter_complex,
            "-map",
            "0:v:0",
            "-map",
            audio_map,
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(output_video),
        ])

        completed = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if completed.returncode != 0:
            return AudioPostProductionResult(
                video_input=str(video_input),
                audio_assets=[asset.path for asset in assets],
                output_video=str(output_video),
                success=False,
                error=completed.stderr[-4000:],
            )

        return AudioPostProductionResult(
            video_input=str(video_input),
            audio_assets=[asset.path for asset in assets],
            output_video=str(output_video),
            success=True,
        )
