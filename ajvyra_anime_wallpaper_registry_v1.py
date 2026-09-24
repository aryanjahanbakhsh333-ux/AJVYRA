"""
AJVYRA Anime Wallpaper Registry v1
-----------------------------------
New architecture for AJVYRA Anime.

Purpose:
    Manage a collection of 30 original anime wallpaper artworks.

Important:
    - Does NOT delete or modify legacy anime files.
    - Does NOT generate video.
    - Does NOT require a GPU.
    - Does NOT create fake video content.
    - Wallpapers are treated as the final anime-media format.
"""

from __future__ import annotations

import json
import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

WALLPAPER_ROOT = PROJECT_ROOT / "ajvyra_anime_wallpapers"

CATALOG_FILE = WALLPAPER_ROOT / "wallpaper_catalog.json"

SUPPORTED_IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
}


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class AnimeWallpaper:
    wallpaper_id: str
    title: str
    genre: str
    story: str
    protagonist: str
    supporting_character: str
    location: str
    visual_prompt: str
    image_file: Optional[str] = None
    published: bool = False

    def to_dict(self) -> Dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

class AnimeWallpaperRegistry:
    """
    Central registry for AJVYRA's anime wallpaper collection.
    """

    REQUIRED_COUNT = 30

    def __init__(
        self,
        root: Path = WALLPAPER_ROOT,
        catalog_file: Path = CATALOG_FILE,
    ) -> None:

        self.root = Path(root)
        self.catalog_file = Path(catalog_file)

        self.root.mkdir(parents=True, exist_ok=True)

        self.items: List[AnimeWallpaper] = []

        self.load()

    # -----------------------------------------------------------------------
    # Persistence
    # -----------------------------------------------------------------------

    def load(self) -> None:
        """
        Load an existing catalog.

        Missing catalogs are allowed and start empty.
        """

        if not self.catalog_file.exists():
            self.items = []
            return

        try:
            data = json.loads(
                self.catalog_file.read_text(
                    encoding="utf-8"
                )
            )

            if not isinstance(data, list):
                raise ValueError("Catalog root must be a list.")

            self.items = [
                AnimeWallpaper(**item)
                for item in data
            ]

        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            raise RuntimeError(
                f"Unable to load anime wallpaper catalog: {exc}"
            ) from exc

    def save(self) -> None:
        """
        Save the current catalog.
        """

        self.catalog_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        payload = [
            item.to_dict()
            for item in self.items
        ]

        self.catalog_file.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=4
            ),
            encoding="utf-8"
        )

    # -----------------------------------------------------------------------
    # Identity
    # -----------------------------------------------------------------------

    @staticmethod
    def make_id(title: str) -> str:
        """
        Generate a stable ID from the title.
        """

        normalized = " ".join(
            title.strip().lower().split()
        )

        digest = hashlib.sha256(
            normalized.encode("utf-8")
        ).hexdigest()[:12]

        return f"anime-wallpaper-{digest}"

    # -----------------------------------------------------------------------
    # Registration
    # -----------------------------------------------------------------------

    def add(
        self,
        title: str,
        genre: str,
        story: str,
        protagonist: str,
        supporting_character: str,
        location: str,
        visual_prompt: str,
        image_file: Optional[str] = None,
        published: bool = False,
    ) -> AnimeWallpaper:

        title = title.strip()

        if not title:
            raise ValueError("Wallpaper title cannot be empty.")

        if any(item.title.casefold() == title.casefold()
               for item in self.items):
            raise ValueError(
                f"Duplicate wallpaper title: {title}"
            )

        if len(self.items) >= self.REQUIRED_COUNT:
            raise RuntimeError(
                "The 30-item anime wallpaper collection is already full."
            )

        item = AnimeWallpaper(
            wallpaper_id=self.make_id(title),
            title=title,
            genre=genre.strip(),
            story=story.strip(),
            protagonist=protagonist.strip(),
            supporting_character=supporting_character.strip(),
            location=location.strip(),
            visual_prompt=visual_prompt.strip(),
            image_file=image_file,
            published=published,
        )

        self.items.append(item)
        self.save()

        return item

    # -----------------------------------------------------------------------
    # Lookup
    # -----------------------------------------------------------------------

    def get(self, wallpaper_id: str) -> Optional[AnimeWallpaper]:

        for item in self.items:
            if item.wallpaper_id == wallpaper_id:
                return item

        return None

    def search(self, query: str) -> List[AnimeWallpaper]:

        query = query.casefold().strip()

        if not query:
            return list(self.items)

        results = []

        for item in self.items:

            searchable = " ".join([
                item.title,
                item.genre,
                item.story,
                item.protagonist,
                item.supporting_character,
                item.location,
            ]).casefold()

            if query in searchable:
                results.append(item)

        return results

    # -----------------------------------------------------------------------
    # Image validation
    # -----------------------------------------------------------------------

    def validate_image(self, image_file: str) -> Path:

        path = Path(image_file)

        if not path.is_absolute():
            path = self.root / path

        if not path.exists():
            raise FileNotFoundError(
                f"Wallpaper image does not exist: {path}"
            )

        if path.suffix.casefold() not in SUPPORTED_IMAGE_EXTENSIONS:
            raise ValueError(
                f"Unsupported image format: {path.suffix}"
            )

        return path

    # -----------------------------------------------------------------------
    # Publishing
    # -----------------------------------------------------------------------

    def publish(self, wallpaper_id: str) -> AnimeWallpaper:

        item = self.get(wallpaper_id)

        if item is None:
            raise KeyError(
                f"Unknown wallpaper ID: {wallpaper_id}"
            )

        if not item.image_file:
            raise RuntimeError(
                f"Wallpaper '{item.title}' has no image file."
            )

        self.validate_image(item.image_file)

        item.published = True
        self.save()

        return item

    # -----------------------------------------------------------------------
    # Collection status
    # -----------------------------------------------------------------------

    def published_items(self) -> List[AnimeWallpaper]:

        return [
            item
            for item in self.items
            if item.published
        ]

    def count(self) -> int:
        return len(self.items)

    def published_count(self) -> int:
        return len(self.published_items())

    def export_public_catalog(self) -> Dict:

        return {
            "project": "AJVYRA",
            "media_type": "anime_wallpaper",
            "collection_size": self.REQUIRED_COUNT,
            "items": [
                item.to_dict()
                for item in self.published_items()
            ],
        }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:

    registry = AnimeWallpaperRegistry()

    print()
    print("AJVYRA Anime Wallpaper Registry")
    print("--------------------------------")
    print(f"Registered wallpapers : {registry.count()}/30")
    print(f"Published wallpapers  : {registry.published_count()}/30")
    print(f"Catalog               : {registry.catalog_file}")
    print()

    public_catalog = registry.export_public_catalog()

    print(
        json.dumps(
            public_catalog,
            ensure_ascii=False,
            indent=4
        )
    )


if __name__ == "__main__":
    main()
