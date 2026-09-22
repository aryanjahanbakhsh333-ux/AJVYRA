from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TTSConfig:
    sample_rate: int = 22050
    n_mels: int = 80
    n_fft: int = 1024
    hop_length: int = 256
    win_length: int = 1024

    text_embedding_dim: int = 256
    encoder_dim: int = 256
    speaker_dim: int = 128
    emotion_dim: int = 64
    prosody_dim: int = 64

    decoder_channels: int = 256
    decoder_layers: int = 8

    max_text_length: int = 512
    max_audio_seconds: int = 30

    learning_rate: float = 2e-4
    batch_size: int = 8
    epochs: int = 100

    root: Path = Path("ajvyra_tts_data")

    @property
    def checkpoints(self) -> Path:
        return self.root / "checkpoints"

    @property
    def datasets(self) -> Path:
        return self.root / "datasets"

    @property
    def voices(self) -> Path:
        return self.root / "voices"

    @property
    def generated(self) -> Path:
        return self.root / "generated"


TTS_CONFIG = TTSConfig()


def prepare_directories() -> None:
    directories = [
        TTS_CONFIG.root,
        TTS_CONFIG.checkpoints,
        TTS_CONFIG.datasets,
        TTS_CONFIG.voices,
        TTS_CONFIG.generated,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
