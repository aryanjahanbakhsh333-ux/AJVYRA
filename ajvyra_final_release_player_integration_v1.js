/*
 * AJVYRA — Final Release Player Integration
 * File: ajvyra_final_release_player_integration_v1.js
 *
 * Connects:
 *   Final Anime Catalog
 *        ↓
 *   Anime Cards
 *        ↓
 *   Release Player
 *        ↓
 *   Real MP4 / Poster / Subtitle
 *
 * This file does NOT generate media.
 * It only plays already-released assets.
 */

(function () {
    "use strict";

    const PLAYER_ID = "ajvyra-release-player-v1";
    const STYLE_ID = "ajvyra-release-player-style-v1";

    if (window.__AJVYRA_RELEASE_PLAYER_V1__) {
        return;
    }

    window.__AJVYRA_RELEASE_PLAYER_V1__ = true;

    /*
     * ---------------------------------------------------------
     * 1. CLEAN PREVIOUS PLAYER
     * ---------------------------------------------------------
     */

    const oldPlayer = document.getElementById(PLAYER_ID);

    if (oldPlayer) {
        oldPlayer.remove();
    }

    const oldStyle = document.getElementById(STYLE_ID);

    if (oldStyle) {
        oldStyle.remove();
    }

    /*
     * ---------------------------------------------------------
     * 2. PLAYER STYLE
     * ---------------------------------------------------------
     */

    const style = document.createElement("style");

    style.id = STYLE_ID;

    style.textContent = `
        #${PLAYER_ID} {
            position: fixed;
            inset: 0;
            z-index: 99999;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 18px;
            background: rgba(0,0,0,.94);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
        }

        #${PLAYER_ID}.open {
            display: flex;
        }

        .ajv-player-shell {
            width: min(1180px, 100%);
            max-height: 94vh;
            overflow: auto;
            border: 1px solid rgba(255,255,255,.1);
            background: #080808;
            border-radius: 18px;
            box-shadow: 0 30px 100px rgba(0,0,0,.7);
        }

        .ajv-player-top {
            min-height: 68px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            padding: 12px 16px;
            border-bottom: 1px solid rgba(255,255,255,.07);
        }

        .ajv-player-title-wrap {
            min-width: 0;
        }

        .ajv-player-kicker {
            margin: 0 0 5px;
            color: #777;
            font-size: 9px;
            font-weight: 700;
            letter-spacing: .24em;
            text-transform: uppercase;
        }

        .ajv-player-title {
            margin: 0;
            color: #fff;
            font-size: 18px;
            font-weight: 700;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .ajv-player-close {
            width: 42px;
            height: 42px;
            flex: 0 0 42px;
            border: 1px solid rgba(255,255,255,.1);
            border-radius: 50%;
            background: #111;
            color: #fff;
            cursor: pointer;
            font-size: 18px;
        }

        .ajv-player-video-wrap {
            position: relative;
            background: #000;
        }

        .ajv-player-video {
            width: 100%;
            display: block;
            max-height: 72vh;
            background: #000;
        }

        .ajv-player-info {
            display: grid;
            grid-template-columns: minmax(0, 1fr) auto;
            gap: 20px;
            padding: 18px;
        }

        .ajv-player-description {
            margin: 0;
            color: #888;
            font-size: 13px;
            line-height: 1.7;
        }

        .ajv-player-status {
            color: #666;
            font-size: 11px;
            text-align: right;
        }

        .ajv-player-error {
            display: none;
            padding: 20px;
            color: #aaa;
            border-top: 1px solid rgba(255,255,255,.06);
            background: #0d0d0d;
        }

        .ajv-player-error.show {
            display: block;
        }

        .ajv-player-error strong {
            display: block;
            margin-bottom: 6px;
            color: #fff;
        }

        @media (max-width: 640px) {
            #${PLAYER_ID} {
                padding: 0;
            }

            .ajv-player-shell {
                width: 100%;
                max-height: 100%;
                border-radius: 0;
                border-left: 0;
                border-right: 0;
            }

            .ajv-player-info {
                grid-template-columns: 1fr;
            }

            .ajv-player-status {
                text-align: left;
            }
        }
    `;

    document.head.appendChild(style);

    /*
     * ---------------------------------------------------------
     * 3. PLAYER DOM
     * ---------------------------------------------------------
     */

    const overlay = document.createElement("div");

    overlay.id = PLAYER_ID;
    overlay.setAttribute("aria-hidden", "true");

    const shell = document.createElement("div");

    shell.className = "ajv-player-shell";

    const top = document.createElement("div");

    top.className = "ajv-player-top";

    const titleWrap = document.createElement("div");

    titleWrap.className = "ajv-player-title-wrap";

    const kicker = document.createElement("p");

    kicker.className = "ajv-player-kicker";
    kicker.textContent = "AJVYRA RELEASE";

    const title = document.createElement("h2");

    title.className = "ajv-player-title";
    title.textContent = "Untitled Release";

    titleWrap.appendChild(kicker);
    titleWrap.appendChild(title);

    const closeButton = document.createElement("button");

    closeButton.className = "ajv-player-close";
    closeButton.type = "button";
    closeButton.textContent = "×";
    closeButton.setAttribute(
        "aria-label",
        "Close player"
    );

    top.appendChild(titleWrap);
    top.appendChild(closeButton);

    /*
     * ---------------------------------------------------------
     * VIDEO
     * ---------------------------------------------------------
     */

    const videoWrap = document.createElement("div");

    videoWrap.className = "ajv-player-video-wrap";

    const video = document.createElement("video");

    video.className = "ajv-player-video";
    video.controls = true;
    video.preload = "metadata";
    video.playsInline = true;

    video.setAttribute(
        "aria-label",
        "AJVYRA anime player"
    );

    videoWrap.appendChild(video);

    /*
     * ---------------------------------------------------------
     * INFO
     * ---------------------------------------------------------
     */

    const info = document.createElement("div");

    info.className = "ajv-player-info";

    const description = document.createElement("p");

    description.className = "ajv-player-description";
    description.textContent =
        "AJVYRA cinematic release.";

    const status = document.createElement("div");

    status.className = "ajv-player-status";
    status.textContent = "READY";

    info.appendChild(description);
    info.appendChild(status);

    /*
     * ---------------------------------------------------------
     * ERROR
     * ---------------------------------------------------------
     */

    const errorBox = document.createElement("div");

    errorBox.className = "ajv-player-error";

    const errorTitle = document.createElement("strong");

    errorTitle.textContent =
        "This release could not be played.";

    const errorText = document.createElement("span");

    errorText.textContent =
        "The release URL may be missing, unavailable, or unsupported.";

    errorBox.appendChild(errorTitle);
    errorBox.appendChild(errorText);

    shell.appendChild(top);
    shell.appendChild(videoWrap);
    shell.appendChild(info);
    shell.appendChild(errorBox);

    overlay.appendChild(shell);

    document.body.appendChild(overlay);

    /*
     * ---------------------------------------------------------
     * 4. RELEASE NORMALIZATION
     * ---------------------------------------------------------
     */

    function normalizeRelease(release) {
        if (!release || typeof release !== "object") {
            return null;
        }

        return {
            id:
                release.id ||
                release.slug ||
                release.title ||
                release.name ||
                "",

            title:
                release.title ||
                release.name ||
                "Untitled Release",

            description:
                release.description ||
                release.synopsis ||
                "AJVYRA cinematic release.",

            poster:
                release.poster ||
                release.posterUrl ||
                release.cover ||
                release.coverUrl ||
                "",

            video:
                release.video ||
                release.videoUrl ||
                release.mediaUrl ||
                release.mp4 ||
                release.mp4Url ||
                "",

            subtitle:
                release.subtitle ||
                release.subtitleUrl ||
                release.vtt ||
                release.vttUrl ||
                "",

            type:
                release.type ||
                "anime"
        };
    }

    /*
     * ---------------------------------------------------------
     * 5. OPEN PLAYER
     * ---------------------------------------------------------
     */

    function openRelease(release) {
        const normalized =
            normalizeRelease(release);

        if (!normalized) {
            return false;
        }

        /*
         * Never pretend an asset exists.
         */

        if (!normalized.video) {
            errorBox.classList.add("show");

            status.textContent = "NO VIDEO";

            title.textContent =
                normalized.title;

            description.textContent =
                "This release exists in the catalog, but its final video URL has not been connected yet.";

            overlay.classList.add("open");
            overlay.setAttribute(
                "aria-hidden",
                "false"
            );

            document.body.style.overflow = "hidden";

            return false;
        }

        errorBox.classList.remove("show");

        title.textContent =
            normalized.title;

        description.textContent =
            normalized.description;

        status.textContent =
            "READY";

        /*
         * Poster
         */

        if (normalized.poster) {
            video.poster =
                normalized.poster;
        } else {
            video.removeAttribute("poster");
        }

        /*
         * Clear previous sources
         */

        while (video.firstChild) {
            video.removeChild(video.firstChild);
        }

        /*
         * MP4 source
         */

        const source =
            document.createElement("source");

        source.src =
            normalized.video;

        source.type =
            "video/mp4";

        video.appendChild(source);

        /*
         * Subtitle
         */

        if (normalized.subtitle) {
            const track =
                document.createElement("track");

            track.kind = "subtitles";
            track.label = "Subtitles";
            track.srclang = "fa";
            track.src =
                normalized.subtitle;
            track.default = true;

            video.appendChild(track);
        }

        /*
         * Reload player after changing sources.
         */

        video.load();

        overlay.classList.add("open");

        overlay.setAttribute(
            "aria-hidden",
            "false"
        );

        document.body.style.overflow = "hidden";

        return true;
    }

    /*
     * ---------------------------------------------------------
     * 6. CLOSE PLAYER
     * ---------------------------------------------------------
     */

    function closePlayer() {
        video.pause();

        video.removeAttribute("src");

        while (video.firstChild) {
            video.removeChild(video.firstChild);
        }

        video.load();

        overlay.classList.remove("open");

        overlay.setAttribute(
            "aria-hidden",
            "true"
        );

        document.body.style.overflow = "";

        errorBox.classList.remove("show");

        status.textContent = "READY";
    }

    closeButton.addEventListener(
        "click",
        closePlayer
    );

    /*
     * Clicking outside the player closes it.
     */

    overlay.addEventListener(
        "click",
        function (event) {
            if (event.target === overlay) {
                closePlayer();
            }
        }
    );

    /*
     * Escape closes player.
     */

    document.addEventListener(
        "keydown",
        function (event) {
            if (
                event.key === "Escape" &&
                overlay.classList.contains("open")
            ) {
                closePlayer();
            }
        }
    );

    /*
     * ---------------------------------------------------------
     * 7. VIDEO EVENTS
     * ---------------------------------------------------------
     */

    video.addEventListener(
        "loadstart",
        function () {
            status.textContent =
                "LOADING";
        }
    );

    video.addEventListener(
        "loadedmetadata",
        function () {
            status.textContent =
                "READY";
        }
    );

    video.addEventListener(
        "playing",
        function () {
            status.textContent =
                "PLAYING";
        }
    );

    video.addEventListener(
        "pause",
        function () {
            if (!video.ended) {
                status.textContent =
                    "PAUSED";
            }
        }
    );

    video.addEventListener(
        "ended",
        function () {
            status.textContent =
                "FINISHED";
        }
    );

    video.addEventListener(
        "error",
        function () {
            status.textContent =
                "ERROR";

            errorBox.classList.add("show");
        }
    );

    /*
     * ---------------------------------------------------------
     * 8. CONNECT TO DESIGN SHELL
     * ---------------------------------------------------------
     */

    window.addEventListener(
        "ajvyra:open-release",
        function (event) {
            if (
                event &&
                event.detail
            ) {
                openRelease(event.detail);
            }
        }
    );

    /*
     * ---------------------------------------------------------
     * 9. PUBLIC API
     * ---------------------------------------------------------
     */

    window.AJVYRAReleasePlayer = {
        open: openRelease,
        close: closePlayer,
        isOpen() {
            return overlay.classList.contains(
                "open"
            );
        }
    };

})();
