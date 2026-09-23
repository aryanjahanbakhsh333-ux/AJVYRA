from ajvyra_ai_shot_engine_v6 import AJVYRAShotEngine


def prepare():

    engine = AJVYRAShotEngine()

    shots = engine.create_initial_30(
        episode=1,
        story=(
            "In a ruined world where memories disappear every night, "
            "a young traveler searches for the person who remembers him."
        ),
        character=(
            "A fictional young anime protagonist with silver-black hair, "
            "dark coat, calm expression and a distinctive pendant."
        ),
    )

    print(f"AJVYRA: {len(shots)} initial shots prepared.")

    for shot in shots:
        print(
            f"{shot['number']:03d} | "
            f"{shot['genre']} | "
            f"{shot['status']}"
        )


if __name__ == "__main__":
    prepare()
