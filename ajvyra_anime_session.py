from dataclasses import dataclass, field
from datetime import datetime, timezone
import secrets
from typing import Dict


@dataclass
class AnimeSession:
    session_id: str
    anime_id: int | None = None
    audio_language: str = "fa"
    subtitle_language: str = "off"
    position: float = 0.0
    created_at: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )


class AnimeSessionManager:

    def __init__(self):
        self.sessions: Dict[str, AnimeSession] = {}

    def create(self) -> AnimeSession:
        session_id = secrets.token_urlsafe(24)

        session = AnimeSession(
            session_id=session_id
        )

        self.sessions[session_id] = session

        return session

    def get(self, session_id: str):
        return self.sessions.get(session_id)

    def update(
        self,
        session_id: str,
        anime_id: int | None = None,
        audio_language: str | None = None,
        subtitle_language: str | None = None,
        position: float | None = None,
    ):
        session = self.get(session_id)

        if session is None:
            raise KeyError("Session not found.")

        if anime_id is not None:
            session.anime_id = anime_id

        if audio_language is not None:
            session.audio_language = audio_language

        if subtitle_language is not None:
            session.subtitle_language = subtitle_language

        if position is not None:
            session.position = max(
                0,
                float(position)
            )

        return session

    def delete(self, session_id: str):
        return self.sessions.pop(
            session_id,
            None
        )

    def count(self):
        return len(self.sessions)
