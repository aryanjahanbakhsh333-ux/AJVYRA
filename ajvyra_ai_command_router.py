"""
AJVYRA AI COMMAND ROUTER

Converts Persian/English human commands into deterministic
AJVYRA production operations.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class RoutedCommand:
    operation: str
    arguments: Dict[str, Any] = field(default_factory=dict)


class AICommandRouter:

    OPERATIONS = {
        "build_all",
        "build_anime",
        "build_games",
        "posters",
        "publish",
        "sync_site",
        "status",
        "search",
        "inspect",
    }

    def normalize(self, text: str) -> str:
        text = str(text or "").strip().lower()

        replacements = {
            "ي": "ی",
            "ى": "ی",
            "ك": "ک",
            "ۀ": "ه",
            "ة": "ه",
            "\u200c": " ",
            "\u200f": "",
            "\u200e": "",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        text = re.sub(r"\s+", " ", text)

        return text

    def route(self, text: str, **kwargs: Any) -> RoutedCommand:
        normalized = self.normalize(text)

        # Explicit operation names first.
        if normalized in self.OPERATIONS:
            return RoutedCommand(
                operation=normalized,
                arguments=dict(kwargs),
            )

        # -----------------------------------------------------
        # BUILD EVERYTHING
        # -----------------------------------------------------

        all_patterns = [
            "build everything",
            "build all",
            "create everything",
            "create all",
            "make everything",
            "make all",
            "همه رو بساز",
            "همه را بساز",
            "همه رو کامل کن",
            "همه را کامل کن",
            "همه انیمه ها و بازی ها رو بساز",
            "همه انیمه ها و بازی ها را بساز",
            "کل پروژه رو بساز",
            "کل پروژه را بساز",
            "کل ajvyra رو بساز",
        ]

        if self._matches_any(normalized, all_patterns):
            return RoutedCommand(
                "build_all",
                {"resume": True, **kwargs},
            )

        # -----------------------------------------------------
        # ANIME
        # -----------------------------------------------------

        anime_patterns = [
            "build anime",
            "build all anime",
            "create anime",
            "create all anime",
            "make all anime",
            "همه انیمه ها رو بساز",
            "همه انیمه ها را بساز",
            "همه انیمه ها رو کامل کن",
            "همه انیمه ها را کامل کن",
            "انیمه ها رو بساز",
            "انیمه ها را بساز",
        ]

        if self._matches_any(normalized, anime_patterns):
            return RoutedCommand(
                "build_anime",
                {"resume": True, **kwargs},
            )

        # -----------------------------------------------------
        # GAMES
        # -----------------------------------------------------

        game_patterns = [
            "build games",
            "build all games",
            "create games",
            "create all games",
            "make all games",
            "همه بازی ها رو بساز",
            "همه بازی ها را بساز",
            "همه بازی ها رو کامل کن",
            "همه بازی ها را کامل کن",
            "بازی ها رو بساز",
            "بازی ها را بساز",
        ]

        if self._matches_any(normalized, game_patterns):
            return RoutedCommand(
                "build_games",
                {"resume": True, **kwargs},
            )

        # -----------------------------------------------------
        # POSTERS
        # -----------------------------------------------------

        poster_patterns = [
            "generate posters",
            "create posters",
            "make posters",
            "generate all posters",
            "پوسترها رو بساز",
            "پوسترها را بساز",
            "پوستر همه انیمه ها رو بساز",
            "پوستر همه انیمه ها را بساز",
        ]

        if self._matches_any(normalized, poster_patterns):
            return RoutedCommand(
                "posters",
                {"resume": True, **kwargs},
            )

        # -----------------------------------------------------
        # PUBLISH / SITE
        # -----------------------------------------------------

        publish_patterns = [
            "publish",
            "publish everything",
            "publish all",
            "publish site",
            "انتشار بده",
            "همه رو منتشر کن",
            "همه را منتشر کن",
            "روی سایت منتشر کن",
            "روی سایت قرار بده",
        ]

        if self._matches_any(normalized, publish_patterns):
            return RoutedCommand(
                "publish",
                dict(kwargs),
            )

        site_patterns = [
            "sync site",
            "update site",
            "update search",
            "sync search",
            "سایت رو آپدیت کن",
            "سایت را آپدیت کن",
            "سرچ سایت رو آپدیت کن",
            "سرچ سایت را آپدیت کن",
            "همه رو داخل سایت بیار",
            "همه را داخل سایت بیاور",
        ]

        if self._matches_any(normalized, site_patterns):
            return RoutedCommand(
                "sync_site",
                dict(kwargs),
            )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        status_patterns = [
            "status",
            "project status",
            "what is the status",
            "وضعیت",
            "وضعیت پروژه",
            "چقدر کامل شده",
            "پروژه چقدر پیش رفته",
        ]

        if self._matches_any(normalized, status_patterns):
            return RoutedCommand(
                "status",
                dict(kwargs),
            )

        # -----------------------------------------------------
        # SEARCH
        # -----------------------------------------------------

        search_match = re.match(
            r"^(?:search|find|جستجو|سرچ)\s+(.+)$",
            normalized,
        )

        if search_match:
            return RoutedCommand(
                "search",
                {
                    "query": search_match.group(1).strip(),
                    **kwargs,
                },
            )

        # -----------------------------------------------------
        # INSPECT
        # -----------------------------------------------------

        inspect_patterns = [
            "inspect",
            "inspect project",
            "بررسی پروژه",
            "پروژه رو بررسی کن",
            "پروژه را بررسی کن",
        ]

        if self._matches_any(normalized, inspect_patterns):
            return RoutedCommand(
                "inspect",
                dict(kwargs),
            )

        raise ValueError(
            f"Unknown AJVYRA command: {text}"
        )

    @staticmethod
    def _matches_any(
        text: str,
        patterns: list[str],
    ) -> bool:

        return any(
            text == pattern or pattern in text
            for pattern in patterns
        )
