from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence


# ============================================================
# AJVYRA REAL VIDEO GENERATION ENGINE
# ============================================================
#
# File:
#   ajvyra_anime_real_video_generation_engine.py
#
# Purpose:
#   Convert AJVYRA ShotSpecs into real generated video files.
#
# Pipeline:
#
#   Shot Plan
#       ↓
#   Character References
#       ↓
#   Video Provider
#       ↓
#   Async Generation Operation
#       ↓
#   Poll
#       ↓
#   Download
#       ↓
#   Validate
#       ↓
#   Save
#       ↓
#   Render Queue
#
# Provider modes:
#
#   gemini
#   http
#   local
#   mock
#
# No API key is hard-coded.
#
# ============================================================


ENGINE_NAME = "AJVYRA Real Video Generation Engine"
ENGINE_VERSION = "1.0.0"

DEFAULT_OUTPUT_ROOT = Path(
    "generated/anime_production"
)

DEFAULT_MAX_RETRIES = 3

SUPPORTED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".webm",
    ".mkv",
}


# ============================================================
# GENERAL HELPERS
# ============================================================


def utc_timestamp() -> str:
    return time.strftime(
        "%Y-%m-%dT%H:%M:%SZ",
        time.gmtime(),
    )


def stable_hash(value: Any) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return hashlib.sha256(raw).hexdigest()


def safe_slug(value: str) -> str:
    result = []

    for char in str(value).lower():

        if char.isalnum():
            result.append(char)

        elif char in {" ", "-", "_"}:
            result.append("_")

    value = "".join(result).strip("_")

    return value or "unnamed"


def write_json(
    path: Path,
    data: Any,
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary = path.with_suffix(
        path.suffix + ".tmp"
    )

    with temporary.open(
        "w",
        encoding="utf-8",
    ) as handle:

        json.dump(
            data,
            handle,
            ensure_ascii=False,
            indent=2,
        )

    temporary.replace(path)


def read_json(
    path: Path,
    default: Any = None,
) -> Any:

    if not path.exists():
        return default

    try:

        with path.open(
            "r",
            encoding="utf-8",
        ) as handle:

            return json.load(handle)

    except (
        OSError,
        json.JSONDecodeError,
    ):

        return default


def sha256_file(
    path: Path,
) -> str:

    digest = hashlib.sha256()

    with path.open(
        "rb"
    ) as handle:

        while True:

            chunk = handle.read(
                1024 * 1024
            )

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


# ============================================================
# SHOT DATA
# ============================================================


@dataclass
class VideoShotSpec:

    anime_id: str
    episode_id: str
    scene_id: str
    shot_id: str

    duration_seconds: float

    prompt: str
    negative_prompt: str

    characters: List[str] = field(
        default_factory=list
    )

    reference_images: List[str] = field(
        default_factory=list
    )

    seed: Optional[int] = None

    aspect_ratio: str = "16:9"

    resolution: str = "720p"

    language: str = "ja"

    previous_video: Optional[str] = None

    first_frame: Optional[str] = None

    last_frame: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def normalized(self):

        return asdict(self)


@dataclass
class VideoGenerationResult:

    success: bool

    provider: str

    shot_id: str

    status: str

    output_path: Optional[str] = None

    operation_id: Optional[str] = None

    duration_seconds: Optional[float] = None

    error: Optional[str] = None

    attempts: int = 0

    raw: Dict[str, Any] = field(
        default_factory=dict
    )

    def normalized(self):

        return asdict(self)


# ============================================================
# PROVIDER INTERFACE
# ============================================================


class AJVYRAVideoProvider:

    name = "base"

    def generate(
        self,
        shot: VideoShotSpec,
        output_path: Path,
    ) -> VideoGenerationResult:

        raise NotImplementedError


# ============================================================
# GEMINI / VEO PROVIDER
# ============================================================


class AJVYRAVeoProvider(
    AJVYRAVideoProvider
):
    """
    Real Google Gemini / Veo adapter.

    Environment variables:

        GEMINI_API_KEY
        GOOGLE_API_KEY

        AJVYRA_VEO_MODEL
        AJVYRA_VEO_POLL_SECONDS
        AJVYRA_VEO_TIMEOUT

    Default model:

        veo-3.1-generate-preview
    """

    name = "veo"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        poll_seconds: Optional[int] = None,
        timeout_seconds: Optional[int] = None,
    ):

        self.api_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
        )

        self.model = (
            model
            or os.getenv(
                "AJVYRA_VEO_MODEL"
            )
            or "veo-3.1-generate-preview"
        )

        self.poll_seconds = int(
            poll_seconds
            or os.getenv(
                "AJVYRA_VEO_POLL_SECONDS",
                "10",
            )
        )

        self.timeout_seconds = int(
            timeout_seconds
            or os.getenv(
                "AJVYRA_VEO_TIMEOUT",
                "3600",
            )
        )

        self.client = None

    # --------------------------------------------------------
    # Client
    # --------------------------------------------------------

    def _load_client(self):

        if self.client is not None:
            return

        if not self.api_key:

            raise RuntimeError(
                "GEMINI_API_KEY or GOOGLE_API_KEY "
                "is not configured."
            )

        try:

            from google import genai

        except ImportError as exc:

            raise RuntimeError(
                "Google GenAI SDK is not installed. "
                "Install the current google-genai package."
            ) from exc

        self.client = genai.Client(
            api_key=self.api_key
        )

    # --------------------------------------------------------
    # Image loading
    # --------------------------------------------------------

    @staticmethod
    def _load_image(
        path: str,
    ):

        from PIL import Image

        file_path = Path(path)

        if not file_path.exists():

            raise FileNotFoundError(
                f"Reference image does not exist: "
                f"{file_path}"
            )

        return Image.open(
            file_path
        ).convert("RGB")

    # --------------------------------------------------------
    # Duration
    # --------------------------------------------------------

    @staticmethod
    def _normalize_duration(
        duration: float,
    ) -> str:

        allowed = [
            4,
            6,
            8,
        ]

        closest = min(
            allowed,
            key=lambda value:
                abs(value - duration),
        )

        return str(
            closest
        )

    # --------------------------------------------------------
    # Generate
    # --------------------------------------------------------

    def generate(
        self,
        shot: VideoShotSpec,
        output_path: Path,
    ) -> VideoGenerationResult:

        started = time.time()

        try:

            self._load_client()

            from google.genai import types

            duration = (
                self._normalize_duration(
                    shot.duration_seconds
                )
            )

            prompt = self._build_prompt(
                shot
            )

            config_kwargs = {
                "aspect_ratio": (
                    shot.aspect_ratio
                ),
                "duration_seconds": duration,
                "resolution": (
                    shot.resolution
                ),
            }

            # ------------------------------------------------
            # Reference images
            # ------------------------------------------------

            reference_images = []

            for path in (
                shot.reference_images[:3]
            ):

                image = self._load_image(
                    path
                )

                reference_images.append(
                    types.VideoGenerationReferenceImage(
                        image=image,
                        reference_type="asset",
                    )
                )

            if reference_images:

                config_kwargs[
                    "reference_images"
                ] = reference_images

            # ------------------------------------------------
            # First / last frame
            # ------------------------------------------------

            primary_image = None

            if shot.first_frame:

                primary_image = (
                    self._load_image(
                        shot.first_frame
                    )
                )

                if shot.last_frame:

                    config_kwargs[
                        "last_frame"
                    ] = self._load_image(
                        shot.last_frame
                    )

            # ------------------------------------------------
            # Seed
            # ------------------------------------------------

            if shot.seed is not None:

                config_kwargs[
                    "seed"
                ] = int(
                    shot.seed
                )

            config = (
                types.GenerateVideosConfig(
                    **config_kwargs
                )
            )

            # ------------------------------------------------
            # Real generation request
            # ------------------------------------------------

            if primary_image is not None:

                operation = (
                    self.client.models.generate_videos(
                        model=self.model,
                        prompt=prompt,
                        image=primary_image,
                        config=config,
                    )
                )

            else:

                operation = (
                    self.client.models.generate_videos(
                        model=self.model,
                        prompt=prompt,
                        config=config,
                    )
                )

            operation_id = self._operation_id(
                operation
            )

            # ------------------------------------------------
            # Poll
            # ------------------------------------------------

            operation = self._wait_for_operation(
                operation
            )

            # ------------------------------------------------
            # Download
            # ------------------------------------------------

            generated_videos = (
                getattr(
                    getattr(
                        operation,
                        "response",
                        None,
                    ),
                    "generated_videos",
                    None,
                )
            )

            if not generated_videos:

                raise RuntimeError(
                    "Veo operation completed but "
                    "returned no generated video."
                )

            video = (
                generated_videos[0]
            )

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self.client.files.download(
                file=video.video,
                destination=str(
                    output_path
                ),
            )

            if not output_path.exists():

                raise RuntimeError(
                    "Video download completed "
                    "without creating output file."
                )

            elapsed = (
                time.time()
                - started
            )

            return VideoGenerationResult(
                success=True,
                provider=self.name,
                shot_id=shot.shot_id,
                status="completed",
                output_path=str(
                    output_path
                ),
                operation_id=operation_id,
                duration_seconds=elapsed,
                attempts=1,
                raw={
                    "model": self.model,
                    "requested_duration": duration,
                    "resolution": (
                        shot.resolution
                    ),
                    "reference_count": len(
                        reference_images
                    ),
                },
            )

        except Exception as exc:

            return VideoGenerationResult(
                success=False,
                provider=self.name,
                shot_id=shot.shot_id,
                status="failed",
                error=str(exc),
                attempts=1,
            )

    # --------------------------------------------------------
    # Operation ID
    # --------------------------------------------------------

    @staticmethod
    def _operation_id(
        operation: Any,
    ) -> Optional[str]:

        for attribute in (
            "name",
            "operation_name",
            "id",
        ):

            value = getattr(
                operation,
                attribute,
                None,
            )

            if value:
                return str(
                    value
                )

        return None

    # --------------------------------------------------------
    # Poll
    # --------------------------------------------------------

    def _wait_for_operation(
        self,
        operation: Any,
    ):

        started = time.time()

        while True:

            done = bool(
                getattr(
                    operation,
                    "done",
                    False,
                )
            )

            if done:
                return operation

            elapsed = (
                time.time()
                - started
            )

            if (
                elapsed
                >= self.timeout_seconds
            ):

                raise TimeoutError(
                    "Veo generation operation "
                    "timed out."
                )

            time.sleep(
                self.poll_seconds
            )

            # Current Google GenAI SDK exposes
            # operation refresh/get methods.
            try:

                operation = (
                    self.client.operations.get(
                        operation
                    )
                )

            except Exception:

                # Some SDK versions expose a
                # video-operation-specific method.
                if hasattr(
                    self.client.operations,
                    "get_videos_operation",
                ):

                    operation = (
                        self.client
                        .operations
                        .get_videos_operation(
                            operation
                        )
                    )

                else:

                    raise

    # --------------------------------------------------------
    # Prompt
    # --------------------------------------------------------

    def _build_prompt(
        self,
        shot: VideoShotSpec,
    ) -> str:

        prompt = (
            shot.prompt.strip()
        )

        prompt += (
            "\n\nAJVYRA VIDEO DIRECTOR "
            "REQUIREMENTS:\n"
            "Maintain the identity and clothing "
            "of all referenced characters.\n"
            "Maintain scene geography between "
            "the beginning and ending of the shot.\n"
            "Respect the specified camera movement.\n"
            "Use natural body motion.\n"
            "Avoid sudden character redesign.\n"
            "Avoid unexplained object changes.\n"
            "Create coherent cinematic motion.\n"
        )

        if shot.negative_prompt:

            prompt += (
                "\nNEGATIVE CONSTRAINTS:\n"
                + shot.negative_prompt
            )

        return prompt


# ============================================================
# GENERIC HTTP PROVIDER
# ============================================================


class AJVYRAHTTPVideoProvider(
    AJVYRAVideoProvider
):
    """
    Connects AJVYRA to your own backend.

    Request:

        POST endpoint

    JSON:

        {
            "operation": "video_generation",
            "shot": {...}
        }

    Supported response patterns:

        {
            "status": "completed",
            "video_url": "...",
            "operation_id": "..."
        }

    or:

        {
            "status": "queued",
            "operation_id": "..."
        }

    The status endpoint is optional.
    """

    name = "ajvyra_http"

    def __init__(
        self,
        endpoint: str,
        api_key: str = "",
        status_endpoint: str = "",
        timeout: int = 600,
        poll_seconds: int = 10,
    ):

        self.endpoint = endpoint
        self.api_key = api_key
        self.status_endpoint = (
            status_endpoint
        )
        self.timeout = timeout
        self.poll_seconds = poll_seconds

    def _post(
        self,
        endpoint: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:

        body = json.dumps(
            payload,
            ensure_ascii=False,
        ).encode("utf-8")

        headers = {
            "Content-Type":
                "application/json",
        }

        if self.api_key:

            headers[
                "Authorization"
            ] = (
                f"Bearer {self.api_key}"
            )

        request = urllib.request.Request(
            endpoint,
            data=body,
            headers=headers,
            method="POST",
        )

        with urllib.request.urlopen(
            request,
            timeout=self.timeout,
        ) as response:

            raw = response.read().decode(
                "utf-8"
            )

        return json.loads(
            raw
        )

    def _get(
        self,
        endpoint: str,
    ) -> Dict[str, Any]:

        headers = {}

        if self.api_key:

            headers[
                "Authorization"
            ] = (
                f"Bearer {self.api_key}"
            )

        request = urllib.request.Request(
            endpoint,
            headers=headers,
            method="GET",
        )

        with urllib.request.urlopen(
            request,
            timeout=self.timeout,
        ) as response:

            raw = response.read().decode(
                "utf-8"
            )

        return json.loads(
            raw
        )

    def generate(
        self,
        shot: VideoShotSpec,
        output_path: Path,
    ) -> VideoGenerationResult:

        try:

            response = self._post(
                self.endpoint,
                {
                    "engine": ENGINE_NAME,
                    "operation":
                        "video_generation",
                    "shot":
                        shot.normalized(),
                },
            )

            operation_id = response.get(
                "operation_id"
            )

            status = str(
                response.get(
                    "status",
                    "queued",
                )
            ).lower()

            if status not in {
                "completed",
                "complete",
                "success",
            }:

                response = (
                    self._poll(
                        operation_id,
                        response,
                    )
                )

            video_url = response.get(
                "video_url"
            )

            if not video_url:

                raise RuntimeError(
                    "AJVYRA HTTP provider "
                    "returned no video_url."
                )

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self._download(
                video_url,
                output_path,
            )

            return VideoGenerationResult(
                success=True,
                provider=self.name,
                shot_id=shot.shot_id,
                status="completed",
                output_path=str(
                    output_path
                ),
                operation_id=operation_id,
                attempts=1,
                raw=response,
            )

        except Exception as exc:

            return VideoGenerationResult(
                success=False,
                provider=self.name,
                shot_id=shot.shot_id,
                status="failed",
                error=str(exc),
                attempts=1,
            )

    def _poll(
        self,
        operation_id: Optional[str],
        initial: Dict[str, Any],
    ) -> Dict[str, Any]:

        if (
            not operation_id
            or not self.status_endpoint
        ):

            raise RuntimeError(
                "Provider operation is incomplete "
                "but no status endpoint was configured."
            )

        started = time.time()

        while True:

            if (
                time.time() - started
                > self.timeout
            ):

                raise TimeoutError(
                    "AJVYRA HTTP video operation timed out."
                )

            endpoint = (
                self.status_endpoint
                .rstrip("/")
                + "/"
                + str(operation_id)
            )

            response = self._get(
                endpoint
            )

            status = str(
                response.get(
                    "status",
                    "",
                )
            ).lower()

            if status in {
                "completed",
                "complete",
                "success",
                "failed",
                "error",
            }:

                if status in {
                    "failed",
                    "error",
                }:

                    raise RuntimeError(
                        response.get(
                            "error",
                            "Provider failed.",
                        )
                    )

                return response

            time.sleep(
                self.poll_seconds
            )

    def _download(
        self,
        url: str,
        destination: Path,
    ) -> None:

        request = urllib.request.Request(
            url,
            method="GET",
        )

        with urllib.request.urlopen(
            request,
            timeout=self.timeout,
        ) as response:

            with destination.open(
                "wb"
            ) as output:

                while True:

                    chunk = response.read(
                        1024 * 1024
                    )

                    if not chunk:
                        break

                    output.write(
                        chunk
                    )


# ============================================================
# MOCK PROVIDER
# ============================================================


class AJVYRAMockVideoProvider(
    AJVYRAVideoProvider
):
    """
    Development provider.

    It DOES NOT generate fake video data.

    Instead it creates a job description and returns
    success=False so production code cannot accidentally
    mistake a mock run for a real video.
    """

    name = "mock"

    def generate(
        self,
        shot: VideoShotSpec,
        output_path: Path,
    ) -> VideoGenerationResult:

        return VideoGenerationResult(
            success=False,
            provider=self.name,
            shot_id=shot.shot_id,
            status="mock_only",
            error=(
                "Mock mode does not create video. "
                "Configure a real video provider."
            ),
        )


# ============================================================
# PROVIDER ROUTER
# ============================================================


class AJVYRAVideoProviderRouter:

    def __init__(
        self,
        mode: Optional[str] = None,
    ):

        self.mode = (
            mode
            or os.getenv(
                "AJVYRA_VIDEO_PROVIDER",
                "gemini",
            )
        ).lower()

        self._provider = None

    def get_provider(
        self,
    ) -> AJVYRAVideoProvider:

        if self._provider is not None:
            return self._provider

        if self.mode == "gemini":

            self._provider = (
                AJVYRAVeoProvider()
            )

        elif self.mode == "http":

            endpoint = os.getenv(
                "AJVYRA_VIDEO_ENDPOINT",
                "",
            )

            if not endpoint:

                raise RuntimeError(
                    "AJVYRA_VIDEO_ENDPOINT "
                    "is required."
                )

            self._provider = (
                AJVYRAHTTPVideoProvider(
                    endpoint=endpoint,
                    api_key=os.getenv(
                        "AJVYRA_VIDEO_API_KEY",
                        "",
                    ),
                    status_endpoint=os.getenv(
                        "AJVYRA_VIDEO_STATUS_ENDPOINT",
                        "",
                    ),
                )
            )

        elif self.mode == "mock":

            self._provider = (
                AJVYRAMockVideoProvider()
            )

        elif self.mode == "auto":

            endpoint = os.getenv(
                "AJVYRA_VIDEO_ENDPOINT",
                "",
            )

            if endpoint:

                self._provider = (
                    AJVYRAHTTPVideoProvider(
                        endpoint=endpoint,
                        api_key=os.getenv(
                            "AJVYRA_VIDEO_API_KEY",
                            "",
                        ),
                        status_endpoint=os.getenv(
                            "AJVYRA_VIDEO_STATUS_ENDPOINT",
                            "",
                        ),
                    )
                )

            elif (
                os.getenv("GEMINI_API_KEY")
                or os.getenv("GOOGLE_API_KEY")
            ):

                self._provider = (
                    AJVYRAVeoProvider()
                )

            else:

                self._provider = (
                    AJVYRAMockVideoProvider()
                )

        else:

            raise ValueError(
                f"Unsupported provider: {self.mode}"
            )

        return self._provider


# ============================================================
# SHOT VALIDATOR
# ============================================================


class AJVYRAShotValidator:

    def validate(
        self,
        shot: VideoShotSpec,
    ) -> Dict[str, Any]:

        errors = []
        warnings = []

        if not shot.anime_id:
            errors.append(
                "anime_id is empty"
            )

        if not shot.episode_id:
            errors.append(
                "episode_id is empty"
            )

        if not shot.shot_id:
            errors.append(
                "shot_id is empty"
            )

        if not shot.prompt:
            errors.append(
                "prompt is empty"
            )

        if shot.duration_seconds <= 0:
            errors.append(
                "duration must be positive"
            )

        if shot.duration_seconds > 8:
            warnings.append(
                "Provider may normalize this shot "
                "to its supported duration."
            )

        if (
            shot.aspect_ratio
            not in {
                "16:9",
                "9:16",
            }
        ):

            errors.append(
                "Unsupported aspect ratio."
            )

        for path in (
            shot.reference_images
        ):

            if not Path(path).exists():

                errors.append(
                    f"Missing reference: {path}"
                )

        if shot.first_frame:

            if not Path(
                shot.first_frame
            ).exists():

                errors.append(
                    "First frame does not exist."
                )

        if shot.last_frame:

            if not Path(
                shot.last_frame
            ).exists():

                errors.append(
                    "Last frame does not exist."
                )

        return {
            "passed": not errors,
            "errors": errors,
            "warnings": warnings,
        }


# ============================================================
# VIDEO FILE VALIDATOR
# ============================================================


class AJVYRAVideoFileValidator:

    def validate(
        self,
        path: Path,
    ) -> Dict[str, Any]:

        if not path.exists():

            return {
                "passed": False,
                "error": "Video file does not exist.",
            }

        if path.stat().st_size <= 0:

            return {
                "passed": False,
                "error": "Video file is empty.",
            }

        if (
            path.suffix.lower()
            not in SUPPORTED_VIDEO_EXTENSIONS
        ):

            return {
                "passed": False,
                "error": (
                    f"Unsupported video extension: "
                    f"{path.suffix}"
                ),
            }

        checksum = sha256_file(
            path
        )

        duration = (
            self._probe_duration(path)
        )

        return {
            "passed": True,
            "path": str(path),
            "size_bytes": path.stat().st_size,
            "sha256": checksum,
            "duration_seconds": duration,
        }

    @staticmethod
    def _probe_duration(
        path: Path,
    ) -> Optional[float]:

        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ]

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

            if result.returncode != 0:
                return None

            return float(
                result.stdout.strip()
            )

        except (
            OSError,
            ValueError,
            subprocess.SubprocessError,
        ):

            return None


# ============================================================
# SHOT GENERATION ENGINE
# ============================================================


class AJVYRARealVideoGenerationEngine:

    def __init__(
        self,
        provider: Optional[
            AJVYRAVideoProvider
        ] = None,
        output_root: str | Path = (
            DEFAULT_OUTPUT_ROOT
        ),
        max_retries: int = DEFAULT_MAX_RETRIES,
    ):

        self.provider = (
            provider
            or AJVYRAVideoProviderRouter()
            .get_provider()
        )

        self.output_root = Path(
            output_root
        )

        self.max_retries = max(
            1,
            int(max_retries),
        )

        self.shot_validator = (
            AJVYRAShotValidator()
        )

        self.video_validator = (
            AJVYRAVideoFileValidator()
        )

    # --------------------------------------------------------
    # Output path
    # --------------------------------------------------------

    def output_path(
        self,
        shot: VideoShotSpec,
    ) -> Path:

        directory = (
            self.output_root
            / safe_slug(shot.anime_id)
            / "season_01"
            / safe_slug(shot.episode_id)
            / "media"
            / "video"
        )

        return (
            directory
            / f"{safe_slug(shot.shot_id)}.mp4"
        )

    # --------------------------------------------------------
    # Job manifest
    # --------------------------------------------------------

    def job_manifest_path(
        self,
        shot: VideoShotSpec,
    ) -> Path:

        directory = (
            self.output_root
            / safe_slug(shot.anime_id)
            / "season_01"
            / safe_slug(shot.episode_id)
            / "jobs"
        )

        return (
            directory
            / f"{safe_slug(shot.shot_id)}.json"
        )

    # --------------------------------------------------------
    # Generate one shot
    # --------------------------------------------------------

    def generate_shot(
        self,
        shot: VideoShotSpec,
    ) -> VideoGenerationResult:

        validation = (
            self.shot_validator.validate(
                shot
            )
        )

        manifest_path = (
            self.job_manifest_path(
                shot
            )
        )

        manifest = {
            "engine": ENGINE_NAME,
            "version": ENGINE_VERSION,
            "created_at": utc_timestamp(),
            "shot": shot.normalized(),
            "provider": self.provider.name,
            "validation": validation,
            "status": "queued",
        }

        write_json(
            manifest_path,
            manifest,
        )

        if not validation["passed"]:

            result = VideoGenerationResult(
                success=False,
                provider=self.provider.name,
                shot_id=shot.shot_id,
                status="invalid",
                error=json.dumps(
                    validation,
                    ensure_ascii=False,
                ),
            )

            manifest[
                "status"
            ] = "invalid"

            manifest[
                "result"
            ] = result.normalized()

            write_json(
                manifest_path,
                manifest,
            )

            return result

        output_path = (
            self.output_path(
                shot
            )
        )

        # ----------------------------------------------------
        # Resume support
        # ----------------------------------------------------

        if output_path.exists():

            existing = (
                self.video_validator.validate(
                    output_path
                )
            )

            if existing["passed"]:

                result = VideoGenerationResult(
                    success=True,
                    provider=self.provider.name,
                    shot_id=shot.shot_id,
                    status="already_exists",
                    output_path=str(
                        output_path
                    ),
                    attempts=0,
                    raw={
                        "validation":
                            existing,
                    },
                )

                manifest[
                    "status"
                ] = "already_exists"

                manifest[
                    "result"
                ] = result.normalized()

                write_json(
                    manifest_path,
                    manifest,
                )

                return result

        # ----------------------------------------------------
        # Retry loop
        # ----------------------------------------------------

        last_result = None

        for attempt in range(
            1,
            self.max_retries + 1,
        ):

            result = self.provider.generate(
                shot=shot,
                output_path=output_path,
            )

            result.attempts = attempt

            if result.success:

                file_validation = (
                    self.video_validator.validate(
                        output_path
                    )
                )

                if not file_validation[
                    "passed"
                ]:

                    result.success = False
                    result.status = (
                        "invalid_output"
                    )
                    result.error = json.dumps(
                        file_validation,
                        ensure_ascii=False,
                    )

                else:

                    result.raw[
                        "file_validation"
                    ] = file_validation

                    last_result = result

                    break

            last_result = result

            if attempt < self.max_retries:

                time.sleep(
                    min(
                        30,
                        2 ** attempt,
                    )
                )

        if last_result is None:

            last_result = VideoGenerationResult(
                success=False,
                provider=self.provider.name,
                shot_id=shot.shot_id,
                status="failed",
                error="Unknown generation failure.",
            )

        # ----------------------------------------------------
        # Save manifest
        # ----------------------------------------------------

        manifest[
            "status"
        ] = last_result.status

        manifest[
            "result"
        ] = last_result.normalized()

        manifest[
            "completed_at"
        ] = utc_timestamp()

        write_json(
            manifest_path,
            manifest,
        )

        return last_result

    # --------------------------------------------------------
    # Generate episode
    # --------------------------------------------------------

    def generate_episode(
        self,
        shots: Sequence[
            VideoShotSpec
        ],
    ) -> Dict[str, Any]:

        results = []

        started = time.time()

        for shot in shots:

            result = self.generate_shot(
                shot
            )

            results.append(
                result.normalized()
            )

        elapsed = (
            time.time()
            - started
        )

        successful = sum(
            1
            for result in results
            if result["success"]
        )

        failed = (
            len(results)
            - successful
        )

        return {
            "engine": ENGINE_NAME,
            "version": ENGINE_VERSION,
            "provider": self.provider.name,
            "created_at": utc_timestamp(),
            "shot_count": len(results),
            "successful": successful,
            "failed": failed,
            "elapsed_seconds": round(
                elapsed,
                2,
            ),
            "results": results,
        }


# ============================================================
# SHOT PLAN LOADER
# ============================================================


class AJVYRAShotPlanLoader:

    def load(
        self,
        path: str | Path,
    ) -> List[VideoShotSpec]:

        data = read_json(
            Path(path),
            {},
        )

        shots = []

        for scene in data.get(
            "scenes",
            [],
        ):

            for shot in scene.get(
                "shots",
                [],
            ):

                camera = shot.get(
                    "camera",
                    {}
                )

                lighting = shot.get(
                    "lighting",
                    {}
                )

                prompt = shot.get(
                    "visual_prompt",
                    ""
                )

                # Camera and lighting information
                # become part of the final video prompt.
                prompt += (
                    "\nCamera details: "
                    + json.dumps(
                        camera,
                        ensure_ascii=False,
                    )
                )

                prompt += (
                    "\nLighting details: "
                    + json.dumps(
                        lighting,
                        ensure_ascii=False,
                    )
                )

                shot_spec = VideoShotSpec(
                    anime_id=data[
                        "anime_id"
                    ],
                    episode_id=data[
                        "episode_id"
                    ],
                    scene_id=shot[
                        "scene_id"
                    ],
                    shot_id=shot[
                        "shot_id"
                    ],
                    duration_seconds=float(
                        shot.get(
                            "duration_seconds",
                            8,
                        )
                    ),
                    prompt=prompt,
                    negative_prompt=shot.get(
                        "negative_prompt",
                        "",
                    ),
                    characters=shot.get(
                        "characters",
                        [],
                    ),
                    reference_images=shot.get(
                        "reference_images",
                        [],
                    ),
                    seed=shot.get(
                        "continuity_seed"
                    ),
                    aspect_ratio="16:9",
                    resolution="720p",
                    metadata={
                        "action": shot.get(
                            "action",
                            "",
                        ),
                        "emotion": shot.get(
                            "emotion",
                            "",
                        ),
                        "camera": camera,
                        "lighting": lighting,
                    },
                )

                shots.append(
                    shot_spec
                )

        return shots


# ============================================================
# EPISODE PRODUCTION COMMANDER
# ============================================================


class AJVYRAEpisodeVideoProductionCommander:

    def __init__(
        self,
        engine: Optional[
            AJVYRARealVideoGenerationEngine
        ] = None,
    ):

        self.engine = (
            engine
            or AJVYRARealVideoGenerationEngine()
        )

        self.loader = (
            AJVYRAShotPlanLoader()
        )

    def produce_from_plan(
        self,
        plan_path: str | Path,
    ) -> Dict[str, Any]:

        shots = self.loader.load(
            plan_path
        )

        report = (
            self.engine.generate_episode(
                shots
            )
        )

        report_path = (
            Path(plan_path).parent
            / "video_generation_report.json"
        )

        write_json(
            report_path,
            report,
        )

        return report


# ============================================================
# FFMPEG ASSEMBLY
# ============================================================


class AJVYRAEpisodeAssembler:

    """
    Takes generated shot videos and prepares a final episode.

    FFmpeg is intentionally used only as the media assembler.
    The creative decisions remain inside AJVYRA.
    """

    def __init__(
        self,
        ffmpeg_binary: str = "ffmpeg",
    ):

        self.ffmpeg = (
            ffmpeg_binary
        )

    def check_available(self) -> bool:

        try:

            result = subprocess.run(
                [
                    self.ffmpeg,
                    "-version",
                ],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )

            return (
                result.returncode == 0
            )

        except (
            OSError,
            subprocess.SubprocessError,
        ):

            return False

    def create_concat_file(
        self,
        videos: Sequence[
            str | Path
        ],
        output_txt: str | Path,
    ) -> Path:

        output_txt = Path(
            output_txt
        )

        output_txt.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        lines = []

        for video in videos:

            path = Path(
                video
            ).resolve()

            escaped = (
                str(path)
                .replace(
                    "'",
                    "'\\''",
                )
            )

            lines.append(
                f"file '{escaped}'"
            )

        output_txt.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        return output_txt

    def assemble(
        self,
        videos: Sequence[
            str | Path
        ],
        output_path: str | Path,
    ) -> Dict[str, Any]:

        output_path = Path(
            output_path
        )

        if not videos:

            return {
                "success": False,
                "error": (
                    "No video files supplied."
                ),
            }

        if not self.check_available():

            return {
                "success": False,
                "error": (
                    "FFmpeg is not installed "
                    "or is not available on PATH."
                ),
            }

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        concat_file = (
            output_path.parent
            / "concat_list.txt"
        )

        self.create_concat_file(
            videos,
            concat_file,
        )

        command = [
            self.ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(output_path),
        ]

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=3600,
                check=False,
            )

        except (
            OSError,
            subprocess.SubprocessError,
        ) as exc:

            return {
                "success": False,
                "error": str(exc),
            }

        if result.returncode != 0:

            return {
                "success": False,
                "error": (
                    result.stderr[-5000:]
                ),
            }

        return {
            "success": True,
            "output_path": str(
                output_path
            ),
            "video_count": len(
                videos
            ),
        }


# ============================================================
# DEMO SHOT
# ============================================================


def build_demo_shot() -> VideoShotSpec:

    return VideoShotSpec(
        anime_id="Veylora",
        episode_id="episode_01",
        scene_id="scene_001",
        shot_id="scene_001_shot_001",

        duration_seconds=8,

        prompt=(
            "Cinematic original anime scene. "
            "A quiet silver-haired teenage boy "
            "stands alone at a rainy city train station "
            "in the evening. "
            "He slowly raises his eyes toward the "
            "distant platform. "
            "Rain falls naturally around him. "
            "His expression is controlled sadness. "
            "The camera slowly pushes toward his face. "
            "Wet pavement reflects distant city lights. "
            "Subtle wind moves his hair and jacket."
        ),

        negative_prompt=(
            "different face, different hairstyle, "
            "different clothing, different eye color, "
            "extra fingers, extra limbs, "
            "deformed anatomy, duplicated character, "
            "text, watermark, logo, "
            "unstable background"
        ),

        characters=[
            "veylora_main_01",
        ],

        reference_images=[],

        seed=18273645,

        aspect_ratio="16:9",

        resolution="720p",

        language="ja",

        metadata={
            "test": True,
            "purpose": (
                "AJVYRA real video pipeline test"
            ),
        },
    )


# ============================================================
# CLI
# ============================================================


def main() -> None:

    import argparse

    parser = argparse.ArgumentParser(
        description=ENGINE_NAME
    )

    parser.add_argument(
        "--provider",
        choices=[
            "gemini",
            "http",
            "mock",
            "auto",
        ],
        default=None,
    )

    parser.add_argument(
        "--plan",
        type=str,
        default="",
    )

    parser.add_argument(
        "--demo",
        action="store_true",
    )

    parser.add_argument(
        "--assemble",
        action="store_true",
    )

    parser.add_argument(
        "--videos",
        nargs="*",
        default=[],
    )

    parser.add_argument(
        "--output",
        default=(
            "generated/"
            "anime_production/"
            "assembled_episode.mp4"
        ),
    )

    args = parser.parse_args()

    provider = None

    if args.provider:

        provider = (
            AJVYRAVideoProviderRouter(
                args.provider
            ).get_provider()
        )

    engine = (
        AJVYRARealVideoGenerationEngine(
            provider=provider
        )
    )

    if args.demo:

        shot = build_demo_shot()

        result = (
            engine.generate_shot(
                shot
            )
        )

        print(
            json.dumps(
                result.normalized(),
                ensure_ascii=False,
                indent=2,
            )
        )

    if args.plan:

        commander = (
            AJVYRAEpisodeVideoProductionCommander(
                engine=engine
            )
        )

        report = (
            commander.produce_from_plan(
                args.plan
            )
        )

        print(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            )
        )

    if args.assemble:

        assembler = (
            AJVYRAEpisodeAssembler()
        )

        report = assembler.assemble(
            videos=args.videos,
            output_path=args.output,
        )

        print(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
