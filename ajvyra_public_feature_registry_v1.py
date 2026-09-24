"""
AJVYRA Active Feature Registry
------------------------------
Controls which major systems are active in the public build.

Legacy Anime files are intentionally NOT deleted.
They simply are not registered as active public features.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Feature:
    name: str
    enabled: bool
    public: bool
    description: str


class AJVYRAFeatureRegistry:

    def __init__(self):

        self._features: Dict[str, Feature] = {

            "games": Feature(
                name="games",
                enabled=True,
                public=True,
                description="AJVYRA playable game collection."
            ),

            "anime": Feature(
                name="anime",
                enabled=False,
                public=False,
                description="Legacy Anime system disabled."
            ),

            "anime_wallpapers": Feature(
                name="anime_wallpapers",
                enabled=False,
                public=False,
                description="Anime wallpaper system disabled."
            ),

            "anime_video": Feature(
                name="anime_video",
                enabled=False,
                public=False,
                description="Legacy Anime video system disabled."
            ),

            "anime_audio": Feature(
                name="anime_audio",
                enabled=False,
                public=False,
                description="Legacy Anime audio system disabled."
            ),

            "anime_subtitles": Feature(
                name="anime_subtitles",
                enabled=False,
                public=False,
                description="Legacy Anime subtitle system disabled."
            ),
        }

    def is_enabled(self, feature_name: str) -> bool:

        feature = self._features.get(feature_name)

        if feature is None:
            return False

        return feature.enabled

    def is_public(self, feature_name: str) -> bool:

        feature = self._features.get(feature_name)

        if feature is None:
            return False

        return feature.public

    def active_features(self) -> List[str]:

        return [
            feature.name
            for feature in self._features.values()
            if feature.enabled
        ]

    def public_features(self) -> List[str]:

        return [
            feature.name
            for feature in self._features.values()
            if feature.enabled and feature.public
        ]

    def get_public_manifest(self) -> Dict:

        return {
            "project": "AJVYRA",
            "features": self.public_features(),
            "anime": {
                "enabled": False,
                "public": False
            }
        }


# ------------------------------------------------------------
# Public build integration
# ------------------------------------------------------------

FEATURES = AJVYRAFeatureRegistry()


def anime_is_available() -> bool:
    return FEATURES.is_public("anime")


def games_are_available() -> bool:
    return FEATURES.is_public("games")


def get_public_build_manifest() -> Dict:
    return FEATURES.get_public_manifest()


# ------------------------------------------------------------
# Safety guard
# ------------------------------------------------------------

def prevent_legacy_anime_execution():

    if not anime_is_available():
        return {
            "allowed": False,
            "reason": "Anime is disabled in the current AJVYRA build."
        }

    return {
        "allowed": True
    }


# ------------------------------------------------------------
# Example
# ------------------------------------------------------------

if __name__ == "__main__":

    print("AJVYRA PUBLIC BUILD")
    print("-------------------")

    print(
        "Active features:",
        FEATURES.active_features()
    )

    print(
        "Public features:",
        FEATURES.public_features()
    )

    print(
        "Anime available:",
        anime_is_available()
    )

    print(
        "Games available:",
        games_are_available()
    )

    print(
        "Build manifest:",
        get_public_build_manifest()
    )
