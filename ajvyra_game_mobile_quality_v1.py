from __future__ import annotations

from typing import Dict, Any


class MobileGameQuality:
    """
    Runtime rules for phone/tablet play.
    """

    def __init__(self):
        self.minimum_width = 320
        self.minimum_height = 180
        self.preferred_orientation = "landscape"

    def configure(
        self,
        width: int,
        height: int,
        touch: bool,
    ) -> Dict[str, Any]:
        width = max(
            self.minimum_width,
            int(width),
        )

        height = max(
            self.minimum_height,
            int(height),
        )

        return {
            "viewport": {
                "width": width,
                "height": height,
            },
            "touch": bool(touch),
            "orientation": (
                "landscape"
                if width >= height
                else "portrait"
            ),
            "recommended_orientation":
                self.preferred_orientation,
            "pixel_ratio_aware": True,
            "responsive": True,
            "safe_area": True,
        }

    def quality_profile(
        self,
        width: int,
        height: int,
        touch: bool,
    ) -> Dict[str, Any]:
        config = self.configure(
            width,
            height,
            touch,
        )

        pixels = width * height

        if pixels >= 1920 * 1080:
            tier = "high"
        elif pixels >= 1280 * 720:
            tier = "medium"
        else:
            tier = "mobile"

        config["quality_tier"] = tier

        return config
