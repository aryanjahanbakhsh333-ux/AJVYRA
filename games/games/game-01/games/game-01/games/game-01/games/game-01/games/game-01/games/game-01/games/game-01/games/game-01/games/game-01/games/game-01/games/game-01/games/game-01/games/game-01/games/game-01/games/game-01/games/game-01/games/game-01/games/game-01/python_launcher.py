import subprocess
import sys
from pathlib import Path


def launch():

    base = Path(__file__).resolve().parent

    main_file = base / "black_run_main.py"

    subprocess.run(
        [
            sys.executable,
            str(main_file)
        ],
        cwd=str(base)
    )


if __name__ == "__main__":
    launch()
