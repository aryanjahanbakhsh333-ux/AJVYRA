from dataclasses import dataclass


@dataclass
class Train:
    name: str
    destination: str
    priority: int
    track: int = 0
    dispatched: bool = False


class RailwayDispatcherGame:
    GAME_ID = "AJVYRA-090"
    TITLE = "Last Station"
    GENRE = "Railway Strategy"

    def __init__(self):
        self.dispatcher = "Mira Kade"
        self.score = 0
        self.errors = 0

        self.trains = [
            Train("Aurora 01", "North City", 2),
            Train("Night Express", "West Port", 3),
            Train("Silver Arrow", "East Valley", 1),
            Train("Dawn Cargo", "South Harbor", 4),
        ]

        self.tracks = {
            1: None,
            2: None,
            3: None,
        }

    def assign_track(self, train_index: int, track: int):
        if train_index < 0 or train_index >= len(self.trains):
            return False

        if track not in self.tracks:
            self.errors += 1
            return False

        train = self.trains[train_index]

        if self.tracks[track] is not None:
            self.errors += 1
            return False

        train.track = track
        self.tracks[track] = train.name

        return True

    def dispatch(self, train_index: int):
        if train_index < 0 or train_index >= len(self.trains):
            return False

        train = self.trains[train_index]

        if train.track == 0:
            self.errors += 1
            return False

        train.dispatched = True
        self.tracks[train.track] = None

        self.score += train.priority * 25

        return True

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "dispatcher": self.dispatcher,
            "score": self.score,
            "errors": self.errors,
            "tracks": self.tracks.copy(),
            "trains": [t.__dict__.copy() for t in self.trains],
        }
