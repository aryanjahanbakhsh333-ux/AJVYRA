from dataclasses import dataclass
from typing import List


@dataclass
class Track:
    name: str
    bpm: int
    energy: int
    genre: str


class MusicProducerGame:
    GAME_ID = "AJVYRA-068"
    TITLE = "Midnight Producer"
    GENRE = "Music Creation Simulation"

    def __init__(self):
        self.cash = 1500
        self.fans = 0
        self.studio_level = 1
        self.tracks: List[Track] = []

    def create_track(self, name: str, bpm: int, energy: int, genre: str):
        if self.cash < 100:
            return False

        bpm = max(50, min(220, bpm))
        energy = max(0, min(100, energy))

        self.cash -= 100

        track = Track(name, bpm, energy, genre)
        self.tracks.append(track)

        return True

    def release_track(self, index: int):
        if index < 0 or index >= len(self.tracks):
            return False

        track = self.tracks[index]

        quality = (
            self.studio_level * 20
            + track.energy // 2
            + min(30, abs(track.bpm - 120) // 4)
        )

        fans_gained = max(10, quality * 3)

        self.fans += fans_gained
        self.cash += fans_gained * 2

        return {
            "track": track.name,
            "quality": quality,
            "fans_gained": fans_gained,
        }

    def upgrade_studio(self):
        cost = self.studio_level * 1000

        if self.cash < cost:
            return False

        self.cash -= cost
        self.studio_level += 1
        return True

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "cash": self.cash,
            "fans": self.fans,
            "studio_level": self.studio_level,
            "tracks": [track.__dict__.copy() for track in self.tracks],
        }
