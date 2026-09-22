/*
 * AJVYRA — Final Internal Design Shell
 * Version: 1.0
 *
 * Purpose:
 * Final visual/UI shell for the AJVYRA website.
 *
 * Design:
 * - Pure black / dark luxury
 * - Minimal cinematic interface
 * - Anime + Games platform
 * - Mobile-first
 * - No content generation
 * - Reads already-produced content only
 */

(function () {
    "use strict";

    if (window.__AJVYRA_FINAL_DESIGN_SHELL__) {
        return;
    }

    window.__AJVYRA_FINAL_DESIGN_SHELL__ = true;

    const root = document.createElement("div");

    root.id = "ajvyra-final-shell";

    root.innerHTML = `
        <style>
            #ajvyra-final-shell {
                --aj-bg: #050505;
                --aj-surface: #0b0b0b;
                --aj-surface-2: #111111;
                --aj-border: #1e1e1e;
                --aj-border-soft: #151515;
                --aj-text: #f2f2f2;
                --aj-muted: #888888;
                --aj-soft: #b8b8b8;
                --aj-white: #ffffff;

                min-height: 100vh;
                width: 100%;
                background: var(--aj-bg);
                color: var(--aj-text);
                font-family:
                    Inter,
                    -apple-system,
                    BlinkMacSystemFont,
                    "Segoe UI",
                    sans-serif;

                box-sizing: border-box;
                overflow-x: hidden;
            }

            #ajvyra-final-shell *,
            #ajvyra-final-shell *::before,
            #ajvyra-final-shell *::after {
                box-sizing: border-box;
            }

            #ajvyra-final-shell button,
            #ajvyra-final-shell a,
            #ajvyra-final-shell input {
                font: inherit;
            }

            #ajvyra-final-shell button,
            #ajvyra-final-shell a {
                -webkit-tap-highlight-color: transparent;
            }

            .aj-shell {
                min-height: 100vh;
                background:
                    radial-gradient(
                        circle at 50% -20%,
                        rgba(255,255,255,0.055),
                        transparent 42%
                    ),
                    #050505;
            }

            /* ---------------------------------
               HEADER
            --------------------------------- */

            .aj-header {
                position: sticky;
                top: 0;
                z-index: 100;
                height: 72px;

                display: flex;
                align-items: center;
                justify-content: space-between;

                padding: 0 28px;

                background: rgba(5,5,5,0.92);
                border-bottom: 1px solid var(--aj-border-soft);

                backdrop-filter: blur(18px);
                -webkit-backdrop-filter: blur(18px);
            }

            .aj-brand {
                display: flex;
                align-items: center;
                gap: 12px;

                color: var(--aj-text);
                text-decoration: none;
            }

            .aj-logo {
                width: 42px;
                height: 42px;
                flex: 0 0 42px;

                display: grid;
                place-items: center;

                position: relative;

                border: 1px solid #292929;
                border-radius: 50%;

                background:
                    radial-gradient(
                        circle at 50% 45%,
                        #242424 0,
                        #0c0c0c 62%,
                        #050505 100%
                    );

                overflow: hidden;
            }

            /*
             * Symbolic black fox.
             * Kept vector/CSS-based so the shell does not depend
             * on a missing external image.
             */
            .aj-logo::before {
                content: "";
                width: 23px;
                height: 19px;

                background: #050505;

                clip-path: polygon(
                    0 22%,
                    25% 0,
                    39% 16%,
                    61% 16%,
                    75% 0,
                    100% 22%,
                    91% 80%,
                    72% 100%,
                    28% 100%,
                    9% 80%
                );

                border: 1px solid #555;
            }

            .aj-logo::after {
                content: "AJ";

                position: absolute;
                left: 50%;
                top: 2px;

                transform: translateX(-50%);

                font-size: 6px;
                font-weight: 800;
                letter-spacing: 0.08em;

                color: #bdbdbd;
            }

            .aj-brand-name {
                font-size: 15px;
                font-weight: 700;
                letter-spacing: 0.18em;
            }

            .aj-nav {
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .aj-nav-button {
                min-height: 40px;
                padding: 0 14px;

                border: 1px solid transparent;
                border-radius: 10px;

                background: transparent;
                color: var(--aj-muted);

                cursor: pointer;
                transition:
                    color 160ms ease,
                    background 160ms ease,
                    border-color 160ms ease;
            }

            .aj-nav-button:hover,
            .aj-nav-button:focus-visible {
                color: var(--aj-text);
                background: #101010;
                border-color: #222;
                outline: none;
            }

            .aj-nav-button.active {
                color: var(--aj-text);
            }

            .aj-menu-button {
                display: none;

                width: 44px;
                height: 44px;

                border: 1px solid #222;
                border-radius: 10px;

                background: #0b0b0b;
                color: white;

                cursor: pointer;
            }

            /* ---------------------------------
               MAIN
            --------------------------------- */

            .aj-main {
                width: min(1400px, 100%);
                margin: 0 auto;
                padding: 0 28px 80px;
            }

            .aj-hero {
                min-height: 520px;

                display: flex;
                align-items: flex-end;

                padding: 80px 0 64px;

                position: relative;
                isolation: isolate;
            }

            .aj-hero::before {
                content: "";

                position: absolute;
                inset: 0;

                z-index: -2;

                background:
                    linear-gradient(
                        180deg,
                        transparent 20%,
                        rgba(5,5,5,0.7) 70%,
                        #050505 100%
                    ),
                    radial-gradient(
                        ellipse at 65% 35%,
                        rgba(255,255,255,0.09),
                        transparent 38%
                    );
            }

            .aj-hero-content {
                max-width: 720px;
            }

            .aj-kicker {
                color: #858585;
                font-size: 12px;
                letter-spacing: 0.28em;
                text-transform: uppercase;
                margin-bottom: 16px;
            }

            .aj-title {
                margin: 0;

                font-size: clamp(
                    42px,
                    8vw,
                    88px
                );

                line-height: 0.95;
                letter-spacing: -0.055em;
                font-weight: 800;
            }

            .aj-description {
                max-width: 590px;

                margin: 24px 0 0;

                color: var(--aj-soft);

                font-size: 16px;
                line-height: 1.7;
            }

            .aj-actions {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;

                margin-top: 30px;
            }

            .aj-primary,
            .aj-secondary {
                min-height: 48px;
                padding: 0 22px;

                border-radius: 12px;

                cursor: pointer;

                font-weight: 700;

                transition:
                    transform 160ms ease,
                    background 160ms ease,
                    border-color 160ms ease;
            }

            .aj-primary {
                background: white;
                color: black;
                border: 1px solid white;
            }

            .aj-secondary {
                background: #0d0d0d;
                color: white;
                border: 1px solid #292929;
            }

            .aj-primary:hover,
            .aj-secondary:hover {
                transform: translateY(-1px);
            }

            .aj-primary:focus-visible,
            .aj-secondary:focus-visible {
                outline: 2px solid white;
                outline-offset: 3px;
            }

            /* ---------------------------------
               SECTIONS
            --------------------------------- */

            .aj-section {
                margin-top: 54px;
            }

            .aj-section-head {
                display: flex;
                align-items: flex-end;
                justify-content: space-between;
                gap: 20px;

                margin-bottom: 18px;
            }

            .aj-section-title {
                margin: 0;

                font-size: 22px;
                letter-spacing: -0.02em;
            }

            .aj-section-subtitle {
                margin: 6px 0 0;

                color: var(--aj-muted);
                font-size: 13px;
            }

            .aj-view-all {
                border: 0;
                background: transparent;
                color: #999;
                cursor: pointer;
                padding: 8px;
            }

            .aj-view-all:hover {
                color: white;
            }

            /* ---------------------------------
               CARDS
            --------------------------------- */

            .aj-grid {
                display: grid;

                grid-template-columns:
                    repeat(
                        5,
                        minmax(0, 1fr)
                    );

                gap: 14px;
            }

            .aj-card {
                min-width: 0;

                position: relative;

                overflow: hidden;

                border: 1px solid #191919;
                border-radius: 15px;

                background: #090909;

                cursor: pointer;

                transition:
                    transform 180ms ease,
                    border-color 180ms ease,
                    background 180ms ease;
            }

            .aj-card:hover {
                transform: translateY(-3px);
                border-color: #343434;
                background: #0d0d0d;
            }

            .aj-poster {
                aspect-ratio: 2 / 3;

                display: grid;
                place-items: center;

                position: relative;

                background:
                    linear-gradient(
                        145deg,
                        #171717,
                        #080808 65%,
                        #111
                    );

                overflow: hidden;
            }

            .aj-poster::before {
                content: "";

                position: absolute;
                width: 70%;
                height: 70%;

                border-radius: 50%;

                background:
                    radial-gradient(
                        circle,
                        rgba(255,255,255,0.12),
                        transparent 65%
                    );

                filter: blur(10px);
            }

            .aj-poster-mark {
                position: relative;

                font-size: 11px;
                font-weight: 800;

                letter-spacing: 0.24em;

                color: #999;
            }

            .aj-card-body {
                padding: 13px;
            }

            .aj-card-title {
                margin: 0;

                font-size: 14px;
                font-weight: 700;

                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }

            .aj-card-meta {
                margin-top: 6px;

                color: #666;

                font-size: 11px;
            }

            /* ---------------------------------
               FEATURED PLAYER
            --------------------------------- */

            .aj-player {
                display: none;

                margin-top: 22px;

                border: 1px solid #242424;
                border-radius: 16px;

                overflow: hidden;

                background: #000;
            }

            .aj-player.open {
                display: block;
            }

            .aj-video {
                display: block;

                width: 100%;
                max-height: 720px;

                background: #000;
            }

            .aj-player-info {
                padding: 18px;
            }

            .aj-player-title {
                margin: 0;
                font-size: 20px;
            }

            .aj-player-status {
                margin-top: 6px;
                color: #777;
                font-size: 12px;
            }

            /* ---------------------------------
               SEARCH
            --------------------------------- */

            .aj-search {
                width: 100%;

                min-height: 50px;

                padding: 0 16px;

                border: 1px solid #252525;
                border-radius: 12px;

                outline: none;

                background: #090909;
                color: white;
            }

            .aj-search::placeholder {
                color: #555;
            }

            .aj-search:focus {
                border-color: #444;
            }

            /* ---------------------------------
               FOOTER
            --------------------------------- */

            .aj-footer {
                margin-top: 90px;

                padding: 30px 0;

                border-top: 1px solid #151515;

                color: #555;

                font-size: 12px;
            }

            .aj-footer-row {
                display: flex;
                align-items: center;
                justify-content: space-between;

                gap: 20px;
            }

            /* ---------------------------------
               MOBILE
            --------------------------------- */

            @media (max-width: 1050px) {
                .aj-grid {
                    grid-template-columns:
                        repeat(
                            4,
                            minmax(0, 1fr)
                        );
                }
            }

            @media (max-width: 780px) {
                .aj-header {
                    padding: 0 16px;
                }

                .aj-nav {
                    display: none;

                    position: absolute;

                    top: 72px;
                    left: 12px;
                    right: 12px;

                    padding: 10px;

                    flex-direction: column;
                    align-items: stretch;

                    background: #090909;

                    border: 1px solid #222;
                    border-radius: 14px;
                }

                .aj-nav.open {
                    display: flex;
                }

                .aj-nav-button {
                    width: 100%;
                    text-align: left;
                }

                .aj-menu-button {
                    display: block;
                }

                .aj-main {
                    padding-left: 16px;
                    padding-right: 16px;
                }

                .aj-hero {
                    min-height: 480px;
                    padding-top: 60px;
                }

                .aj-grid {
                    grid-template-columns:
                        repeat(
                            2,
                            minmax(0, 1fr)
                        );
                }
            }

            @media (max-width: 420px) {
                .aj-brand-name {
                    font-size: 13px;
                }

                .aj-title {
                    font-size: 43px;
                }

                .aj-description {
                    font-size: 14px;
                }

                .aj-grid {
                    gap: 10px;
                }

                .aj-card-body {
                    padding: 10px;
                }

                .aj-card-title {
                    font-size: 13px;
                }

                .aj-footer-row {
                    flex-direction: column;
                    align-items: flex-start;
                }
            }

            @media (prefers-reduced-motion: reduce) {
                #ajvyra-final-shell *,
                #ajvyra-final-shell *::before,
                #ajvyra-final-shell *::after {
                    scroll-behavior: auto !important;
                    transition-duration: 0.01ms !important;
                    animation-duration: 0.01ms !important;
                }
            }
        </style>

        <div class="aj-shell">

            <header class="aj-header">

                <a
                    href="#home"
                    class="aj-brand"
                    aria-label="AJVYRA Home"
                >
                    <span
                        class="aj-logo"
                        aria-hidden="true"
                    ></span>

                    <span class="aj-brand-name">
                        AJVYRA
                    </span>
                </a>

                <nav
                    class="aj-nav"
                    id="aj-main-nav"
                    aria-label="Main navigation"
                >
                    <button
                        type="button"
                        class="aj-nav-button active"
                        data-page="home"
                    >
                        Home
                    </button>

                    <button
                        type="button"
                        class="aj-nav-button"
                        data-page="anime"
                    >
                        Anime
                    </button>

                    <button
                        type="button"
                        class="aj-nav-button"
                        data-page="games"
                    >
                        Games
                    </button>

                    <button
                        type="button"
                        class="aj-nav-button"
                        data-page="library"
                    >
                        Library
                    </button>
                </nav>

                <button
                    type="button"
                    class="aj-menu-button"
                    id="aj-menu-button"
                    aria-expanded="false"
                    aria-controls="aj-main-nav"
                    aria-label="Open menu"
                >
                    ☰
                </button>

            </header>

            <main class="aj-main">

                <section
                    class="aj-hero"
                    id="home"
                    aria-labelledby="aj-hero-title"
                >
                    <div class="aj-hero-content">

                        <div class="aj-kicker">
                            AJVYRA ORIGINAL
                        </div>

                        <h1
                            class="aj-title"
                            id="aj-hero-title"
                        >
                            DARK WORLDS.
                            <br>
                            NEW STORIES.
                        </h1>

                        <p class="aj-description">
                            An independent universe of cinematic
                            anime and playable worlds.
                            Enter the world of AJVYRA.
                        </p>

                        <div class="aj-actions">

                            <button
                                type="button"
                                class="aj-primary"
                                data-action="anime"
                            >
                                Explore Anime
                            </button>

                            <button
                                type="button"
                                class="aj-secondary"
                                data-action="games"
                            >
                                Play Games
                            </button>

                        </div>

                    </div>
                </section>

                <section
                    class="aj-section"
                    id="anime"
                    aria-labelledby="aj-anime-heading"
                >

                    <div class="aj-section-head">

                        <div>
                            <h2
                                class="aj-section-title"
                                id="aj-anime-heading"
                            >
                                Anime
                            </h2>

                            <p class="aj-section-subtitle">
                                Original cinematic stories
                            </p>
                        </div>

                        <button
                            type="button"
                            class="aj-view-all"
                            data-action="anime"
                        >
                            View all
                        </button>

                    </div>

                    <div
                        class="aj-grid"
                        id="aj-anime-grid"
                    ></div>

                    <div
                        class="aj-player"
                        id="aj-anime-player"
                    >

                        <video
                            class="aj-video"
                            id="aj-video"
                            controls
                            playsinline
                            preload="metadata"
                        ></video>

                        <div class="aj-player-info">

                            <h3
                                class="aj-player-title"
                                id="aj-player-title"
                            >
                                —
                            </h3>

                            <div
                                class="aj-player-status"
                                id="aj-player-status"
                            >
                                Ready
                            </div>

                        </div>

                    </div>

                </section>

                <section
                    class="aj-section"
                    id="games"
                    aria-labelledby="aj-games-heading"
                >

                    <div class="aj-section-head">

                        <div>
                            <h2
                                class="aj-section-title"
                                id="aj-games-heading"
                            >
                                Games
                            </h2>

                            <p class="aj-section-subtitle">
                                Playable worlds
                            </p>
                        </div>

                        <button
                            type="button"
                            class="aj-view-all"
                            data-action="games"
                        >
                            View all
                        </button>

                    </div>

                    <div
                        class="aj-grid"
                        id="aj-games-grid"
                    ></div>

                </section>

                <section
                    class="aj-section"
                    aria-labelledby="aj-search-heading"
                >

                    <div class="aj-section-head">

                        <div>
                            <h2
                                class="aj-section-title"
                                id="aj-search-heading"
                            >
                                Discover
                            </h2>

                            <p class="aj-section-subtitle">
                                Search the AJVYRA universe
                            </p>
                        </div>

                    </div>

                    <input
                        id="aj-search"
                        class="aj-search"
                        type="search"
                        placeholder="Search anime or games..."
                        aria-label="Search AJVYRA"
                    />

                </section>

                <footer class="aj-footer">

                    <div class="aj-footer-row">

                        <span>
                            © AJVYRA
                        </span>

                        <span>
                            DARK WORLDS. NEW STORIES.
                        </span>

                    </div>

                </footer>

            </main>

        </div>
    `;

    document.body.appendChild(root);

    const nav = root.querySelector("#aj-main-nav");
    const menuButton = root.querySelector("#aj-menu-button");

    const animeGrid = root.querySelector("#aj-anime-grid");
    const gamesGrid = root.querySelector("#aj-games-grid");

    const player = root.querySelector("#aj-anime-player");
    const video = root.querySelector("#aj-video");
    const playerTitle = root.querySelector("#aj-player-title");
    const playerStatus = root.querySelector("#aj-player-status");

    const searchInput = root.querySelector("#aj-search");

    const animeFallback = [
        "Veylora",
        "Aelvryn",
        "Nyxara",
        "Kaelith",
        "Orivane"
    ];

    const gameFallback = [
        "Shadow Runner",
        "Neon Drift",
        "Void Arena",
        "Lost Realm",
        "Night Hunt"
    ];

    function getAnimeCatalog() {
        const catalog =
            window.AJVYRA_ANIME_CATALOG ||
            window.ajvyraAnimeCatalog ||
            [];

        return Array.isArray(catalog)
            ? catalog
            : [];
    }

    function getGameCatalog() {
        const catalog =
            window.AJVYRA_GAME_CATALOG ||
            window.ajvyraGameCatalog ||
            [];

        return Array.isArray(catalog)
            ? catalog
            : [];
    }

    function normalizeAnime(item, index) {
        if (typeof item === "string") {
            return {
                id: item.toLowerCase(),
                title: item,
                video: ""
            };
        }

        return {
            id: item?.id || `anime-${index}`,
            title: item?.title || "Untitled Anime",
            video: item?.video || item?.videoUrl || ""
        };
    }

    function normalizeGame(item, index) {
        if (typeof item === "string") {
            return {
                id: item.toLowerCase(),
                title: item
            };
        }

        return {
            id: item?.id || `game-${index}`,
            title: item?.title || "Untitled Game"
        };
    }

    function createCard(item, type) {
        const card = document.createElement("article");

        card.className = "aj-card";
        card.tabIndex = 0;

        card.innerHTML = `
            <div class="aj-poster">
                <span class="aj-poster-mark">
                    ${type === "anime" ? "AJVYRA ANIME" : "AJVYRA GAME"}
                </span>
            </div>

            <div class="aj-card-body">

                <h3 class="aj-card-title"></h3>

                <div class="aj-card-meta">
                    ${type === "anime" ? "Cinematic Original" : "Playable World"}
                </div>

            </div>
        `;

        card.querySelector(".aj-card-title").textContent =
            item.title;

        function activate() {
            if (type === "anime") {
                openAnime(item);
            } else {
                window.dispatchEvent(
                    new CustomEvent(
                        "ajvyra:game-open",
                        {
                            detail: item
                        }
                    )
                );
            }
        }

        card.addEventListener(
            "click",
            activate
        );

        card.addEventListener(
            "keydown",
            (event) => {
                if (
                    event.key === "Enter" ||
                    event.key === " "
                ) {
                    event.preventDefault();
                    activate();
                }
            }
        );

        return card;
    }

    function renderAnime() {

        animeGrid.innerHTML = "";

        let catalog = getAnimeCatalog()
            .map(normalizeAnime);

        /*
         * These fallback cards are deliberately not presented
         * as playable/generated assets. They are only used to
         * keep the visual shell visible before the final catalog
         * is connected.
         */

        if (!catalog.length) {
            catalog = animeFallback.map(
                normalizeAnime
            );
        }

        catalog
            .slice(0, 10)
            .forEach(
                (item) => {
                    animeGrid.appendChild(
                        createCard(
                            item,
                            "anime"
                        )
                    );
                }
            );
    }

    function renderGames() {

        gamesGrid.innerHTML = "";

        let catalog = getGameCatalog()
            .map(normalizeGame);

        if (!catalog.length) {
            catalog = gameFallback.map(
                normalizeGame
            );
        }

        catalog
            .slice(0, 10)
            .forEach(
                (item) => {
                    gamesGrid.appendChild(
                        createCard(
                            item,
                            "game"
                        )
                    );
                }
            );
    }

    function openAnime(item) {

        if (!item.video) {
            player.classList.add("open");

            playerTitle.textContent =
                item.title;

            playerStatus.textContent =
                "Video asset is not connected yet.";

            video.removeAttribute("src");
            video.load();

            return;
        }

        player.classList.add("open");

        playerTitle.textContent =
            item.title;

        playerStatus.textContent =
            "Ready to play.";

        video.src = item.video;
        video.load();

        player.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }

    function navigate(page) {

        nav
            .querySelectorAll(".aj-nav-button")
            .forEach(
                (button) => {
                    button.classList.toggle(
                        "active",
                        button.dataset.page === page
                    );
                }
            );

        const target =
            root.querySelector(
                `#${page}`
            );

        if (target) {
            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        }

        nav.classList.remove("open");
        menuButton.setAttribute(
            "aria-expanded",
            "false"
        );
    }

    menuButton.addEventListener(
        "click",
        () => {

            const open =
                nav.classList.toggle("open");

            menuButton.setAttribute(
                "aria-expanded",
                String(open)
            );
        }
    );

    nav
        .querySelectorAll(".aj-nav-button")
        .forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    () => {
                        navigate(
                            button.dataset.page
                        );
                    }
                );

            }
        );

    root
        .querySelectorAll(
            "[data-action]"
        )
        .forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    () => {
                        navigate(
                            button.dataset.action
                        );
                    }
                );

            }
        );

    searchInput.addEventListener(
        "input",
        () => {

            const query =
                searchInput.value
                    .trim()
                    .toLowerCase();

            root
                .querySelectorAll(".aj-card")
                .forEach(
                    (card) => {

                        const title =
                            card
                                .querySelector(
                                    ".aj-card-title"
                                )
                                .textContent
                                .toLowerCase();

                        card.style.display =
                            !query ||
                            title.includes(query)
                                ? ""
                                : "none";
                    }
                );
        }
    );

    renderAnime();
    renderGames();

    window.AJVYRAFinalDesignShell = {
        root,
        renderAnime,
        renderGames,
        openAnime,
        navigate
    };

})();
