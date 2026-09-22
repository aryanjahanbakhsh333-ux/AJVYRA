from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List


class AJVYRAEpisodeRenderEngine:

    def __init__(
        self,
        root: str = "generated/anime_production",
        ffmpeg: str = "ffmpeg",
    ):
        self.root = Path(root)
        self.ffmpeg = ffmpeg

    def render_episode(
        self,
        anime_id: str,
        episode_id: str,
        shot_plan: Dict[str, Any],
    ) -> Path:

        episode_root = (
            self.root
            / anime_id
            / "season_01"
            / episode_id
        )

        media_dir = episode_root / "media"
        audio_dir = episode_root / "audio"
        subtitle_dir = episode_root / "subtitles"
        render_dir = episode_root / "renders"

        render_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        videos = self._collect_videos(
            media_dir,
            shot_plan,
        )

        if not videos:
            raise RuntimeError(
                "No generated video shots were found."
            )

        normalized = self._normalize_videos(
            videos,
            render_dir,
        )

        silent_video = render_dir / "video_concat.mp4"

        self._concat_videos(
            normalized,
            silent_video,
        )

        audio_manifest = (
            audio_dir / "audio_manifest.json"
        )

        final_video = (
            episode_root
            / "episode.mp4"
        )

        if audio_manifest.exists():
            mixed_audio = (
                render_dir / "dialogue_mix.wav"
            )

            self._build_audio_mix(
                audio_manifest,
                mixed_audio,
            )

            self._mux(
                silent_video,
                mixed_audio,
                final_video,
            )
        else:
            shutil.copy2(
                silent_video,
                final_video,
            )

        report = self._inspect(
            final_video,
            shot_plan,
        )

        (
            episode_root / "render_report.json"
        ).write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return final_video

    def _collect_videos(
        self,
        media_dir: Path,
        shot_plan: Dict[str, Any],
    ) -> List[Path]:

        result = []

        for shot in shot_plan.get("shots", []):
            shot_id = shot["shot_id"]

            candidates = [
                media_dir / f"{shot_id}.mp4",
                media_dir / f"{shot_id}.MP4",
            ]

            found = next(
                (
                    path
                    for path in candidates
                    if path.exists()
                ),
                None,
            )

            if found:
                result.append(found)

        return result

    def _normalize_videos(
        self,
        videos: List[Path],
        output_dir: Path,
    ) -> List[Path]:

        normalized = []

        for index, video in enumerate(
            videos,
            start=1,
        ):
            output = (
                output_dir
                / f"normalized_{index:05d}.mp4"
            )

            command = [
                self.ffmpeg,
                "-y",
                "-i",
                str(video),
                "-vf",
                "scale=1280:720:force_original_aspect_ratio=decrease,"
                "pad=1280:720:(ow-iw)/2:(oh-ih)/2",
                "-r",
                "24",
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "20",
                "-pix_fmt",
                "yuv420p",
                "-an",
                str(output),
            ]

            self._run(command)
            normalized.append(output)

        return normalized

    def _concat_videos(
        self,
        videos: List[Path],
        output: Path,
    ):

        list_file = output.parent / "concat.txt"

        lines = []

        for video in videos:
            safe_path = str(
                video.resolve()
            ).replace("'", "'\\''")

            lines.append(
                f"file '{safe_path}'"
            )

        list_file.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        command = [
            self.ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_file),
            "-c",
            "copy",
            str(output),
        ]

        self._run(command)

    def _build_audio_mix(
        self,
        manifest_path: Path,
        output: Path,
    ):

        data = json.loads(
            manifest_path.read_text(
                encoding="utf-8"
            )
        )

        lines = [
            item
            for item in data.get(
                "dialogue",
                []
            )
            if item.get("audio_path")
        ]

        if not lines:
            raise RuntimeError(
                "Audio manifest contains no audio."
            )

        inputs = []
        filters = []

        for index, item in enumerate(lines):
            path = Path(item["audio_path"])

            inputs.extend(
                ["-i", str(path)]
            )

            delay = int(
                float(
                    item.get("start", 0)
                ) * 1000
            )

            filters.append(
                f"[{index}:a]"
                f"adelay={delay}|{delay}"
                f"[a{index}]"
            )

        labels = "".join(
            f"[a{i}]"
            for i in range(len(lines))
        )

        filters.append(
            f"{labels}amix="
            f"inputs={len(lines)}:"
            f"duration=longest:"
            f"dropout_transition=2"
            "[mix]"
        )

        command = [
            self.ffmpeg,
            "-y",
            *inputs,
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[mix]",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(output),
        ]

        self._run(command)

    def _mux(
        self,
        video: Path,
        audio: Path,
        output: Path,
    ):

        command = [
            self.ffmpeg,
            "-y",
            "-i",
            str(video),
            "-i",
            str(audio),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-shortest",
            str(output),
        ]

        self._run(command)

    def _inspect(
        self,
        output: Path,
        shot_plan: Dict[str, Any],
    ) -> Dict[str, Any]:

        return {
            "exists": output.exists(),
            "size_bytes": (
                output.stat().st_size
                if output.exists()
                else 0
            ),
            "expected_duration_seconds": (
                shot_plan.get(
                    "target_duration_seconds"
                )
            ),
            "shot_count": len(
                shot_plan.get("shots", [])
            ),
            "file": str(output),
        }

    def _run(self, command: List[str]):

        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if process.returncode != 0:
            raise RuntimeError(
                "FFmpeg failed:\n"
                + process.stderr[-5000:]
            )
