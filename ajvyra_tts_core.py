from dataclasses import dataclass

import torch

from ajvyra_tts_config import (
    TTS_CONFIG,
    prepare_directories,
)

from ajvyra_tts_tokenizer import (
    AJVYRATokenizer,
)

from ajvyra_tts_emotion_encoder import (
    EmotionEncoder,
)

from ajvyra_tts_prosody_engine import (
    ProsodyEngine,
)

from ajvyra_tts_neural_model import (
    AJVYRA_TTS_Model,
)


@dataclass
class TTSInput:
    text: str
    language: str
    emotion: str = "neutral"
    emotion_intensity: float = 1.0


class AJVYRATTSCore:

    def __init__(self):

        prepare_directories()

        self.tokenizer = AJVYRATokenizer()

        self.emotion_encoder = EmotionEncoder()

        self.prosody_engine = ProsodyEngine()

        self.model = None

    def initialize_model(self):

        self.tokenizer.build_for_language("fa")
        self.tokenizer.build_for_language("ja")

        self.model = AJVYRA_TTS_Model(
            vocab_size=self.tokenizer.vocabulary_size,
            speaker_dim=TTS_CONFIG.speaker_dim,
            emotion_dim=self.emotion_encoder.dimension,
            prosody_dim=4,
            mel_dim=TTS_CONFIG.n_mels,
        )

        return self.model

    def prepare_input(
        self,
        request: TTSInput,
    ):

        tokens = self.tokenizer.encode(
            request.text,
            request.language,
        )

        emotion = self.emotion_encoder.encode(
            request.emotion,
            request.emotion_intensity,
        )

        prosody = self.prosody_engine.analyze(
            request.text,
            request.emotion,
        )

        token_tensor = torch.tensor(
            tokens,
            dtype=torch.long,
        ).unsqueeze(0)

        emotion_tensor = torch.tensor(
            emotion.values,
            dtype=torch.float32,
        ).unsqueeze(0)

        prosody_tensor = torch.tensor(
            [
                prosody.speaking_rate,
                prosody.pitch_shift,
                prosody.energy,
                prosody.pause_scale,
            ],
            dtype=torch.float32,
        ).unsqueeze(0)

        return {
            "tokens": token_tensor,
            "emotion": emotion_tensor,
            "prosody": prosody_tensor,
            "prosody_info": prosody,
            "emotion_info": emotion,
        }

    def forward(
        self,
        request: TTSInput,
        speaker_embedding: torch.Tensor,
    ):

        if self.model is None:
            self.initialize_model()

        prepared = self.prepare_input(request)

        return self.model(
            tokens=prepared["tokens"],
            speaker_embedding=speaker_embedding,
            emotion_vector=prepared["emotion"],
            prosody_vector=prepared["prosody"],
        )


TTS_CORE = AJVYRATTSCore()


if __name__ == "__main__":

    engine = AJVYRATTSCore()

    engine.initialize_model()

    request = TTSInput(
        text="دیگه نمی‌خوام برگردم.",
        language="fa",
        emotion="broken",
        emotion_intensity=0.95,
    )

    speaker = torch.randn(
        1,
        TTS_CONFIG.speaker_dim,
    )

    mel = engine.forward(
        request,
        speaker,
    )

    print("AJVYRA TTS initialized.")
    print("Mel shape:", tuple(mel.shape))
