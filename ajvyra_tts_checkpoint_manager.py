from pathlib import Path
import torch


class TTSCheckpointManager:

    def __init__(
        self,
        directory: str | Path = "ajvyra_tts_data/checkpoints",
    ):
        self.directory = Path(directory)
        self.directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        model,
        optimizer,
        epoch: int,
        loss: float,
        name: str = "latest",
    ) -> Path:

        path = self.directory / f"{name}.pt"

        torch.save(
            {
                "epoch": epoch,
                "loss": loss,
                "model": model.state_dict(),
                "optimizer": optimizer.state_dict(),
            },
            path,
        )

        return path

    def load(
        self,
        model,
        optimizer=None,
        name: str = "latest",
    ):

        path = self.directory / f"{name}.pt"

        if not path.exists():
            raise FileNotFoundError(
                f"Checkpoint not found: {path}"
            )

        checkpoint = torch.load(
            path,
            map_location="cpu",
        )

        model.load_state_dict(
            checkpoint["model"]
        )

        if optimizer is not None:
            optimizer.load_state_dict(
                checkpoint["optimizer"]
            )

        return {
            "epoch": checkpoint["epoch"],
            "loss": checkpoint["loss"],
        }
