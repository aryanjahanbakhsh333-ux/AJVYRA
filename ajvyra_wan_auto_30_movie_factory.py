from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from ajvyra_wan_auto_engine import (
    AJVYRAWanAutoEngine,
)

from ajvyra_wan_automatic_film_producer import (
    AJVYRAWAutomaticFilmProducer,
)

from ajvyra_wan_automatic_movie_assembler import (
    AJVYRAWanAutomaticMovieAssembler,
)

from ajvyra_wan_automatic_site_publisher import (
    AJVYRAWanAutomaticSitePublisher,
)


FILMS = [
    ("anime_01", "Veylora"),
    ("anime_02", "Aelvryn"),
    ("anime_03", "Nyxara"),
    ("anime_04", "Kaelith"),
    ("anime_05", "Orivane"),
    ("anime_06", "Zeravia"),
    ("anime_07", "Vaelune"),
    ("anime_08", "Ravelyth"),
    ("anime_09", "Solvarya"),
    ("anime_10", "Xaveren"),
    ("anime_11", "Elyvara"),
    ("anime_12", "Neravelle"),
    ("anime_13", "Vaerith"),
    ("anime_14", "Lunavyr"),
    ("anime_15", "Averlyn"),
    ("anime_16", "Neyvara"),
    ("anime_17", "Elvaria"),
    ("anime_18", "Virelya"),
    ("anime_19", "Caelora"),
    ("anime_20", "Seravyn"),
    ("anime_21", "Mouravia"),
    ("anime_22", "Noxelya"),
    ("anime_23", "Vaelora"),
    ("anime_24", "Eryndra"),
    ("anime_25", "Neylith"),
    ("anime_26", "Auralyne"),
    ("anime_27", "Velmora"),
    ("anime_28", "Seyravia"),
    ("anime_29", "Oryvane"),
    ("anime_30", "Luminarae"),
]


STORIES = {
    "anime_01": (
        "A mysterious young hero discovers a hidden city "
        "beneath a dying sky and must uncover why its light "
        "is disappearing."
    ),
    "anime_02": (
        "A forgotten traveler crosses a frozen kingdom "
        "searching for the person who erased their memories."
    ),
    "anime_03": (
        "A girl connected to the night discovers that her "
        "shadow is protecting the world from an ancient force."
    ),
    "anime_04": (
        "A young warrior returns to a ruined homeland and "
        "must confront the legacy of a vanished civilization."
    ),
    "anime_05": (
        "A quiet wanderer follows mysterious lights across "
        "an endless ocean to find a lost world."
    ),
    "anime_06": (
        "A city built around a forbidden machine begins "
        "to collapse when its true purpose is revealed."
    ),
    "anime_07": (
        "A lonely guardian protects a sleeping moon while "
        "an unknown enemy approaches through the clouds."
    ),
    "anime_08": (
        "Two strangers meet during a supernatural storm "
        "and discover that their pasts are connected."
    ),
    "anime_09": (
        "A young survivor travels through a ruined solar "
        "kingdom searching for the last source of daylight."
    ),
    "anime_10": (
        "A mysterious traveler enters a city where every "
        "memory can be bought and sold."
    ),
    "anime_11": (
        "A girl discovers an abandoned observatory that "
        "contains messages from her future self."
    ),
    "anime_12": (
        "A silent city begins changing every night, forcing "
        "a young explorer to uncover its hidden history."
    ),
    "anime_13": (
        "A fallen knight protects a village from a creature "
        "that only appears when people lose hope."
    ),
    "anime_14": (
        "A dreamer enters a moonlit realm where forgotten "
        "memories become physical places."
    ),
    "anime_15": (
        "A young artist discovers that everything she paints "
        "eventually becomes real."
    ),
    "anime_16": (
        "A traveler searches for a voice that has followed "
        "them through every city they have ever visited."
    ),
    "anime_17": (
        "A hidden kingdom awakens beneath an ordinary town "
        "and chooses an unexpected protector."
    ),
    "anime_18": (
        "A girl trapped between two worlds must decide "
        "which reality she is willing to lose."
    ),
    "anime_19": (
        "A mysterious forest remembers every person who "
        "has ever entered it."
    ),
    "anime_20": (
        "A young pilot discovers an abandoned aircraft "
        "that knows where their missing family disappeared."
    ),
    "anime_21": (
        "A grieving traveler follows a distant melody "
        "through a city that no longer appears on maps."
    ),
    "anime_22": (
        "A boy living beneath a permanent eclipse discovers "
        "a secret hidden inside the darkness."
    ),
    "anime_23": (
        "A forgotten princess returns to a kingdom that "
        "believes she died many years ago."
    ),
    "anime_24": (
        "A scientist finds evidence that the stars above "
        "the world are artificial."
    ),
    "anime_25": (
        "A young fighter protects a mysterious child whose "
        "dreams can change reality."
    ),
    "anime_26": (
        "A singer loses her voice and discovers that the "
        "silence itself is trying to communicate with her."
    ),
    "anime_27": (
        "A traveler enters a city where nobody remembers "
        "their own name."
    ),
    "anime_28": (
        "A young guardian discovers an ancient civilization "
        "beneath a frozen mountain."
    ),
    "anime_29": (
        "A lonely wanderer finds a door that opens into "
        "the moment they most regret."
    ),
    "anime_30": (
        "A final journey begins when a mysterious light "
        "appears above a world preparing for its last night."
    ),
}


CHARACTERS = {
    film_id: (
        "A young anime protagonist with a distinctive "
        "silhouette, expressive eyes, consistent hairstyle "
        "and consistent dark cinematic clothing."
    )
    for film_id, _ in FILMS
}


WORLDS = {
    film_id: (
        "A dark cinematic fantasy world with large-scale "
        "architecture, atmospheric skies, detailed streets, "
        "dramatic weather and deep environmental perspective."
    )
    for film_id, _ in FILMS
}


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--start",
        type=int,
        default=1,
    )

    parser.add_argument(
        "--end",
        type=int,
        default=30,
    )

    parser.add_argument(
        "--resume",
        action="store_true",
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=1800,
    )

    parser.add_argument(
        "--model",
        default=(
            "Wan-AI/"
            "Wan2.1-T2V-1.3B-Diffusers"
        ),
    )

    parser.add_argument(
        "--media-base-url",
        default=os.getenv(
            "AJVYRA_MEDIA_BASE_URL"
        ),
    )

    return parser.parse_args()


def main() -> int:

    args = parse_args()

    if args.start < 1:
        args.start = 1

    if args.end > 30:
        args.end = 30

    if args.start > args.end:

        raise SystemExit(
            "Invalid film range."
        )

    print(
        "======================================"
    )

    print(
        "AJVYRA AUTOMATIC WAN FILM FACTORY"
    )

    print(
        "======================================"
    )

    print(
        f"Films: {args.start} → {args.end}"
    )

    print(
        f"Duration per film: "
        f"{args.duration / 60:.1f} minutes"
    )

    print(
        f"Model: {args.model}"
    )

    print()

    # ---------------------------------------------------------
    # Real Wan engine
    # ---------------------------------------------------------

    engine = (
        AJVYRAWanAutoEngine(
            model_id=args.model,
            device="auto",
            cpu_offload=True,
            dtype="bfloat16",
        )
    )

    producer = (
        AJVYRAWAutomaticFilmProducer(
            engine=engine,
            production_root=(
                "production/wan_films"
            ),
        )
    )

    assembler = (
        AJVYRAWanAutomaticMovieAssembler(
            production_root=(
                "production/wan_films"
            ),
        )
    )

    publisher = (
        AJVYRAWanAutomaticSitePublisher(
            production_root=(
                "production/wan_films"
            ),
            public_root="public",
            media_base_url=(
                args.media_base_url
            ),
        )
    )

    completed = []

    for number in range(
        args.start,
        args.end + 1,
    ):

        film_id, title = FILMS[
            number - 1
        ]

        print()
        print(
            "======================================"
        )
        print(
            f"FILM {number}/30 — {title}"
        )
        print(
            "======================================"
        )

        story = STORIES[
            film_id
        ]

        character = CHARACTERS[
            film_id
        ]

        world = WORLDS[
            film_id
        ]

        state = producer.produce(
            film_id=film_id,
            title=title,
            story=story,
            character_description=character,
            world_description=world,
            duration_seconds=(
                args.duration
            ),
            resume=args.resume,
        )

        if state.status != (
            "SEGMENTS_COMPLETE"
        ):

            print(
                f"[FAILED] {title}"
            )

            print(
                state.error
            )

            continue

        try:

            movie = assembler.assemble(
                film_id
            )

        except Exception as exc:

            print(
                f"[ASSEMBLY FAILED] "
                f"{title}: {exc}"
            )

            continue

        try:

            entry = (
                publisher.publish_movie(
                    film_id,
                    title,
                )
            )

            completed.append(
                entry
            )

            print(
                f"[SITE READY] {title}"
            )

        except Exception as exc:

            print(
                f"[SITE FAILED] "
                f"{title}: {exc}"
            )

    # ---------------------------------------------------------
    # Final catalog
    # ---------------------------------------------------------

    catalog = (
        publisher.build_catalog(
            [
                (film_id, title)
                for film_id, title in FILMS
                if any(
                    item["film_id"]
                    == film_id
                    for item in completed
                )
            ]
        )
    )

    report = {
        "expected_films": 30,
        "processed_range": [
            args.start,
            args.end,
        ],
        "watchable_films": (
            catalog["total_watchable"]
        ),
        "release_ready": (
            catalog["release_ready"]
            and args.start == 1
            and args.end == 30
        ),
        "movies": completed,
    }

    Path(
        "public"
    ).mkdir(
        parents=True,
        exist_ok=True,
    )

    Path(
        "public/"
        "ajvyra_automatic_production_report.json"
    ).write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print(
        "======================================"
    )

    print(
        "PRODUCTION FINISHED"
    )

    print(
        f"Real movies ready: "
        f"{catalog['total_watchable']}/30"
    )

    if report["release_ready"]:

        print(
            "AJVYRA RELEASE: READY"
        )

    else:

        print(
            "AJVYRA RELEASE: BLOCKED"
        )

    print(
        "======================================"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
