"""
AJVYRA Anime Player
Mobile-friendly local anime player.

Run:
    python ajvyra_anime_player.py

Open:
    http://127.0.0.1:8765
"""

from __future__ import annotations

import json
import mimetypes
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from ajvyra_anime_studio import ANIME, ROOT, validate_catalog


HOST = "127.0.0.1"
PORT = 8765

BASE_DIR = Path(__file__).resolve().parent
ASSET_ROOT = (BASE_DIR / ROOT).resolve()


HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width,
    initial-scale=1.0,
    maximum-scale=1.0,
    user-scalable=no"
>

<title>AJVYRA Anime</title>

<style>

* {
    box-sizing: border-box;
}

html,
body {
    margin: 0;
    padding: 0;
    background: #07080b;
    color: #ffffff;
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

body {
    min-height: 100vh;
}

header {
    position: sticky;
    top: 0;
    z-index: 20;

    padding: 18px;

    background:
        rgba(7, 8, 11, 0.94);

    backdrop-filter: blur(15px);

    border-bottom:
        1px solid #20232a;
}

.logo {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: 1px;
}

.tagline {
    margin-top: 4px;

    color: #8e949e;

    font-size: 13px;
}

main {
    width: 100%;
    max-width: 1100px;

    margin: auto;

    padding: 15px;
}

.controls {
    display: grid;

    grid-template-columns:
        minmax(0, 1fr)
        170px;

    gap: 9px;

    margin-bottom: 14px;
}

input,
select,
button {

    width: 100%;

    border:
        1px solid #2a2e36;

    border-radius: 11px;

    background: #11141a;

    color: #ffffff;

    padding: 12px;

    font-size: 14px;

    outline: none;
}

button {
    cursor: pointer;
}

button:active {
    transform: scale(0.98);
}

.player {

    width: 100%;

    background: #000000;

    border-radius: 15px;

    overflow: hidden;

    box-shadow:
        0 15px 50px
        rgba(0, 0, 0, 0.45);
}

video {

    display: block;

    width: 100%;

    max-height: 65vh;

    background: #000;
}

.audio-panel {

    display: grid;

    grid-template-columns:
        auto
        minmax(150px, 220px);

    align-items: center;

    gap: 10px;

    margin-top: 10px;

    padding: 12px;

    background: #101319;

    border:
        1px solid #242830;

    border-radius: 12px;
}

.audio-status {

    color: #9298a2;

    font-size: 12px;
}

.info {

    margin-top: 12px;

    padding: 15px;

    border:
        1px solid #252932;

    border-radius: 13px;

    background: #0e1015;
}

.title {

    margin: 0;

    font-size: 21px;
}

.logline {

    color: #b8bdc6;

    line-height: 1.6;

    font-size: 14px;
}

.tags {

    display: flex;

    flex-wrap: wrap;

    gap: 7px;

    margin-top: 9px;
}

.tag {

    padding:
        5px 9px;

    border-radius: 100px;

    background: #1a1e26;

    color: #c8ccd3;

    font-size: 11px;
}

.status {

    margin-top: 10px;

    color: #777e89;

    font-size: 12px;
}

.segments {

    margin-top: 12px;

    padding: 13px;

    border:
        1px solid #252932;

    border-radius: 13px;

    background: #0e1015;
}

.segment-grid {

    display: grid;

    grid-template-columns:
        repeat(
            auto-fill,
            minmax(120px, 1fr)
        );

    gap: 7px;

    margin-top: 10px;
}

.library {

    display: grid;

    grid-template-columns:
        repeat(
            auto-fill,
            minmax(220px, 1fr)
        );

    gap: 10px;

    margin-top: 15px;
}

.anime-card {

    text-align: left;

    padding: 9px;

    transition:
        transform 0.15s ease,
        border-color 0.15s ease;
}

.anime-card:hover {

    border-color: #565d68;
}

.anime-card.active {

    border-color: #8b929d;
}

.poster {

    width: 100%;

    aspect-ratio: 16 / 9;

    margin-bottom: 8px;

    border-radius: 9px;

    overflow: hidden;

    background: #171a21;
}

.poster img {

    width: 100%;

    height: 100%;

    object-fit: cover;
}

.card-title {

    font-weight: 700;

    font-size: 14px;
}

.card-sub {

    margin-top: 3px;

    color: #858b95;

    font-size: 11px;
}

.empty {

    padding: 35px;

    text-align: center;

    color: #777e89;
}

@media (max-width: 650px) {

    .controls {

        grid-template-columns: 1fr;
    }

    .audio-panel {

        grid-template-columns: 1fr;
    }

    .library {

        grid-template-columns:
            repeat(2, minmax(0, 1fr));
    }

}

@media (max-width: 400px) {

    .library {

        grid-template-columns: 1fr;
    }

}

</style>

</head>

<body>

<header>

    <div class="logo">
        AJVYRA
    </div>

    <div class="tagline">
        Anime Universe · 30 Original Episodes
    </div>

</header>


<main>

    <div class="controls">

        <input
            id="search"
            type="search"
            placeholder="Search anime..."
        >

        <select id="genre">

            <option value="">
                All Genres
            </option>

            <option value="Action">
                Action
            </option>

            <option value="Romance">
                Romance
            </option>

            <option value="Sad / Heartbreak">
                Sad / Heartbreak
            </option>

        </select>

    </div>


    <section class="player">

        <video
            id="video"
            controls
            playsinline
            preload="metadata"
        ></video>

    </section>


    <section class="audio-panel">

        <strong>
            Audio
        </strong>

        <select id="audio">

            <option value="fa">
                Persian
            </option>

            <option value="ja">
                Japanese
            </option>

        </select>

        <div
            class="audio-status"
            id="audioStatus"
        >
            Select an anime.
        </div>

        <audio
            id="voice"
            preload="metadata"
        ></audio>

    </section>


    <section class="info">

        <h2
            class="title"
            id="title"
        >
            Choose an anime
        </h2>

        <div
            class="tags"
            id="tags"
        ></div>

        <p
            class="logline"
            id="logline"
        >
            Select an episode from the library below.
        </p>

        <div
            class="status"
            id="assetStatus"
        ></div>

    </section>


    <section class="segments">

        <strong>
            Episode Segments
        </strong>

        <div
            id="segments"
            class="segment-grid"
        ></div>

    </section>


    <section
        id="library"
        class="library"
    ></section>

</main>


<script>

let catalog = [];

let currentAnime = null;


const video =
    document.getElementById("video");

const voice =
    document.getElementById("voice");

const audioSelect =
    document.getElementById("audio");

const audioStatus =
    document.getElementById("audioStatus");

const library =
    document.getElementById("library");

const search =
    document.getElementById("search");

const genre =
    document.getElementById("genre");

const title =
    document.getElementById("title");

const tags =
    document.getElementById("tags");

const logline =
    document.getElementById("logline");

const assetStatus =
    document.getElementById("assetStatus");

const segments =
    document.getElementById("segments");


function escapeHTML(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function formatTime(seconds) {

    const minutes =
        Math.floor(seconds / 60);

    const secs =
        Math.floor(seconds % 60);

    return (
        String(minutes).padStart(2, "0")
        + ":"
        + String(secs).padStart(2, "0")
    );
}


async function loadCatalog() {

    const response =
        await fetch("/api/anime");

    catalog =
        await response.json();

    renderLibrary();
}


function renderLibrary() {

    const query =
        search.value
            .trim()
            .toLowerCase();

    const selectedGenre =
        genre.value;

    const filtered =
        catalog.filter(anime => {

            const text = (
                anime.title
                + " "
                + anime.title_fa
                + " "
                + anime.title_ja
            ).toLowerCase();

            const matchesSearch =
                !query ||
                text.includes(query);

            const matchesGenre =
                !selectedGenre ||
                anime.genre === selectedGenre;

            return (
                matchesSearch &&
                matchesGenre
            );
        });


    library.innerHTML = "";


    if (!filtered.length) {

        library.innerHTML =
            '<div class="empty">No anime found.</div>';

        return;
    }


    filtered.forEach(anime => {

        const button =
            document.createElement("button");

        button.className =
            "anime-card";

        if (
            currentAnime &&
            currentAnime.number === anime.number
        ) {
            button.classList.add("active");
        }


        button.innerHTML = `

            <div class="poster">

                <img
                    loading="lazy"
                    src="/asset/${anime.poster}"
                    alt=""
                >

            </div>

            <div class="card-title">

                #${anime.number}
                ·
                ${escapeHTML(anime.title)}

            </div>

            <div class="card-sub">

                ${escapeHTML(anime.title_fa)}
                ·
                ${escapeHTML(anime.genre)}

            </div>
        `;


        button.onclick = () =>
            selectAnime(anime.number);


        library.appendChild(button);

    });

}


function selectAnime(number) {

    currentAnime =
        catalog.find(
            anime =>
                anime.number === number
        );


    if (!currentAnime) {
        return;
    }


    title.textContent =
        "#" +
        currentAnime.number +
        " · " +
        currentAnime.title;


    logline.textContent =
        currentAnime.logline;


    tags.innerHTML = `

        <span class="tag">
            ${escapeHTML(currentAnime.genre)}
        </span>

        <span class="tag">
            ${escapeHTML(currentAnime.mood)}
        </span>

        <span class="tag">
            ${escapeHTML(currentAnime.title_fa)}
        </span>

        <span class="tag">
            ${escapeHTML(currentAnime.title_ja)}
        </span>

    `;


    assetStatus.textContent =
        "Video: " +
        currentAnime.video +
        " · Persian/Japanese audio · EN/FA/JA subtitles";


    video.src =
        "/asset/" +
        currentAnime.video;


    video.load();


    loadVoice();


    renderSegments();


    renderLibrary();

}


function loadVoice() {

    if (!currentAnime) {
        return;
    }


    const language =
        audioSelect.value;


    const voicePath =
        currentAnime.voice[language];


    if (!voicePath) {

        audioStatus.textContent =
            "Voice track unavailable.";

        voice.removeAttribute("src");

        return;
    }


    voice.src =
        "/asset/" +
        voicePath;


    voice.load();


    audioStatus.textContent =
        language === "fa"
            ? "Persian voice track"
            : "Japanese voice track";

}


function renderSegments() {

    segments.innerHTML = "";


    if (!currentAnime) {
        return;
    }


    currentAnime.segments.forEach(
        (segment, index) => {

            const button =
                document.createElement("button");


            button.innerHTML = `

                Segment ${index + 1}

                <br>

                <small>
                    ${formatTime(segment.start)}
                    -
                    ${formatTime(segment.end)}
                </small>

            `;


            button.onclick = () => {

                video.currentTime =
                    segment.start;

                syncVoice();

                video.play().catch(() => {});

                voice.play().catch(() => {});

            };


            segments.appendChild(button);

        }
    );

}


function syncVoice() {

    if (!voice.src) {
        return;
    }


    try {

        if (
            Math.abs(
                voice.currentTime -
                video.currentTime
            ) > 0.35
        ) {

            voice.currentTime =
                video.currentTime;
        }

    } catch (error) {

        // Ignore temporary media sync errors.

    }

}


audioSelect.addEventListener(
    "change",
    () => {

        const wasPlaying =
            !video.paused;

        loadVoice();

        setTimeout(() => {

            syncVoice();

            if (wasPlaying) {

                voice.play().catch(
                    () => {}
                );

            }

        }, 200);

    }
);


video.addEventListener(
    "play",
    () => {

        syncVoice();

        voice.play().catch(
            () => {}
        );

    }
);


video.addEventListener(
    "pause",
    () => {

        voice.pause();

    }
);


video.addEventListener(
    "seeking",
    () => {

        syncVoice();

    }
);


video.addEventListener(
    "timeupdate",
    () => {

        syncVoice();

    }
);


video.addEventListener(
    "ratechange",
    () => {

        voice.playbackRate =
            video.playbackRate;

    }
);


video.addEventListener(
    "ended",
    () => {

        voice.pause();

    }
);


search.addEventListener(
    "input",
    renderLibrary
);


genre.addEventListener(
    "change",
    renderLibrary
);


loadCatalog().catch(error => {

    console.error(error);

    library.innerHTML =
        '<div class="empty">Unable to load AJVYRA catalog.</div>';

});

</script>

</body>

</html>
"""


def srt_to_vtt(data: bytes) -> bytes:

    text = data.decode(
        "utf-8-sig"
    )

    text = re.sub(
        r"(\d\d:\d\d:\d\d),(\d\d\d)",
        r"\1.\2",
        text
    )

    result = (
        "WEBVTT\n\n"
        + text
    )

    return result.encode("utf-8")


def safe_asset(relative_path: str) -> Path:

    relative =
        Path(unquote(relative_path))

    target =
        (
            ASSET_ROOT / relative
        ).resolve()


    if (
        target != ASSET_ROOT
        and ASSET_ROOT not in target.parents
    ):

        raise PermissionError(
            "Invalid asset path."
        )


    return target


def anime_to_json():

    result = []


    for anime in ANIME:

        result.append({

            "number":
                anime.number,

            "title":
                anime.title,

            "title_fa":
                anime.title_fa,

            "title_ja":
                anime.title_ja,

            "genre":
                anime.genre,

            "mood":
                anime.mood,

            "logline":
                anime.logline,

            "video":
                anime.video,

            "poster":
                anime.poster,

            "voice":
                anime.voice,

            "subtitles":
                anime.subtitles,

            "segments": [

                {
                    "number":
                        segment.number,

                    "start":
                        segment.start,

                    "end":
                        segment.end,

                    "title":
                        segment.title
                }

                for segment
                in anime.segments
            ]

        })


    return result


class AnimeRequestHandler(
    BaseHTTPRequestHandler
):


    def send_bytes(
        self,
        data: bytes,
        content_type: str,
        status=HTTPStatus.OK
    ):

        self.send_response(status)

        self.send_header(
            "Content-Type",
            content_type
        )

        self.send_header(
            "Content-Length",
            str(len(data))
        )

        self.send_header(
            "Cache-Control",
            "no-cache"
        )

        self.end_headers()

        self.wfile.write(data)


    def do_GET(self):

        path =
            urlparse(self.path).path


        try:

            if path == "/":

                return self.send_bytes(
                    HTML.encode("utf-8"),
                    "text/html; charset=utf-8"
                )


            if path == "/api/anime":

                data =
                    json.dumps(
                        anime_to_json(),
                        ensure_ascii=False
                    ).encode("utf-8")


                return self.send_bytes(
                    data,
                    "application/json; charset=utf-8"
                )


            if path == "/api/status":

                valid, errors =
                    validate_catalog()


                data =
                    json.dumps(
                        {
                            "valid": valid,
                            "errors": errors
                        },
                        ensure_ascii=False
                    ).encode("utf-8")


                return self.send_bytes(
                    data,
                    "application/json; charset=utf-8"
                )


            if path.startswith("/asset/"):

                relative =
                    path[len("/asset/"):]


                target =
                    safe_asset(relative)


                if not target.is_file():

                    return self.send_error(
                        HTTPStatus.NOT_FOUND,
                        "Asset not found."
                    )


                content =
                    target.read_bytes()


                content_type =
                    mimetypes.guess_type(
                        target.name
                    )[0]


                if not content_type:

                    content_type =
                        "application/octet-stream"


                return self.send_bytes(
                    content,
                    content_type
                )


            if path.startswith("/subtitle/"):

                relative =
                    path[len("/subtitle/"):]


                target =
                    safe_asset(relative)


                if (
                    target.suffix.lower()
                    != ".srt"
                    or not target.is_file()
                ):

                    return self.send_error(
                        HTTPStatus.NOT_FOUND,
                        "Subtitle not found."
                    )


                vtt =
                    srt_to_vtt(
                        target.read_bytes()
                    )


                return self.send_bytes(
                    vtt,
                    "text/vtt; charset=utf-8"
                )


            return self.send_error(
                HTTPStatus.NOT_FOUND,
                "Not found."
            )


        except PermissionError:

            return self.send_error(
                HTTPStatus.FORBIDDEN,
                "Forbidden."
            )


        except Exception as error:

            return self.send_error(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                str(error)
            )


    def log_message(
        self,
        format_string,
        *args
    ):

        print(
            "[AJVYRA]",
            format_string % args
        )


def main():

    valid, errors =
        validate_catalog()


    if not valid:

        print(
            "AJVYRA anime catalog validation failed:"
        )

        for error in errors:

            print(
                " -",
                error
            )

        raise SystemExit(1)


    print()
    print(
        "======================================"
    )
    print(
        "       AJVYRA ANIME PLAYER"
    )
    print(
        "======================================"
    )
    print()
    print(
        f"Open: http://{HOST}:{PORT}"
    )
    print()
    print(
        "Press Ctrl+C to stop."
    )
    print()


    server =
        ThreadingHTTPServer(
            (HOST, PORT),
            AnimeRequestHandler
        )


    server.serve_forever()


if __name__ == "__main__":

    main()
