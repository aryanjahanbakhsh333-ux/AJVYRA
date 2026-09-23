60 — ajvyra_complete_shot_factory_v7.py

from __future__ import annotations

import threading
import time
from pathlib import Path

from ajvyra_30_ready_shots_v6 import prepare
from ajvyra_real_shot_worker_v7 import (
    RealShotWorker
)


ROOT = Path(__file__).resolve().parent


def start():

    print(
        "AJVYRA COMPLETE SHOT FACTORY"
    )

    # -------------------------------------------------
    # 1. Create the initial 30-shot queue.
    # -------------------------------------------------

    prepare()

    # -------------------------------------------------
    # 2. Start the real Wan production worker.
    # -------------------------------------------------

    worker = RealShotWorker()

    thread = threading.Thread(
        target=worker.process_next,
        daemon=True
    )

    # -------------------------------------------------
    # 3. Produce queued shots.
    # -------------------------------------------------

    def production_loop():

        while True:

            try:
                worker.process_next()

            except Exception as error:

                print(
                    "[AJVYRA] Production paused:",
                    error
                )

                time.sleep(60)

    production_thread = threading.Thread(
        target=production_loop,
        daemon=True
    )

    production_thread.start()

    # -------------------------------------------------
    # 4. Keep the process alive.
    # -------------------------------------------------

    while True:
        time.sleep(3600)


if __name__ == "__main__":
    start()
