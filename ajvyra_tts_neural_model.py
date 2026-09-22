import torch
from torch import nn


class AJVYRAEncoder(nn.Module):

    def __init__(
        self,
        vocab_size: int,
        embedding_dim: int = 256,
        hidden_dim: int = 256,
    ):
        super().__init__()

        self.embedding = nn.Embedding(
            vocab_size,
            embedding_dim,
        )

        self.gru = nn.GRU(
            input_size=embedding_dim,
            hidden_size=hidden_dim,
            batch_first=True,
            bidirectional=True,
        )

        self.projection = nn.Linear(
            hidden_dim * 2,
            hidden_dim,
        )

    def forward(self, tokens):
        x = self.embedding(tokens)

        x, _ = self.gru(x)

        return self.projection(x)


class AJVYRAAcousticDecoder(nn.Module):

    def __init__(
        self,
        input_dim: int = 256,
        output_dim: int = 80,
    ):
        super().__init__()

        self.network = nn.Sequential(
            nn.Conv1d(
                input_dim,
                256,
                kernel_size=5,
                padding=2,
            ),
            nn.ReLU(),

            nn.Conv1d(
                256,
                256,
                kernel_size=5,
                padding=2,
            ),
            nn.ReLU(),

            nn.Conv1d(
                256,
                output_dim,
                kernel_size=1,
            ),
        )

    def forward(self, x):
        x = x.transpose(1, 2)

        x = self.network(x)

        return x.transpose(1, 2)


class AJVYRA_TTS_Model(nn.Module):

    def __init__(
        self,
        vocab_size: int,
        speaker_dim: int = 128,
        emotion_dim: int = 12,
        prosody_dim: int = 4,
        mel_dim: int = 80,
    ):
        super().__init__()

        self.encoder = AJVYRAEncoder(
            vocab_size=vocab_size,
        )

        self.speaker_projection = nn.Linear(
            speaker_dim,
            256,
        )

        self.emotion_projection = nn.Linear(
            emotion_dim,
            256,
        )

        self.prosody_projection = nn.Linear(
            prosody_dim,
            256,
        )

        self.decoder = AJVYRAAcousticDecoder(
            input_dim=256,
            output_dim=mel_dim,
        )

    def forward(
        self,
        tokens,
        speaker_embedding,
        emotion_vector,
        prosody_vector,
    ):

        encoded = self.encoder(tokens)

        speaker = self.speaker_projection(
            speaker_embedding
        ).unsqueeze(1)

        emotion = self.emotion_projection(
            emotion_vector
        ).unsqueeze(1)

        prosody = self.prosody_projection(
            prosody_vector
        ).unsqueeze(1)

        conditioned = (
            encoded
            + speaker
            + emotion
            + prosody
        )

        mel = self.decoder(conditioned)

        return mel
