from __future__ import annotations


PROFILES = {
    "sport": {
        "background": "arena",
        "primary": "player",
        "actions": ("attack", "strike", "serve", "shoot", "sprint", "trick"),
    },
    "racing": {
        "background": "road",
        "primary": "vehicle",
        "actions": ("accelerate", "boost", "drift", "brake", "drive"),
    },
    "horror": {
        "background": "dark",
        "primary": "player",
        "actions": ("search_room", "stay_calm", "escape", "explore"),
    },
    "space": {
        "background": "space",
        "primary": "ship",
        "actions": ("travel", "scan", "repair", "boost", "explore"),
    },
    "fantasy": {
        "background": "fantasy",
        "primary": "hero",
        "actions": ("attack", "explore", "cast", "build", "discover"),
    },
    "strategy": {
        "background": "grid",
        "primary": "city",
        "actions": ("build", "upgrade", "train", "research", "advance"),
    },
    "simulation": {
        "background": "city",
        "primary": "manager",
        "actions": ("build", "hire", "repair", "upgrade", "serve"),
    },
    "adventure": {
        "background": "adventure",
        "primary": "player",
        "actions": ("explore", "travel", "collect", "rest", "complete"),
    },
}


def profile_for(game_id: int, title: str = "") -> dict:
    text = f"{game_id} {title}".lower()

    if any(x in text for x in (
        "football", "basketball", "volleyball", "tennis",
        "boxing", "wrestling", "hockey", "golf", "skate",
        "boxing", "karate", "mma", "arena",
    )):
        key = "sport"
    elif any(x in text for x in (
        "race", "rally", "car", "motorcycle", "bike",
        "hoverboard", "driver",
    )):
        key = "racing"
    elif any(x in text for x in (
        "horror", "haunted", "shadow", "escape",
    )):
        key = "horror"
    elif any(x in text for x in (
        "space", "starship", "asteroid", "moon",
        "colony", "cosmic",
    )):
        key = "space"
    elif any(x in text for x in (
        "dragon", "wizard", "fantasy", "kingdom",
        "magic", "pirate",
    )):
        key = "fantasy"
    elif any(x in text for x in (
        "manager", "builder", "architect", "factory",
        "governor", "tycoon", "city",
    )):
        key = "strategy"
    elif any(x in text for x in (
        "adventure", "explorer", "detective",
        "expedition", "treasure",
    )):
        key = "adventure"
    else:
        key = "simulation"

    return {
        "type": key,
        **PROFILES[key],
    }
