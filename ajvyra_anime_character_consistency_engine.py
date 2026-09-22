from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


# ============================================================
# AJVYRA ANIME CHARACTER CONSISTENCY ENGINE
# ============================================================
#
# Purpose
# -------
# Keeps an anime character visually consistent across hundreds
# of generated shots.
#
# This is NOT a fake image generator.
#
# It provides:
#   - Character identity records
#   - Reference image management
#   - Identity fingerprints
#   - Prompt locking
#   - Negative prompt locking
#   - Outfit locking
#   - Expression variants
#   - Camera-aware prompt construction
#   - Seed management
#   - Local image-provider adapter
#   - HTTP image-provider adapter
#   - Gemini-compatible image adapter
#   - Optional Diffusers/IP-Adapter backend
#   - Character consistency validation
#   - Shot reference manifests
#   - Persistent JSON state
#
# No API key is hard-coded.
#
# ============================================================


ENGINE_NAME = "AJVYRA Character Consistency Engine"
ENGINE_VERSION = "1.0.0"


SUPPORTED_IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
}


DEFAULT_NEGATIVE_PROMPT = (
    "different character, different face, different hairstyle, "
    "different eye color, different clothing, different age, "
    "deformed face, bad anatomy, extra fingers, missing fingers, "
    "extra limbs, duplicate person, distorted eyes, asymmetrical eyes, "
    "blurry face, low quality, watermark, text, logo"
)


# ============================================================
# Helpers
# ============================================================


def utc_timestamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def stable_hash(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return hashlib.sha256(payload).hexdigest()


def safe_slug(value: str) -> str:
    result = []

    for char in value.lower():
        if char.isalnum():
            result.append(char)
        elif char in {" ", "-", "_"}:
            result.append("_")

    slug = "".join(result).strip("_")

    return slug or "unnamed"


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def unique_list(values: Sequence[str]) -> List[str]:
    result = []
    seen = set()

    for value in values:
        value = str(value).strip()

        if not value:
            continue

        if value not in seen:
            seen.add(value)
            result.append(value)

    return result


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default

    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary = path.with_suffix(path.suffix + ".tmp")

    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(
            data,
            handle,
            ensure_ascii=False,
            indent=2,
        )

    temporary.replace(path)


def copy_if_exists(source: Path, destination: Path) -> bool:
    if not source.exists():
        return False

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)

    return True


# ============================================================
# Data Models
# ============================================================


@dataclass
class CharacterAppearance:
    age_range: str = "young adult"
    height: str = "average"
    body_type: str = "slim"
    skin_tone: str = ""
    face_shape: str = ""
    eye_color: str = ""
    eye_shape: str = ""
    eyebrow_shape: str = ""
    hair_color: str = ""
    hair_style: str = ""
    hair_length: str = ""
    distinguishing_features: List[str] = field(default_factory=list)

    def normalized(self) -> Dict[str, Any]:
        return {
            "age_range": self.age_range,
            "height": self.height,
            "body_type": self.body_type,
            "skin_tone": self.skin_tone,
            "face_shape": self.face_shape,
            "eye_color": self.eye_color,
            "eye_shape": self.eye_shape,
            "eyebrow_shape": self.eyebrow_shape,
            "hair_color": self.hair_color,
            "hair_style": self.hair_style,
            "hair_length": self.hair_length,
            "distinguishing_features": unique_list(
                self.distinguishing_features
            ),
        }


@dataclass
class CharacterOutfit:
    outfit_id: str
    name: str
    description: str
    colors: List[str] = field(default_factory=list)
    accessories: List[str] = field(default_factory=list)
    footwear: str = ""
    season: str = "default"
    locked: bool = True

    def normalized(self) -> Dict[str, Any]:
        return {
            "outfit_id": self.outfit_id,
            "name": self.name,
            "description": self.description,
            "colors": unique_list(self.colors),
            "accessories": unique_list(self.accessories),
            "footwear": self.footwear,
            "season": self.season,
            "locked": self.locked,
        }


@dataclass
class CharacterPersonality:
    personality_traits: List[str] = field(default_factory=list)
    emotional_range: List[str] = field(default_factory=list)
    default_expression: str = "neutral"
    speech_style: str = ""
    mannerisms: List[str] = field(default_factory=list)

    def normalized(self) -> Dict[str, Any]:
        return {
            "personality_traits": unique_list(self.personality_traits),
            "emotional_range": unique_list(self.emotional_range),
            "default_expression": self.default_expression,
            "speech_style": self.speech_style,
            "mannerisms": unique_list(self.mannerisms),
        }


@dataclass
class CharacterReference:
    reference_id: str
    path: str
    reference_type: str
    view: str = "front"
    priority: float = 1.0
    notes: str = ""

    def normalized(self) -> Dict[str, Any]:
        return {
            "reference_id": self.reference_id,
            "path": self.path,
            "reference_type": self.reference_type,
            "view": self.view,
            "priority": clamp(float(self.priority), 0.0, 1.0),
            "notes": self.notes,
        }


@dataclass
class CharacterIdentity:
    character_id: str
    name: str
    anime_id: str

    appearance: CharacterAppearance
    personality: CharacterPersonality

    outfits: List[CharacterOutfit] = field(default_factory=list)
    references: List[CharacterReference] = field(default_factory=list)

    visual_style: str = (
        "cinematic anime, high-detail character illustration, "
        "consistent facial identity"
    )

    canonical_expression: str = "neutral"
    identity_strength: float = 0.85
    style_strength: float = 0.65

    voice_identity_id: str = ""

    locked: bool = True

    created_at: str = field(default_factory=utc_timestamp)
    updated_at: str = field(default_factory=utc_timestamp)

    identity_hash: str = ""

    def rebuild_hash(self) -> str:
        payload = {
            "character_id": self.character_id,
            "name": self.name,
            "anime_id": self.anime_id,
            "appearance": self.appearance.normalized(),
            "personality": self.personality.normalized(),
            "outfits": [
                outfit.normalized()
                for outfit in self.outfits
            ],
            "visual_style": self.visual_style,
            "canonical_expression": self.canonical_expression,
        }

        self.identity_hash = stable_hash(payload)[:32]
        self.updated_at = utc_timestamp()

        return self.identity_hash

    def normalized(self) -> Dict[str, Any]:
        if not self.identity_hash:
            self.rebuild_hash()

        return {
            "character_id": self.character_id,
            "name": self.name,
            "anime_id": self.anime_id,
            "appearance": self.appearance.normalized(),
            "personality": self.personality.normalized(),
            "outfits": [
                outfit.normalized()
                for outfit in self.outfits
            ],
            "references": [
                reference.normalized()
                for reference in self.references
            ],
            "visual_style": self.visual_style,
            "canonical_expression": self.canonical_expression,
            "identity_strength": self.identity_strength,
            "style_strength": self.style_strength,
            "voice_identity_id": self.voice_identity_id,
            "locked": self.locked,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "identity_hash": self.identity_hash,
        }


@dataclass
class ShotCharacterRequest:
    character_id: str
    expression: str = ""
    emotion: str = ""
    action: str = ""
    outfit_id: str = ""
    pose: str = ""
    camera_angle: str = "medium shot"
    lighting: str = "cinematic"
    environment: str = ""
    additional_prompt: str = ""


@dataclass
class CharacterPromptPackage:
    character_id: str
    positive_prompt: str
    negative_prompt: str

    reference_paths: List[str]

    identity_strength: float
    style_strength: float

    seed: int

    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> Dict[str, Any]:
        return {
            "character_id": self.character_id,
            "positive_prompt": self.positive_prompt,
            "negative_prompt": self.negative_prompt,
            "reference_paths": self.reference_paths,
            "identity_strength": self.identity_strength,
            "style_strength": self.style_strength,
            "seed": self.seed,
            "metadata": self.metadata,
        }


# ============================================================
# Character Registry
# ============================================================


class AJVYRACharacterRegistry:
    """
    Persistent source of truth for character identities.
    """

    def __init__(self, root: str | Path = "generated/anime_characters"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

        self.registry_path = self.root / "character_registry.json"

        self.characters: Dict[str, CharacterIdentity] = {}

        self._load()

    # --------------------------------------------------------
    # Persistence
    # --------------------------------------------------------

    def _load(self) -> None:
        data = read_json(
            self.registry_path,
            {
                "engine": ENGINE_NAME,
                "version": ENGINE_VERSION,
                "characters": {},
            },
        )

        for character_id, payload in data.get(
            "characters",
            {}
        ).items():

            appearance = CharacterAppearance(
                **payload.get("appearance", {})
            )

            personality = CharacterPersonality(
                **payload.get("personality", {})
            )

            outfits = [
                CharacterOutfit(**item)
                for item in payload.get("outfits", [])
            ]

            references = [
                CharacterReference(**item)
                for item in payload.get("references", [])
            ]

            character = CharacterIdentity(
                character_id=payload["character_id"],
                name=payload["name"],
                anime_id=payload["anime_id"],
                appearance=appearance,
                personality=personality,
                outfits=outfits,
                references=references,
                visual_style=payload.get(
                    "visual_style",
                    "cinematic anime",
                ),
                canonical_expression=payload.get(
                    "canonical_expression",
                    "neutral",
                ),
                identity_strength=float(
                    payload.get("identity_strength", 0.85)
                ),
                style_strength=float(
                    payload.get("style_strength", 0.65)
                ),
                voice_identity_id=payload.get(
                    "voice_identity_id",
                    "",
                ),
                locked=bool(
                    payload.get("locked", True)
                ),
                created_at=payload.get(
                    "created_at",
                    utc_timestamp(),
                ),
                updated_at=payload.get(
                    "updated_at",
                    utc_timestamp(),
                ),
                identity_hash=payload.get(
                    "identity_hash",
                    "",
                ),
            )

            self.characters[character_id] = character

    def save(self) -> None:
        payload = {
            "engine": ENGINE_NAME,
            "version": ENGINE_VERSION,
            "updated_at": utc_timestamp(),
            "characters": {
                character_id: character.normalized()
                for character_id, character
                in self.characters.items()
            },
        }

        write_json(
            self.registry_path,
            payload,
        )

    # --------------------------------------------------------
    # Character operations
    # --------------------------------------------------------

    def register(
        self,
        character: CharacterIdentity,
        overwrite: bool = False,
    ) -> CharacterIdentity:

        if (
            character.character_id in self.characters
            and not overwrite
        ):
            raise ValueError(
                f"Character already exists: "
                f"{character.character_id}"
            )

        character.rebuild_hash()

        self.characters[
            character.character_id
        ] = character

        self.save()

        self._create_character_directory(
            character
        )

        return character

    def get(
        self,
        character_id: str,
    ) -> CharacterIdentity:

        try:
            return self.characters[character_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown AJVYRA character: {character_id}"
            ) from exc

    def exists(
        self,
        character_id: str,
    ) -> bool:

        return character_id in self.characters

    def update(
        self,
        character_id: str,
        **changes: Any,
    ) -> CharacterIdentity:

        character = self.get(character_id)

        if character.locked:
            raise PermissionError(
                "Character identity is locked. "
                "Unlock it before changing canonical data."
            )

        for key, value in changes.items():

            if hasattr(character, key):
                setattr(character, key, value)

        character.rebuild_hash()

        self.save()

        return character

    def lock(
        self,
        character_id: str,
    ) -> None:

        character = self.get(character_id)

        character.locked = True
        character.rebuild_hash()

        self.save()

    def unlock(
        self,
        character_id: str,
    ) -> None:

        character = self.get(character_id)

        character.locked = False
        character.updated_at = utc_timestamp()

        self.save()

    # --------------------------------------------------------
    # References
    # --------------------------------------------------------

    def add_reference(
        self,
        character_id: str,
        source_path: str | Path,
        reference_type: str = "character_sheet",
        view: str = "front",
        priority: float = 1.0,
        notes: str = "",
    ) -> CharacterReference:

        character = self.get(character_id)

        source = Path(source_path)

        if not source.exists():
            raise FileNotFoundError(
                f"Reference image does not exist: {source}"
            )

        if source.suffix.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
            raise ValueError(
                f"Unsupported reference image: {source.suffix}"
            )

        destination_directory = (
            self.root
            / safe_slug(character.anime_id)
            / safe_slug(character.character_id)
            / "references"
        )

        destination_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        reference_id = (
            f"{character.character_id}_"
            f"{uuid.uuid4().hex[:10]}"
        )

        destination = (
            destination_directory
            / f"{reference_id}{source.suffix.lower()}"
        )

        shutil.copy2(
            source,
            destination,
        )

        reference = CharacterReference(
            reference_id=reference_id,
            path=str(destination),
            reference_type=reference_type,
            view=view,
            priority=priority,
            notes=notes,
        )

        character.references.append(reference)
        character.rebuild_hash()

        self.save()

        return reference

    def get_reference_images(
        self,
        character_id: str,
        reference_type: Optional[str] = None,
    ) -> List[Path]:

        character = self.get(character_id)

        results = []

        for reference in character.references:

            if (
                reference_type
                and reference.reference_type != reference_type
            ):
                continue

            path = Path(reference.path)

            if path.exists():
                results.append(path)

        return results

    # --------------------------------------------------------
    # Outfit operations
    # --------------------------------------------------------

    def add_outfit(
        self,
        character_id: str,
        outfit: CharacterOutfit,
    ) -> None:

        character = self.get(character_id)

        if character.locked:
            raise PermissionError(
                "Character identity is locked."
            )

        character.outfits.append(outfit)

        character.rebuild_hash()

        self.save()

    def get_outfit(
        self,
        character_id: str,
        outfit_id: str,
    ) -> CharacterOutfit:

        character = self.get(character_id)

        for outfit in character.outfits:

            if outfit.outfit_id == outfit_id:
                return outfit

        raise KeyError(
            f"Unknown outfit '{outfit_id}' "
            f"for character '{character_id}'"
        )

    # --------------------------------------------------------
    # Internal
    # --------------------------------------------------------

    def _create_character_directory(
        self,
        character: CharacterIdentity,
    ) -> Path:

        path = (
            self.root
            / safe_slug(character.anime_id)
            / safe_slug(character.character_id)
        )

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        write_json(
            path / "character_identity.json",
            character.normalized(),
        )

        return path


# ============================================================
# Seed Manager
# ============================================================


class AJVYRACharacterSeedManager:
    """
    Deterministic seed generation.

    A character + shot + episode combination gets a stable seed
    unless the caller explicitly overrides it.
    """

    def __init__(
        self,
        namespace: str = "AJVYRA",
    ):
        self.namespace = namespace

    def make_seed(
        self,
        character_id: str,
        episode_id: str,
        shot_id: str,
        variation: int = 0,
    ) -> int:

        raw = (
            f"{self.namespace}|"
            f"{character_id}|"
            f"{episode_id}|"
            f"{shot_id}|"
            f"{variation}"
        )

        digest = hashlib.sha256(
            raw.encode("utf-8")
        ).digest()

        return int.from_bytes(
            digest[:4],
            "big",
        )

    def make_character_master_seed(
        self,
        character_id: str,
    ) -> int:

        return self.make_seed(
            character_id,
            "MASTER",
            "MASTER",
        )


# ============================================================
# Prompt Lock
# ============================================================


class AJVYRACharacterPromptBuilder:
    """
    Converts canonical character data into a repeatable prompt.
    """

    def __init__(
        self,
        registry: AJVYRACharacterRegistry,
        seed_manager: Optional[
            AJVYRACharacterSeedManager
        ] = None,
    ):
        self.registry = registry

        self.seed_manager = (
            seed_manager
            or AJVYRACharacterSeedManager()
        )

    def build(
        self,
        request: ShotCharacterRequest,
        episode_id: str,
        shot_id: str,
    ) -> CharacterPromptPackage:

        character = self.registry.get(
            request.character_id
        )

        appearance = character.appearance
        personality = character.personality

        outfit = None

        if request.outfit_id:
            outfit = self.registry.get_outfit(
                character.character_id,
                request.outfit_id,
            )
        elif character.outfits:
            locked = [
                item
                for item in character.outfits
                if item.locked
            ]

            outfit = (
                locked[0]
                if locked
                else character.outfits[0]
            )

        positive_parts = [
            character.visual_style,
            f"character: {character.name}",
            f"age appearance: {appearance.age_range}",
            f"body type: {appearance.body_type}",
            f"skin tone: {appearance.skin_tone}",
            f"face shape: {appearance.face_shape}",
            f"eye color: {appearance.eye_color}",
            f"eye shape: {appearance.eye_shape}",
            f"hair color: {appearance.hair_color}",
            f"hair style: {appearance.hair_style}",
            f"hair length: {appearance.hair_length}",
        ]

        if appearance.eyebrow_shape:
            positive_parts.append(
                f"eyebrows: {appearance.eyebrow_shape}"
            )

        if appearance.distinguishing_features:
            positive_parts.append(
                "distinguishing features: "
                + ", ".join(
                    appearance.distinguishing_features
                )
            )

        if outfit:
            positive_parts.extend(
                [
                    f"outfit: {outfit.name}",
                    f"outfit description: {outfit.description}",
                    "outfit colors: "
                    + ", ".join(outfit.colors),
                    "accessories: "
                    + ", ".join(outfit.accessories),
                    f"footwear: {outfit.footwear}",
                ]
            )

        expression = (
            request.expression
            or character.canonical_expression
            or personality.default_expression
        )

        positive_parts.extend(
            [
                f"expression: {expression}",
                f"emotion: {request.emotion}",
                f"action: {request.action}",
                f"pose: {request.pose}",
                f"camera: {request.camera_angle}",
                f"lighting: {request.lighting}",
                f"environment: {request.environment}",
            ]
        )

        if request.additional_prompt:
            positive_parts.append(
                request.additional_prompt
            )

        positive_prompt = ", ".join(
            part
            for part in positive_parts
            if part
        )

        negative_prompt = DEFAULT_NEGATIVE_PROMPT

        references = self.registry.get_reference_images(
            character.character_id
        )

        seed = self.seed_manager.make_seed(
            character.character_id,
            episode_id,
            shot_id,
        )

        return CharacterPromptPackage(
            character_id=character.character_id,
            positive_prompt=positive_prompt,
            negative_prompt=negative_prompt,
            reference_paths=[
                str(path)
                for path in references
            ],
            identity_strength=clamp(
                character.identity_strength,
                0.0,
                1.0,
            ),
            style_strength=clamp(
                character.style_strength,
                0.0,
                1.0,
            ),
            seed=seed,
            metadata={
                "episode_id": episode_id,
                "shot_id": shot_id,
                "character_hash": character.identity_hash,
                "outfit_id": (
                    outfit.outfit_id
                    if outfit
                    else None
                ),
            },
        )


# ============================================================
# Provider Result
# ============================================================


@dataclass
class ImageGenerationResult:
    success: bool
    provider: str
    output_path: Optional[str] = None
    remote_id: Optional[str] = None
    error: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> Dict[str, Any]:
        return asdict(self)


# ============================================================
# Provider Interface
# ============================================================


class AJVYRAImageProvider:
    name = "base"

    def generate(
        self,
        package: CharacterPromptPackage,
        output_path: Path,
        width: int = 1024,
        height: int = 1024,
    ) -> ImageGenerationResult:

        raise NotImplementedError


# ============================================================
# Local Diffusers Provider
# ============================================================


class AJVYRADiffusersImageProvider(AJVYRAImageProvider):
    """
    Optional local provider.

    Requires:
        pip install torch diffusers transformers accelerate safetensors

    This provider is intentionally lazy-loaded.

    IP-Adapter support is optional. If available, character
    reference images can guide generation.

    The implementation follows the official Diffusers pattern:
        load pipeline
        load IP-Adapter
        set adapter scale
        pass reference image
    """

    name = "diffusers"

    def __init__(
        self,
        model_id: str = (
            "stabilityai/stable-diffusion-xl-base-1.0"
        ),
        ip_adapter_repo: str = "h94/IP-Adapter",
        ip_adapter_subfolder: str = "sdxl_models",
        ip_adapter_weight: str = "ip-adapter_sdxl.bin",
        device: Optional[str] = None,
        dtype: str = "float16",
    ):
        self.model_id = model_id
        self.ip_adapter_repo = ip_adapter_repo
        self.ip_adapter_subfolder = ip_adapter_subfolder
        self.ip_adapter_weight = ip_adapter_weight

        self.device = (
            device
            or os.getenv("AJVYRA_IMAGE_DEVICE", "")
            or "cuda"
        )

        self.dtype_name = dtype

        self.pipeline = None

    def _load(self) -> None:

        if self.pipeline is not None:
            return

        try:
            import torch
            from diffusers import (
                AutoPipelineForText2Image,
            )
        except ImportError as exc:
            raise RuntimeError(
                "Diffusers backend requires torch and diffusers."
            ) from exc

        if self.dtype_name == "float32":
            dtype = torch.float32
        else:
            dtype = torch.float16

        device = self.device

        if (
            device == "cuda"
            and not torch.cuda.is_available()
        ):
            device = "cpu"

        self.pipeline = (
            AutoPipelineForText2Image.from_pretrained(
                self.model_id,
                torch_dtype=dtype,
            )
        )

        self.pipeline = self.pipeline.to(device)

        if hasattr(
            self.pipeline,
            "load_ip_adapter",
        ):
            try:
                self.pipeline.load_ip_adapter(
                    self.ip_adapter_repo,
                    subfolder=self.ip_adapter_subfolder,
                    weight_name=self.ip_adapter_weight,
                )
            except Exception:
                # IP-Adapter is optional. The base model can still
                # generate without it.
                pass

    def generate(
        self,
        package: CharacterPromptPackage,
        output_path: Path,
        width: int = 1024,
        height: int = 1024,
    ) -> ImageGenerationResult:

        try:
            self._load()

            import torch

            generator = torch.Generator(
                device=self.pipeline.device
            ).manual_seed(package.seed)

            kwargs = {
                "prompt": package.positive_prompt,
                "negative_prompt": package.negative_prompt,
                "width": width,
                "height": height,
                "generator": generator,
            }

            references = package.reference_paths

            if references and hasattr(
                self.pipeline,
                "set_ip_adapter_scale",
            ):

                from PIL import Image

                reference_images = [
                    Image.open(path).convert("RGB")
                    for path in references[:4]
                ]

                self.pipeline.set_ip_adapter_scale(
                    package.identity_strength
                )

                kwargs[
                    "ip_adapter_image"
                ] = reference_images[
                    0
                ]

            result = self.pipeline(
                **kwargs
            )

            image = result.images[0]

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            image.save(
                output_path
            )

            return ImageGenerationResult(
                success=True,
                provider=self.name,
                output_path=str(output_path),
                raw={
                    "model_id": self.model_id,
                    "seed": package.seed,
                    "references": references,
                },
            )

        except Exception as exc:

            return ImageGenerationResult(
                success=False,
                provider=self.name,
                error=str(exc),
            )


# ============================================================
# Generic HTTP Provider
# ============================================================


class AJVYRAHTTPImageProvider(AJVYRAImageProvider):
    """
    Generic AJVYRA provider gateway.

    Expected response examples:

        {
            "image_base64": "...",
            "id": "generation_123"
        }

    or:

        {
            "image_url": "https://..."
        }

    The provider itself can be your own AJVYRA backend.
    """

    name = "ajvyra_http"

    def __init__(
        self,
        endpoint: str,
        api_key: str = "",
        timeout: int = 300,
    ):
        self.endpoint = endpoint
        self.api_key = api_key
        self.timeout = timeout

    def _request(
        self,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:

        body = json.dumps(
            payload,
            ensure_ascii=False,
        ).encode("utf-8")

        request = urllib.request.Request(
            self.endpoint,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                **(
                    {
                        "Authorization":
                            f"Bearer {self.api_key}"
                    }
                    if self.api_key
                    else {}
                ),
            },
        )

        with urllib.request.urlopen(
            request,
            timeout=self.timeout,
        ) as response:

            raw = response.read().decode(
                "utf-8"
            )

        return json.loads(raw)

    def generate(
        self,
        package: CharacterPromptPackage,
        output_path: Path,
        width: int = 1024,
        height: int = 1024,
    ) -> ImageGenerationResult:

        try:

            payload = {
                "engine": ENGINE_NAME,
                "operation": "character_image",
                "prompt": package.positive_prompt,
                "negative_prompt": package.negative_prompt,
                "references": package.reference_paths,
                "identity_strength": (
                    package.identity_strength
                ),
                "style_strength": (
                    package.style_strength
                ),
                "seed": package.seed,
                "width": width,
                "height": height,
                "metadata": package.metadata,
            }

            response = self._request(
                payload
            )

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            image_base64 = response.get(
                "image_base64"
            )

            if image_base64:

                raw_bytes = base64.b64decode(
                    image_base64
                )

                output_path.write_bytes(
                    raw_bytes
                )

            else:

                image_url = response.get(
                    "image_url"
                )

                if not image_url:
                    raise RuntimeError(
                        "Provider returned neither "
                        "image_base64 nor image_url."
                    )

                urllib.request.urlretrieve(
                    image_url,
                    output_path,
                )

            return ImageGenerationResult(
                success=True,
                provider=self.name,
                output_path=str(output_path),
                remote_id=response.get("id"),
                raw=response,
            )

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            OSError,
            ValueError,
            RuntimeError,
        ) as exc:

            return ImageGenerationResult(
                success=False,
                provider=self.name,
                error=str(exc),
            )


# ============================================================
# Gemini Image Provider
# ============================================================


class AJVYRAGeminiImageProvider(AJVYRAImageProvider):
    """
    Google Gemini image generation adapter.

    API key is read from:
        GEMINI_API_KEY

    Model is configurable with:
        AJVYRA_GEMINI_IMAGE_MODEL

    This adapter intentionally isolates Google-specific code
    from the rest of AJVYRA.
    """

    name = "gemini"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
        )

        self.model = (
            model
            or os.getenv(
                "AJVYRA_GEMINI_IMAGE_MODEL"
            )
            or "gemini-3.1-flash-image"
        )

        self.client = None

    def _load(self) -> None:

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
                "Install the Google GenAI SDK first."
            ) from exc

        self.client = genai.Client(
            api_key=self.api_key
        )

    def generate(
        self,
        package: CharacterPromptPackage,
        output_path: Path,
        width: int = 1024,
        height: int = 1024,
    ) -> ImageGenerationResult:

        try:

            self._load()

            prompt = (
                package.positive_prompt
                + "\n\n"
                + "Maintain the exact canonical "
                  "character identity from the supplied "
                  "reference image."
                + "\n"
                + "Do not redesign the character."
                + "\n"
                + "Do not change hair color, eye color, "
                  "face shape, age appearance, or outfit "
                  "unless explicitly requested."
                + "\n"
                + f"Negative prompt: "
                f"{package.negative_prompt}"
            )

            content: List[Any] = [
                prompt
            ]

            reference_paths = (
                package.reference_paths[:3]
            )

            for path in reference_paths:

                with open(
                    path,
                    "rb",
                ) as handle:

                    image_bytes = handle.read()

                content.append(
                    {
                        "type": "image",
                        "data": base64.b64encode(
                            image_bytes
                        ).decode("utf-8"),
                        "mime_type": (
                            "image/png"
                            if path.lower().endswith(".png")
                            else "image/jpeg"
                        ),
                    }
                )

            interaction = (
                self.client.interactions.create(
                    model=self.model,
                    input=content,
                )
            )

            output_image = getattr(
                interaction,
                "output_image",
                None,
            )

            if output_image is None:
                raise RuntimeError(
                    "Gemini returned no output image."
                )

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            output_path.write_bytes(
                base64.b64decode(
                    output_image.data
                )
            )

            return ImageGenerationResult(
                success=True,
                provider=self.name,
                output_path=str(output_path),
                raw={
                    "model": self.model,
                    "seed": package.seed,
                },
            )

        except Exception as exc:

            return ImageGenerationResult(
                success=False,
                provider=self.name,
                error=str(exc),
            )


# ============================================================
# Provider Router
# ============================================================


class AJVYRAImageProviderRouter:
    """
    Selects the active image backend.

    Modes:
        local
        gemini
        http
        auto

    Environment:
        AJVYRA_IMAGE_PROVIDER
        AJVYRA_IMAGE_ENDPOINT
        AJVYRA_IMAGE_API_KEY
    """

    def __init__(
        self,
        provider_mode: Optional[str] = None,
    ):

        self.mode = (
            provider_mode
            or os.getenv(
                "AJVYRA_IMAGE_PROVIDER",
                "local",
            )
        ).lower()

        self._provider: Optional[
            AJVYRAImageProvider
        ] = None

    def provider(self) -> AJVYRAImageProvider:

        if self._provider is not None:
            return self._provider

        if self.mode == "gemini":

            self._provider = (
                AJVYRAGeminiImageProvider()
            )

        elif self.mode == "http":

            endpoint = os.getenv(
                "AJVYRA_IMAGE_ENDPOINT",
                "",
            )

            if not endpoint:
                raise RuntimeError(
                    "AJVYRA_IMAGE_ENDPOINT "
                    "is required for HTTP mode."
                )

            self._provider = (
                AJVYRAHTTPImageProvider(
                    endpoint=endpoint,
                    api_key=os.getenv(
                        "AJVYRA_IMAGE_API_KEY",
                        "",
                    ),
                )
            )

        elif self.mode == "local":

            self._provider = (
                AJVYRADiffusersImageProvider()
            )

        elif self.mode == "auto":

            endpoint = os.getenv(
                "AJVYRA_IMAGE_ENDPOINT",
                "",
            )

            if endpoint:
                self._provider = (
                    AJVYRAHTTPImageProvider(
                        endpoint=endpoint,
                        api_key=os.getenv(
                            "AJVYRA_IMAGE_API_KEY",
                            "",
                        ),
                    )
                )

            elif (
                os.getenv("GEMINI_API_KEY")
                or os.getenv("GOOGLE_API_KEY")
            ):
                self._provider = (
                    AJVYRAGeminiImageProvider()
                )

            else:
                self._provider = (
                    AJVYRADiffusersImageProvider()
                )

        else:
            raise ValueError(
                f"Unsupported image provider: {self.mode}"
            )

        return self._provider


# ============================================================
# Consistency Validator
# ============================================================


@dataclass
class ConsistencyCheck:
    passed: bool
    score: float
    warnings: List[str]
    errors: List[str]
    details: Dict[str, Any] = field(
        default_factory=dict
    )

    def normalized(self) -> Dict[str, Any]:
        return asdict(self)


class AJVYRACharacterConsistencyValidator:

    def __init__(
        self,
        registry: AJVYRACharacterRegistry,
    ):
        self.registry = registry

    def validate_character(
        self,
        character_id: str,
    ) -> ConsistencyCheck:

        warnings = []
        errors = []
        score = 100.0

        character = self.registry.get(
            character_id
        )

        appearance = character.appearance

        required_fields = {
            "eye_color": appearance.eye_color,
            "hair_color": appearance.hair_color,
            "hair_style": appearance.hair_style,
            "face_shape": appearance.face_shape,
        }

        for field_name, value in required_fields.items():

            if not value:

                warnings.append(
                    f"Missing canonical field: "
                    f"{field_name}"
                )

                score -= 8

        if not character.references:

            warnings.append(
                "Character has no visual reference image."
            )

            score -= 30

        if not character.outfits:

            warnings.append(
                "Character has no locked outfit."
            )

            score -= 10

        if not character.identity_hash:

            errors.append(
                "Character identity hash is missing."
            )

            score -= 20

        score = clamp(
            score,
            0.0,
            100.0,
        )

        passed = (
            not errors
            and score >= 70
        )

        return ConsistencyCheck(
            passed=passed,
            score=score,
            warnings=warnings,
            errors=errors,
            details={
                "character_id": character_id,
                "reference_count": len(
                    character.references
                ),
                "outfit_count": len(
                    character.outfits
                ),
                "identity_hash": (
                    character.identity_hash
                ),
            },
        )

    def validate_shot_package(
        self,
        package: CharacterPromptPackage,
    ) -> ConsistencyCheck:

        warnings = []
        errors = []

        score = 100.0

        if not package.reference_paths:

            warnings.append(
                "No reference image supplied."
            )

            score -= 35

        if package.identity_strength < 0.6:

            warnings.append(
                "Identity strength is relatively low."
            )

            score -= 15

        if not package.positive_prompt:

            errors.append(
                "Positive prompt is empty."
            )

            score -= 30

        if not package.negative_prompt:

            warnings.append(
                "Negative prompt is empty."
            )

            score -= 10

        score = clamp(
            score,
            0.0,
            100.0,
        )

        return ConsistencyCheck(
            passed=(
                not errors
                and score >= 70
            ),
            score=score,
            warnings=warnings,
            errors=errors,
            details={
                "character_id": package.character_id,
                "seed": package.seed,
                "references": len(
                    package.reference_paths
                ),
            },
        )


# ============================================================
# Shot Reference Manager
# ============================================================


class AJVYRAShotReferenceManager:

    def __init__(
        self,
        root: str | Path = (
            "generated/anime_production"
        ),
    ):
        self.root = Path(root)

    def create_manifest(
        self,
        anime_id: str,
        episode_id: str,
        shot_id: str,
        packages: Sequence[
            CharacterPromptPackage
        ],
    ) -> Path:

        path = (
            self.root
            / safe_slug(anime_id)
            / "season_01"
            / safe_slug(episode_id)
            / "shots"
            / safe_slug(shot_id)
        )

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        manifest = {
            "engine": ENGINE_NAME,
            "version": ENGINE_VERSION,
            "anime_id": anime_id,
            "episode_id": episode_id,
            "shot_id": shot_id,
            "created_at": utc_timestamp(),
            "characters": [
                package.normalized()
                for package in packages
            ],
        }

        manifest_path = (
            path / "character_references.json"
        )

        write_json(
            manifest_path,
            manifest,
        )

        return manifest_path


# ============================================================
# Main Character Consistency Engine
# ============================================================


class AJVYRACharacterConsistencyEngine:

    def __init__(
        self,
        root: str | Path = (
            "generated/anime_characters"
        ),
        image_provider: Optional[
            AJVYRAImageProvider
        ] = None,
    ):

        self.registry = (
            AJVYRACharacterRegistry(root)
        )

        self.seed_manager = (
            AJVYRACharacterSeedManager()
        )

        self.prompt_builder = (
            AJVYRACharacterPromptBuilder(
                registry=self.registry,
                seed_manager=self.seed_manager,
            )
        )

        self.validator = (
            AJVYRACharacterConsistencyValidator(
                registry=self.registry
            )
        )

        self.reference_manager = (
            AJVYRAShotReferenceManager()
        )

        self.image_provider = (
            image_provider
            or AJVYRAImageProviderRouter().provider()
        )

    # --------------------------------------------------------
    # Character creation
    # --------------------------------------------------------

    def create_character(
        self,
        anime_id: str,
        character_id: str,
        name: str,
        appearance: CharacterAppearance,
        personality: Optional[
            CharacterPersonality
        ] = None,
        visual_style: str = (
            "cinematic anime, high-detail"
        ),
    ) -> CharacterIdentity:

        character = CharacterIdentity(
            character_id=character_id,
            name=name,
            anime_id=anime_id,
            appearance=appearance,
            personality=(
                personality
                or CharacterPersonality()
            ),
            visual_style=visual_style,
        )

        character.rebuild_hash()

        return self.registry.register(
            character
        )

    # --------------------------------------------------------
    # Master reference generation
    # --------------------------------------------------------

    def generate_master_reference(
        self,
        character_id: str,
        episode_id: str = "MASTER",
        shot_id: str = "CHARACTER_SHEET",
        expression: str = "neutral",
        outfit_id: str = "",
        width: int = 1024,
        height: int = 1024,
    ) -> ImageGenerationResult:

        character = self.registry.get(
            character_id
        )

        request = ShotCharacterRequest(
            character_id=character_id,
            expression=expression,
            emotion="neutral",
            action="standing naturally",
            outfit_id=outfit_id,
            pose=(
                "front-facing character sheet, "
                "relaxed standing pose"
            ),
            camera_angle="front portrait",
            lighting="soft cinematic studio lighting",
            environment=(
                "clean neutral character reference "
                "background"
            ),
            additional_prompt=(
                "full canonical character reference, "
                "clear face, clear hair silhouette, "
                "clear clothing details"
            ),
        )

        package = self.prompt_builder.build(
            request,
            episode_id,
            shot_id,
        )

        validation = (
            self.validator.validate_shot_package(
                package
            )
        )

        if not validation.passed:
            return ImageGenerationResult(
                success=False,
                provider=self.image_provider.name,
                error=json.dumps(
                    validation.normalized(),
                    ensure_ascii=False,
                ),
            )

        output_directory = (
            Path(
                "generated/anime_characters"
            )
            / safe_slug(character.anime_id)
            / safe_slug(character.character_id)
            / "master"
        )

        output_path = (
            output_directory
            / "master_reference.png"
        )

        result = self.image_provider.generate(
            package=package,
            output_path=output_path,
            width=width,
            height=height,
        )

        if result.success:

            self.registry.add_reference(
                character_id=character_id,
                source_path=result.output_path,
                reference_type="master",
                view="front",
                priority=1.0,
                notes="Canonical AJVYRA master reference.",
            )

        return result

    # --------------------------------------------------------
    # Shot image generation
    # --------------------------------------------------------

    def generate_character_shot(
        self,
        anime_id: str,
        episode_id: str,
        shot_id: str,
        request: ShotCharacterRequest,
        width: int = 1280,
        height: int = 720,
    ) -> ImageGenerationResult:

        package = self.prompt_builder.build(
            request,
            episode_id,
            shot_id,
        )

        validation = (
            self.validator.validate_shot_package(
                package
            )
        )

        self.reference_manager.create_manifest(
            anime_id=anime_id,
            episode_id=episode_id,
            shot_id=shot_id,
            packages=[package],
        )

        if not validation.passed:

            return ImageGenerationResult(
                success=False,
                provider=self.image_provider.name,
                error=json.dumps(
                    validation.normalized(),
                    ensure_ascii=False,
                ),
            )

        output_path = (
            Path(
                "generated/anime_production"
            )
            / safe_slug(anime_id)
            / "season_01"
            / safe_slug(episode_id)
            / "media"
            / "images"
            / f"{safe_slug(shot_id)}_"
              f"{safe_slug(request.character_id)}.png"
        )

        return self.image_provider.generate(
            package=package,
            output_path=output_path,
            width=width,
            height=height,
        )

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    def validate_all_characters(
        self,
    ) -> Dict[str, Any]:

        results = {}

        for character_id in self.registry.characters:

            results[
                character_id
            ] = self.validator.validate_character(
                character_id
            ).normalized()

        return {
            "engine": ENGINE_NAME,
            "version": ENGINE_VERSION,
            "checked_at": utc_timestamp(),
            "character_count": len(results),
            "results": results,
        }


# ============================================================
# Demo Configuration
# ============================================================


def create_demo_character(
    engine: AJVYRACharacterConsistencyEngine,
) -> CharacterIdentity:

    character_id = "veylora_main_01"

    if engine.registry.exists(
        character_id
    ):
        return engine.registry.get(
            character_id
        )

    appearance = CharacterAppearance(
        age_range="late teenager",
        height="average",
        body_type="slim athletic",
        skin_tone="light warm neutral",
        face_shape="soft oval",
        eye_color="deep violet",
        eye_shape="slightly narrow almond",
        eyebrow_shape="straight natural",
        hair_color="silver-white",
        hair_style="layered slightly messy anime hair",
        hair_length="medium",
        distinguishing_features=[
            "small scar near left eyebrow",
            "distinctive silver hair fringe",
        ],
    )

    personality = CharacterPersonality(
        personality_traits=[
            "quiet",
            "observant",
            "kind",
            "reserved",
            "determined",
        ],
        emotional_range=[
            "neutral",
            "sad",
            "angry",
            "afraid",
            "hopeful",
            "happy",
        ],
        default_expression="calm neutral",
        speech_style="short thoughtful sentences",
        mannerisms=[
            "looks away briefly when embarrassed",
            "slow deliberate movements",
        ],
    )

    character = engine.create_character(
        anime_id="Veylora",
        character_id=character_id,
        name="Aren Veyl",
        appearance=appearance,
        personality=personality,
        visual_style=(
            "cinematic anime film, detailed "
            "hand-painted backgrounds, realistic "
            "anime character rendering, expressive eyes"
        ),
    )

    engine.registry.unlock(
        character_id
    )

    engine.registry.add_outfit(
        character_id,
        CharacterOutfit(
            outfit_id="default_school",
            name="Veylora School Uniform",
            description=(
                "dark charcoal school jacket, "
                "white shirt, narrow black tie, "
                "dark trousers"
            ),
            colors=[
                "charcoal",
                "white",
                "black",
            ],
            accessories=[
                "small silver pendant",
            ],
            footwear="black low-top shoes",
            season="default",
            locked=True,
        ),
    )

    engine.registry.lock(
        character_id
    )

    return character


# ============================================================
# CLI
# ============================================================


def print_result(
    result: ImageGenerationResult,
) -> None:

    print(
        json.dumps(
            result.normalized(),
            ensure_ascii=False,
            indent=2,
        )
    )


def main() -> None:

    import argparse

    parser = argparse.ArgumentParser(
        description=ENGINE_NAME
    )

    parser.add_argument(
        "--provider",
        choices=[
            "local",
            "gemini",
            "http",
            "auto",
        ],
        default=None,
    )

    parser.add_argument(
        "--create-demo",
        action="store_true",
    )

    parser.add_argument(
        "--generate-master",
        action="store_true",
    )

    parser.add_argument(
        "--generate-shot",
        action="store_true",
    )

    parser.add_argument(
        "--validate",
        action="store_true",
    )

    parser.add_argument(
        "--character",
        default="veylora_main_01",
    )

    args = parser.parse_args()

    engine = AJVYRACharacterConsistencyEngine(
        image_provider=(
            AJVYRAImageProviderRouter(
                args.provider
            ).provider()
            if args.provider
            else None
        )
    )

    if args.create_demo:

        character = create_demo_character(
            engine
        )

        print(
            json.dumps(
                character.normalized(),
                ensure_ascii=False,
                indent=2,
            )
        )

    if args.validate:

        report = (
            engine.validate_all_characters()
        )

        print(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            )
        )

    if args.generate_master:

        result = engine.generate_master_reference(
            character_id=args.character
        )

        print_result(
            result
        )

    if args.generate_shot:

        request = ShotCharacterRequest(
            character_id=args.character,
            expression="sad but controlled",
            emotion="sad",
            action=(
                "standing alone in light rain, "
                "looking toward the distant city"
            ),
            outfit_id="default_school",
            pose="natural standing pose",
            camera_angle="cinematic medium close-up",
            lighting="blue-gray rainy evening",
            environment=(
                "quiet urban street at night, "
                "wet pavement and distant lights"
            ),
        )

        result = engine.generate_character_shot(
            anime_id="Veylora",
            episode_id="episode_01",
            shot_id="shot_001",
            request=request,
        )

        print_result(
            result
        )


if __name__ == "__main__":
    main()
