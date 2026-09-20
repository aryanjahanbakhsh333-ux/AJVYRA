import sys
from pathlib import Path


def prepare():

    game_directory = Path(
        __file__
    ).resolve().parent

    if str(game_directory) not in sys.path:

        sys.path.insert(
            0,
            str(game_directory)
        )


def verify_python():

    if sys.version_info < (3, 10):

        raise RuntimeError(
            "Black Run requires Python 3.10 or newer."
        )


def boot():

    prepare()
    verify_python()


boot()
