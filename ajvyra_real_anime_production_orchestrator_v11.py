"""
AJVYRA — Real Anime Production Orchestrator v11

Pipeline:

Anime Story
    ↓
Episode Plan
    ↓
Shot Plan
    ↓
Video Generation Backend
    ↓
Real MP4 Shots
    ↓
FFmpeg Assembly
    ↓
Final Episode MP4
    ↓
Media Manifest
    ↓
AJVYRA Public Media

IMPORTANT:
- No placeholder video generation.
- No fake "completed" state.
- A shot is successful only when a real media file exists.
- The orchestrator does not pretend to generate video itself.
- The actual video model backend must be connected through the configured
  ComfyUI/Wan endpoint.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib import request, error


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(
    os.getenv(
        "AJVYRA_ROOT",
        Path(__file__).resolve().parent
    )
)

PRODUCTION_ROOT = PROJECT_ROOT / "production" / "anime"

EPISODES_ROOT = PRODUCTION_ROOT / "episodes"
SHOTS_ROOT = PRODUCTION_ROOT / "shots"
FINAL_ROOT = PRODUCTION_ROOT / "final"
MANIFEST_ROOT = PRODUCTION_ROOT / "manifests"

COMFYUI_URL = os.getenv(
    "AJVYRA_COMFYUI_URL",
    "http://127.0.0.1:8188"
).rstrip("/")

COMFYUI_CLIENT_ID = os.getenv(
    "AJVYRA_COMFYUI_CLIENT_ID",
    f"ajvyra-{uuid.uuid4()}"
)

FFMPEG_BIN = os.getenv("AJVYRA_FFMPEG", "ffmpeg")

REQUEST_TIMEOUT = int(
    os.getenv("AJVYRA_REQUEST_TIMEOUT", "60")
)

SHOT_TIMEOUT = int(
    os.getenv("AJVYRA_SHOT_TIMEOUT", "3600")
)

POLL_INTERVAL = float(
    os.getenv("AJVYRA_POLL_INTERVAL", "2.0")
)


# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class ShotSpec:
    shot_id: str
    episode_id: str
    index: int
    prompt: str
    negative_prompt: str = ""
    duration_seconds: float = 5.0
    width: int = 1280
    height: int = 720
    fps: int = 24
    seed: Optional[int] = None


@dataclass
class GeneratedShot:
    shot_id: str
    episode_id: str
    index: int
    output_path: str
    duration_seconds: float
    generated_at: float
    backend: str
    prompt_id: Optional[str] = None


@dataclass
class EpisodeSpec:
    episode_id: str
    title: str
    description: str
    language: str
    target_duration_seconds: int
    shots: List[ShotSpec]


# ============================================================
# FILESYSTEM
# ============================================================

def ensure_directories() -> None:
    for directory in (
        PRODUCTION_ROOT,
        EPISODES_ROOT,
        SHOTS_ROOT,
        FINAL_ROOT,
        MANIFEST_ROOT,
    ):
        directory.mkdir(parents=True, exist_ok=True)


def atomic_write_json(
    path: Path,
    payload: Dict[str, Any]
) -> None:

    path.parent.mkdir(parents=True, exist_ok=True)

    temporary = path.with_suffix(
        path.suffix + ".tmp"
    )

    temporary.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    temporary.replace(path)


# ============================================================
# HTTP
# ============================================================

def http_json(
    url: str,
    method: str = "GET",
    payload: Optional[Dict[str, Any]] = None,
    timeout: int = REQUEST_TIMEOUT
) -> Dict[str, Any]:

    body = None

    headers = {
        "Accept": "application/json",
    }

    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = request.Request(
        url,
        data=body,
        headers=headers,
        method=method
    )

    try:
        with request.urlopen(
            req,
            timeout=timeout
        ) as response:

            raw = response.read()

            if not raw:
                return {}

            return json.loads(
                raw.decode("utf-8")
            )

    except error.HTTPError as exc:
        body = exc.read().decode(
            "utf-8",
            errors="replace"
        )

        raise RuntimeError(
            f"HTTP {exc.code} from {url}: {body}"
        ) from exc

    except error.URLError as exc:
        raise RuntimeError(
            f"Cannot connect to {url}: {exc}"
        ) from exc


# ============================================================
# COMFYUI BACKEND
# ============================================================

class ComfyUIBackend:
    """
    Real generation backend.

    This class submits a real workflow to ComfyUI.
    It never creates synthetic MP4 files.
    """

    def __init__(
        self,
        base_url: str = COMFYUI_URL
    ):
        self.base_url = base_url.rstrip("/")

    def check_connection(self) -> bool:

        try:
            http_json(
                f"{self.base_url}/system_stats",
                timeout=10
            )

            return True

        except Exception:
            return False

    def submit_workflow(
        self,
        workflow: Dict[str, Any]
    ) -> str:

        payload = {
            "prompt": workflow,
            "client_id": COMFYUI_CLIENT_ID
        }

        response = http_json(
            f"{self.base_url}/prompt",
            method="POST",
            payload=payload
        )

        prompt_id = response.get("prompt_id")

        if not prompt_id:
            raise RuntimeError(
                "ComfyUI did not return a prompt_id."
            )

        return prompt_id

    def get_history(
        self,
        prompt_id: str
    ) -> Dict[str, Any]:

        return http_json(
            f"{self.base_url}/history/{prompt_id}"
        )

    def wait_for_completion(
        self,
        prompt_id: str
    ) -> Dict[str, Any]:

        started = time.time()

        while True:

            if time.time() - started > SHOT_TIMEOUT:
                raise TimeoutError(
                    f"Generation timed out: {prompt_id}"
                )

            history = self.get_history(
                prompt_id
            )

            if prompt_id in history:

                result = history[prompt_id]

                status = result.get(
                    "status",
                    {}
                )

                completed = status.get(
                    "completed",
                    False
                )

                if completed:
                    return result

                status_messages = status.get(
                    "status_str",
                    ""
                )

                if status_messages == "error":
                    raise RuntimeError(
                        f"ComfyUI generation failed: "
                        f"{json.dumps(result, ensure_ascii=False)}"
                    )

            time.sleep(POLL_INTERVAL)


# ============================================================
# WORKFLOW ADAPTER
# ============================================================

class WorkflowAdapter:
    """
    Converts a ShotSpec into a ComfyUI workflow.

    The workflow itself is supplied externally as a JSON template.
    This keeps the orchestrator independent from a particular
    Wan/ComfyUI node graph.
    """

    def __init__(
        self,
        template_path: Path
    ):
        self.template_path = template_path

        if not template_path.exists():
            raise FileNotFoundError(
                f"Workflow template not found: {template_path}"
            )

        self.template = json.loads(
            template_path.read_text(
                encoding="utf-8"
            )
        )

    def build(
        self,
        shot: ShotSpec
    ) -> Dict[str, Any]:

        workflow = json.loads(
            json.dumps(self.template)
        )

        serialized = json.dumps(
            workflow,
            ensure_ascii=False
        )

        replacements = {
            "{{AJVYRA_PROMPT}}": shot.prompt,
            "{{AJVYRA_NEGATIVE_PROMPT}}": shot.negative_prompt,
            "{{AJVYRA_WIDTH}}": str(shot.width),
            "{{AJVYRA_HEIGHT}}": str(shot.height),
            "{{AJVYRA_FPS}}": str(shot.fps),
            "{{AJVYRA_DURATION}}": str(
                shot.duration_seconds
            ),
            "{{AJVYRA_SEED}}": str(
                shot.seed
                if shot.seed is not None
                else int(time.time())
            ),
            "{{AJVYRA_SHOT_ID}}": shot.shot_id,
        }

        for key, value in replacements.items():
            serialized = serialized.replace(
                key,
                value
            )

        return json.loads(serialized)


# ============================================================
# OUTPUT EXTRACTION
# ============================================================

def extract_video_outputs(
    history: Dict[str, Any]
) -> List[str]:

    outputs: List[str] = []

    outputs_data = history.get(
        "outputs",
        {}
    )

    for node_output in outputs_data.values():

        videos = node_output.get(
            "gifs",
            []
        )

        for item in videos:

            filename = item.get("filename")

            if filename:
                outputs.append(filename)

        video_items = node_output.get(
            "videos",
            []
        )

        for item in video_items:

            filename = item.get("filename")

            if filename:
                outputs.append(filename)

    return outputs


# ============================================================
# COMFYUI FILE DOWNLOAD
# ============================================================

def download_output(
    backend: ComfyUIBackend,
    filename: str,
    destination: Path
) -> Path:

    url = (
        f"{backend.base_url}/view"
        f"?filename={filename}"
        f"&type=output"
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    req = request.Request(
        url,
        headers={
            "Accept": "*/*"
        }
    )

    with request.urlopen(
        req,
        timeout=REQUEST_TIMEOUT
    ) as response:

        data = response.read()

    if not data:
        raise RuntimeError(
            f"Empty media output: {filename}"
        )

    destination.write_bytes(data)

    if destination.stat().st_size <= 0:
        raise RuntimeError(
            f"Invalid downloaded media: {destination}"
        )

    return destination


# ============================================================
# SHOT GENERATION
# ============================================================

class RealShotGenerator:

    def __init__(
        self,
        backend: ComfyUIBackend,
        workflow_adapter: WorkflowAdapter
    ):
        self.backend = backend
        self.workflow_adapter = workflow_adapter

    def generate(
        self,
        shot: ShotSpec
    ) -> GeneratedShot:

        if not self.backend.check_connection():
            raise RuntimeError(
                "Real video backend is not reachable. "
                "Generation cannot continue."
            )

        workflow = self.workflow_adapter.build(
            shot
        )

        prompt_id = self.backend.submit_workflow(
            workflow
        )

        history = self.backend.wait_for_completion(
            prompt_id
        )

        outputs = extract_video_outputs(
            history
        )

        if not outputs:
            raise RuntimeError(
                f"No real video output returned for "
                f"shot {shot.shot_id}"
            )

        source_filename = outputs[0]

        shot_directory = (
            SHOTS_ROOT /
            shot.episode_id
        )

        destination = (
            shot_directory /
            f"{shot.index:04d}_{shot.shot_id}.mp4"
        )

        download_output(
            self.backend,
            source_filename,
            destination
        )

        return GeneratedShot(
            shot_id=shot.shot_id,
            episode_id=shot.episode_id,
            index=shot.index,
            output_path=str(
                destination.relative_to(
                    PROJECT_ROOT
                )
            ),
            duration_seconds=shot.duration_seconds,
            generated_at=time.time(),
            backend="comfyui"
                ,
            prompt_id=prompt_id
        )


# ============================================================
# VIDEO ASSEMBLY
# ============================================================

class EpisodeAssembler:

    def __init__(
        self,
        ffmpeg_bin: str = FFMPEG_BIN
    ):
        self.ffmpeg_bin = ffmpeg_bin

    def verify_ffmpeg(self) -> None:

        result = subprocess.run(
            [
                self.ffmpeg_bin,
                "-version"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                "FFmpeg is not available."
            )

    def assemble(
        self,
        episode: EpisodeSpec,
        shots: List[GeneratedShot]
    ) -> Path:

        self.verify_ffmpeg()

        if not shots:
            raise RuntimeError(
                "Cannot assemble an episode with zero shots."
            )

        ordered = sorted(
            shots,
            key=lambda x: x.index
        )

        episode_directory = (
            EPISODES_ROOT /
            episode.episode_id
        )

        episode_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        concat_file = (
            episode_directory /
            "concat.txt"
        )

        lines = []

        for shot in ordered:

            absolute = (
                PROJECT_ROOT /
                shot.output_path
            )

            if not absolute.exists():
                raise FileNotFoundError(
                    f"Missing real shot: {absolute}"
                )

            lines.append(
                f"file '{absolute.as_posix()}'"
            )

        concat_file.write_text(
            "\n".join(lines),
            encoding="utf-8"
        )

        final_path = (
            FINAL_ROOT /
            f"{episode.episode_id}.mp4"
        )

        command = [
            self.ffmpeg_bin,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(final_path)
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                "FFmpeg assembly failed:\n"
                + result.stderr
            )

        if not final_path.exists():
            raise RuntimeError(
                "FFmpeg reported success but "
                "the final MP4 does not exist."
            )

        if final_path.stat().st_size <= 0:
            raise RuntimeError(
                "Final MP4 is empty."
            )

        return final_path


# ============================================================
# MANIFEST
# ============================================================

def write_episode_manifest(
    episode: EpisodeSpec,
    generated_shots: List[GeneratedShot],
    final_path: Path
) -> Path:

    manifest = {
        "schema": "ajvyra.anime.production.v11",
        "production": {
            "status": "generated",
            "real_media_required": True,
            "generated_at": time.time(),
        },
        "episode": {
            "episode_id": episode.episode_id,
            "title": episode.title,
            "description": episode.description,
            "language": episode.language,
            "target_duration_seconds":
                episode.target_duration_seconds,
            "final_media": str(
                final_path.relative_to(
                    PROJECT_ROOT
                )
            ),
        },
        "shots": [
            asdict(shot)
            for shot in generated_shots
        ]
    }

    path = (
        MANIFEST_ROOT /
        f"{episode.episode_id}.json"
    )

    atomic_write_json(
        path,
        manifest
    )

    return path


# ============================================================
# FULL PRODUCTION
# ============================================================

class AJVYRAAnimeProduction:

    def __init__(
        self,
        workflow_template: Path
    ):

        ensure_directories()

        self.backend = ComfyUIBackend()

        self.workflow_adapter = (
            WorkflowAdapter(
                workflow_template
            )
        )

        self.generator = (
            RealShotGenerator(
                self.backend,
                self.workflow_adapter
            )
        )

        self.assembler = (
            EpisodeAssembler()
        )

    def produce_episode(
        self,
        episode: EpisodeSpec
    ) -> Dict[str, Any]:

        if not episode.shots:
            raise ValueError(
                "Episode contains no shots."
            )

        generated: List[GeneratedShot] = []

        for shot in sorted(
            episode.shots,
            key=lambda item: item.index
        ):

            result = self.generator.generate(
                shot
            )

            generated.append(result)

        final_path = (
            self.assembler.assemble(
                episode,
                generated
            )
        )

        manifest_path = (
            write_episode_manifest(
                episode,
                generated,
                final_path
            )
        )

        return {
            "episode_id": episode.episode_id,
            "status": "generated",
            "final_video": str(
                final_path.relative_to(
                    PROJECT_ROOT
                )
            ),
            "manifest": str(
                manifest_path.relative_to(
                    PROJECT_ROOT
                )
            ),
            "shot_count": len(generated),
        }


# ============================================================
# EXAMPLE ENTRYPOINT
# ============================================================

def load_episode(
    path: Path
) -> EpisodeSpec:

    data = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    shots = [
        ShotSpec(**shot)
        for shot in data["shots"]
    ]

    return EpisodeSpec(
        episode_id=data["episode_id"],
        title=data["title"],
        description=data["description"],
        language=data.get(
            "language",
            "en"
        ),
        target_duration_seconds=data[
            "target_duration_seconds"
        ],
        shots=shots
    )


def main() -> None:

    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA real anime production "
            "orchestrator v11"
        )
    )

    parser.add_argument(
        "--episode",
        required=True,
        help="Path to an episode JSON file."
    )

    parser.add_argument(
        "--workflow",
        required=True,
        help="Path to the real ComfyUI/Wan workflow JSON."
    )

    args = parser.parse_args()

    episode = load_episode(
        Path(args.episode)
    )

    production = (
        AJVYRAAnimeProduction(
            workflow_template=Path(
                args.workflow
            )
        )
    )

    result = production.produce_episode(
        episode
    )

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        )
    )


if __name__ == "__main__":
    main()
