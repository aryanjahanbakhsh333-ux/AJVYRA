import hashlib
import json
from pathlib import Path


class TranslationMemory:

    def __init__(
        self,
        path: str = "ajvyra_tts_data/translation_memory.json",
    ):
        self.path = Path(path)
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.data = self._load()

    def _load(self) -> dict:
        if not self.path.exists():
            return {}

        return json.loads(
            self.path.read_text(
                encoding="utf-8"
            )
        )

    def _key(
        self,
        text: str,
        source: str,
        target: str,
    ) -> str:

        raw = (
            f"{source}|{target}|{text}"
        )

        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()

    def get(
        self,
        text: str,
        source: str,
        target: str,
    ):

        return self.data.get(
            self._key(text, source, target)
        )

    def put(
        self,
        text: str,
        source: str,
        target: str,
        translation: str,
    ):

        self.data[
            self._key(text, source, target)
        ] = {
            "source": text,
            "source_language": source,
            "target_language": target,
            "translation": translation,
        }

        self._save()

    def _save(self) -> None:
        self.path.write_text(
            json.dumps(
                self.data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
