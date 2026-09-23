"""
AJVYRA Real Video Asset Validator V1
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


MIN_BYTES = 1024


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--queue",
        required=True
    )

    parser.add_argument(
        "--output-root",
        required=True
    )

    parser.add_argument(
        "--report",
        required=True
    )

    args = parser.parse_args()

    queue = load(
        Path(args.queue)
    )

    root = Path(
        args.output_root
    )

    results = []

    for job in queue["jobs"]:

        file_path = (
            root /
            Path(job["output_file"])
        )

        exists = (
            file_path.exists()
            and file_path.is_file()
        )

        valid = (
            exists
            and file_path.stat().st_size >= MIN_BYTES
        )

        results.append({
            "job_id": job["job_id"],
            "film_id": job["film_id"],
            "film_title": job["film_title"],
            "path": str(file_path),
            "ready": valid
        })

    total = len(results)
    ready = sum(
        item["ready"]
        for item in results
    )

    films = {}

    for item in results:
        films.setdefault(
            item["film_id"],
            {
                "title": item["film_title"],
                "total": 0,
                "ready": 0
            }
        )

        films[item["film_id"]]["total"] += 1

        if item["ready"]:
            films[item["film_id"]]["ready"] += 1

    film_results = []

    for film_id, film in films.items():

        film_ready = (
            film["total"] > 0
            and film["ready"] == film["total"]
        )

        film_results.append({
            "film_id": film_id,
            "title": film["title"],
            "ready": film_ready,
            **film
        })

    all_ready = (
        total > 0
        and ready == total
        and len(film_results) == 30
        and all(
            film["ready"]
            for film in film_results
        )
    )

    report = {
        "project": "AJVYRA",
        "total_shots": total,
        "ready_shots": ready,
        "total_films": len(film_results),
        "all_30_films_ready": all_ready,
        "release_allowed": False,
        "films": film_results,
        "shots": results
    }

    report_path = Path(
        args.report
    )

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"Shots ready: {ready}/{total}"
    )

    print(
        f"Films ready: "
        f"{sum(f['ready'] for f in film_results)}/30"
    )

    if not all_ready:
        raise SystemExit(
            "AJVYRA RELEASE BLOCKED: "
            "30 complete films are not ready."
        )


if __name__ == "__main__":
    main()
