from __future__ import annotations

import threading
import time

from ajvyra_30_ready_shots_v6 import prepare
from ajvyra_hourly_shot_factory_v6 import HourlyShotFactory


def start():

    print("=" * 60)
    print("AJVYRA FINAL AI SHOT FACTORY")
    print("=" * 60)

    # Prepare the first 30 shots.
    prepare()

    factory = HourlyShotFactory()

    worker = threading.Thread(
        target=factory.run_forever,
        daemon=True
    )

    worker.start()

    print()
    print("30 initial shots: READY IN QUEUE")
    print("Hourly factory: ONLINE")
    print("Genre rotation: ONLINE")
    print()
    print("AJVYRA SHOT FACTORY IS RUNNING.")

    while True:
        time.sleep(3600)


if __name__ == "__main__":
    start()
