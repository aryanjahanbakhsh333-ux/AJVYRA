/*
 * AJVYRA — Final Brand Identity + Internal UI
 * File: ajvyra_final_brand_identity_ui_v2.js
 *
 * Purpose:
 * - Final dark/luxury internal design layer
 * - Real inline SVG AJVYRA fox logo
 * - Black fox head + luxury bucket hat + AJ
 * - Mobile-first responsive layout
 * - Anime / Games / Library / Search structure
 * - Integrates with existing AJVYRA catalogs when available
 *
 * IMPORTANT:
 * This file does NOT generate anime, games, or media.
 * It only presents already-produced release assets.
 */

(function () {
    "use strict";

    if (window.__AJVYRA_FINAL_BRAND_UI_V2__) {
        return;
    }

    window.__AJVYRA_FINAL_BRAND_UI_V2__ = true;

    const ROOT_ID = "ajvyra-final-brand-ui-v2";
    const STYLE_ID = "ajvyra-final-brand-style-v2";

    /*
     * ---------------------------------------------------------
     * 1. CLEAN OLD FINAL SHELL
     * ---------------------------------------------------------
     */

    const previousShell = document.getElementById("ajvyra-final-shell");

    if (previousShell) {
        previousShell.remove();
    }

    const previousBrandRoot = document.getElementById(ROOT_ID);

    if (previousBrandRoot) {
        previousBrandRoot.remove();
    }

    const previousStyle = document.getElementById(STYLE_ID);

    if (previousStyle) {
        previousStyle.remove();
    }

    /*
     * ---------------------------------------------------------
     * 2. GLOBAL STYLE
     * ---------------------------------------------------------
     */

    const style = document.createElement("style");

    style.id = STYLE_ID;

    style.textContent = `
        :root {
            --aj-black: #030303;
            --aj-black-2: #080808;
            --aj-black-3: #0d0d0d;
            --aj-surface: #111111;
            --aj-surface-2: #151515;
            --aj-border: rgba(255,255,255,.09);
            --aj-border-soft: rgba(255,255,255,.055);
            --aj-text: #f5f5f5;
            --aj-muted: #8d8d8d;
            --aj-dim: #555;
            --aj-white: #ffffff;
            --aj-gold: #c9a86a;
        }

        #${ROOT_ID} {
            min-height: 100vh;
            width: 100%;
            background:
                radial-gradient(
                    circle at 50% -10%,
                    rgba(255,255,255,.045),
                    transparent 34%
                ),
                var(--aj-black);
            color: var(--aj-text);
            font-family:
                Inter,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
            letter-spacing: .01em;
            overflow-x: hidden;
        }

        #${ROOT_ID} *,
        #${ROOT_ID} *::before,
        #${ROOT_ID} *::after {
            box-sizing: border-box;
        }

        #${ROOT_ID} button,
        #${ROOT_ID} input {
            font: inherit;
        }

        .ajv-shell {
            width: min(1440px, 100%);
            margin: 0 auto;
            padding: 0 28px;
        }

        /*
         * HEADER
         */

        .ajv-header {
            position: sticky;
            top: 0;
            z-index: 1000;
            height: 78px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
            padding: 0 28px;
            background: rgba(3,3,3,.88);
            border-bottom: 1px solid var(--aj-border-soft);
            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);
        }

        .ajv-brand {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            min-width: 0;
            color: var(--aj-white);
            text-decoration: none;
        }

        .aj-logo {
            width: 48px;
            height: 48px;
            flex: 0 0 48px;
            display: block;
        }

        .aj-brand-word {
            display: flex;
            flex-direction: column;
            line-height: 1;
        }

        .aj-brand-name {
            font-size: 15px;
            font-weight: 700;
            letter-spacing: .24em;
        }

        .aj-brand-sub {
            margin-top: 6px;
            color: var(--aj-dim);
            font-size: 8px;
            letter-spacing: .28em;
            text-transform: uppercase;
        }

        .aj-nav {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .aj-nav-btn {
            appearance: none;
            border: 0;
            background: transparent;
            color: var(--aj-muted);
            min-height: 42px;
            padding: 0 14px;
            border-radius: 999px;
            cursor: pointer;
            transition:
                background .2s ease,
                color .2s ease;
        }

        .aj-nav-btn:hover,
        .aj-nav-btn.active {
            background: rgba(255,255,255,.07);
            color: var(--aj-white);
        }

        .aj-header-actions {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .aj-icon-btn {
            width: 42px;
            height: 42px;
            display: grid;
            place-items: center;
            border: 1px solid var(--aj-border);
            border-radius: 50%;
            background: rgba(255,255,255,.025);
            color: var(--aj-white);
            cursor: pointer;
            transition:
                background .2s ease,
                border-color .2s ease;
        }

        .aj-icon-btn:hover {
            background: rgba(255,255,255,.08);
            border-color: rgba(255,255,255,.18);
        }

        /*
         * HERO
         */

        .ajv-hero {
            position: relative;
            min-height: 600px;
            display: flex;
            align-items: flex-end;
            padding: 100px 0 82px;
            overflow: hidden;
        }

        .ajv-hero::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(
                    90deg,
                    rgba(3,3,3,.98) 0%,
                    rgba(3,3,3,.82) 42%,
                    rgba(3,3,3,.25) 100%
                ),
                radial-gradient(
                    circle at 75% 40%,
                    rgba(255,255,255,.07),
                    transparent 34%
                );
            pointer-events: none;
        }

        .ajv-hero-inner {
            position: relative;
            z-index: 2;
            width: min(760px, 100%);
        }

        .ajv-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 24px;
            color: var(--aj-muted);
            font-size: 11px;
            font-weight: 600;
            letter-spacing: .28em;
            text-transform: uppercase;
        }

        .ajv-eyebrow::before {
            content: "";
            width: 26px;
            height: 1px;
            background: var(--aj-gold);
        }

        .ajv-title {
            margin: 0;
            max-width: 760px;
            font-size: clamp(48px, 8vw, 104px);
            line-height: .88;
            letter-spacing: -.055em;
            font-weight: 800;
        }

        .ajv-title span {
            color: #666;
        }

        .ajv-description {
            max-width: 560px;
            margin: 28px 0 0;
            color: #a0a0a0;
            font-size: 15px;
            line-height: 1.8;
        }

        .ajv-hero-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 32px;
        }

        .ajv-primary,
        .ajv-secondary {
            min-height: 48px;
            padding: 0 22px;
            border-radius: 999px;
            cursor: pointer;
            transition:
                transform .2s ease,
                background .2s ease,
                border-color .2s ease;
        }

        .ajv-primary {
            border: 1px solid #fff;
            background: #fff;
            color: #000;
            font-weight: 700;
        }

        .ajv-secondary {
            border: 1px solid var(--aj-border);
            background: rgba(255,255,255,.025);
            color: #fff;
        }

        .ajv-primary:hover,
        .ajv-secondary:hover {
            transform: translateY(-1px);
        }

        /*
         * CONTENT
         */

        .ajv-section {
            padding: 72px 0;
        }

        .ajv-section-header {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 20px;
            margin-bottom: 26px;
        }

        .ajv-section-kicker {
            margin: 0 0 8px;
            color: var(--aj-gold);
            font-size: 9px;
            letter-spacing: .3em;
            text-transform: uppercase;
        }

        .ajv-section-title {
            margin: 0;
            font-size: clamp(28px, 4vw, 46px);
            letter-spacing: -.035em;
        }

        .ajv-section-note {
            color: var(--aj-muted);
            font-size: 13px;
        }

        /*
         * CARDS
         */

        .ajv-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 16px;
        }

        .ajv-card {
            position: relative;
            min-width: 0;
            border: 1px solid var(--aj-border-soft);
            background: var(--aj-surface);
            overflow: hidden;
            cursor: pointer;
            transition:
                transform .25s ease,
                border-color .25s ease,
                background .25s ease;
        }

        .ajv-card:hover {
            transform: translateY(-4px);
            border-color: rgba(255,255,255,.18);
            background: var(--aj-surface-2);
        }

        .ajv-poster {
            position: relative;
            aspect-ratio: 2 / 3;
            background:
                linear-gradient(
                    145deg,
                    #181818,
                    #050505
                );
            overflow: hidden;
        }

        .ajv-poster::after {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(
                    180deg,
                    transparent 50%,
                    rgba(0,0,0,.8)
                );
        }

        .ajv-poster img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }

        .ajv-card-body {
            padding: 17px;
        }

        .ajv-card-title {
            margin: 0;
            color: #fff;
            font-size: 15px;
            font-weight: 700;
        }

        .ajv-card-meta {
            margin-top: 7px;
            color: var(--aj-muted);
            font-size: 11px;
        }

        .ajv-empty {
            grid-column: 1 / -1;
            padding: 70px 20px;
            border: 1px dashed var(--aj-border);
            color: var(--aj-muted);
            text-align: center;
        }

        /*
         * SEARCH
         */

        .ajv-search-panel {
            display: none;
            padding: 20px 28px;
            border-bottom: 1px solid var(--aj-border-soft);
            background: #060606;
        }

        .ajv-search-panel.open {
            display: block;
        }

        .ajv-search-input {
            width: 100%;
            max-width: 700px;
            height: 48px;
            border: 1px solid var(--aj-border);
            border-radius: 12px;
            outline: none;
            background: #101010;
            color: #fff;
            padding: 0 16px;
        }

        .ajv-search-input:focus {
            border-color: rgba(255,255,255,.28);
        }

        /*
         * FOOTER
         */

        .ajv-footer {
            padding: 70px 0 35px;
            border-top: 1px solid var(--aj-border-soft);
        }

        .ajv-footer-inner {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
        }

        .ajv-footer-brand {
            color: #fff;
            font-size: 12px;
            letter-spacing: .22em;
            font-weight: 700;
        }

        .ajv-footer-copy {
            color: #555;
            font-size: 11px;
        }

        /*
         * MOBILE
         */

        @media (max-width: 900px) {
            .ajv-nav {
                display: none;
            }

            .ajv-grid {
                grid-template-columns: repeat(3, minmax(0, 1fr));
            }

            .ajv-hero {
                min-height: 560px;
            }
        }

        @media (max-width: 640px) {
            .ajv-shell {
                padding: 0 16px;
            }

            .ajv-header {
                height: 68px;
                padding: 0 16px;
            }

            .aj-logo {
                width: 42px;
                height: 42px;
                flex-basis: 42px;
            }

            .aj-brand-sub {
                display: none;
            }

            .aj-brand-name {
                font-size: 12px;
            }

            .ajv-hero {
                min-height: 540px;
                padding: 85px 0 58px;
            }

            .ajv-title {
                font-size: clamp(48px, 15vw, 78px);
            }

            .ajv-description {
                font-size: 14px;
            }

            .ajv-section {
                padding: 54px 0;
            }

            .ajv-section-header {
                align-items: flex-start;
                flex-direction: column;
            }

            .ajv-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 10px;
            }

            .ajv-card-body {
                padding: 13px;
            }

            .ajv-card-title {
                font-size: 13px;
            }

            .ajv-footer-inner {
                align-items: flex-start;
                flex-direction: column;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            #${ROOT_ID} *,
            #${ROOT_ID} *::before,
            #${ROOT_ID} *::after {
                scroll-behavior: auto !important;
                transition: none !important;
            }
        }
    `;

    document.head.appendChild(style);

    /*
     * ---------------------------------------------------------
     * 3. SVG LOGO
     * ---------------------------------------------------------
     *
     * Actual vector logo:
     * - Black fox head
     * - Luxury bucket hat
     * - AJ on hat
     */

    function createFoxLogo(size = 64) {
        const SVG_NS = "http://www.w3.org/2000/svg";

        const svg = document.createElementNS(SVG_NS, "svg");

        svg.setAttribute("viewBox", "0 0 220 220");
        svg.setAttribute("width", String(size));
        svg.setAttribute("height", String(size));
        svg.setAttribute("role", "img");
        svg.setAttribute("aria-label", "AJVYRA black fox logo");

        const title = document.createElementNS(SVG_NS, "title");
        title.textContent = "AJVYRA Black Fox";

        svg.appendChild(title);

        /*
         * Hat shadow
         */
        const hatShadow = document.createElementNS(SVG_NS, "ellipse");
        hatShadow.setAttribute("cx", "110");
        hatShadow.setAttribute("cy", "61");
        hatShadow.setAttribute("rx", "76");
        hatShadow.setAttribute("ry", "16");
        hatShadow.setAttribute("fill", "#050505");
        hatShadow.setAttribute("stroke", "#333");
        hatShadow.setAttribute("stroke-width", "2");

        svg.appendChild(hatShadow);

        /*
         * Bucket hat crown
         */
        const hat = document.createElementNS(SVG_NS, "path");

        hat.setAttribute(
            "d",
            "M54 61 Q62 31 110 29 Q158 31 166 61 L155 91 Q110 103 65 91 Z"
        );

        hat.setAttribute("fill", "#080808");
        hat.setAttribute("stroke", "#3a3a3a");
        hat.setAttribute("stroke-width", "3");

        svg.appendChild(hat);

        /*
         * Hat brim
         */
        const brim = document.createElementNS(SVG_NS, "path");

        brim.setAttribute(
            "d",
            "M38 62 Q110 45 182 62 Q187 72 178 78 Q110 96 42 78 Q33 72 38 62 Z"
        );

        brim.setAttribute("fill", "#030303");
        brim.setAttribute("stroke", "#4a4a4a");
        brim.setAttribute("stroke-width", "3");

        svg.appendChild(brim);

        /*
         * AJ on hat
         */
        const ajText = document.createElementNS(SVG_NS, "text");

        ajText.setAttribute("x", "110");
        ajText.setAttribute("y", "66");
        ajText.setAttribute("text-anchor", "middle");
        ajText.setAttribute(
            "font-family",
            "Georgia, Times New Roman, serif"
        );
        ajText.setAttribute("font-size", "24");
        ajText.setAttribute("font-weight", "700");
        ajText.setAttribute("letter-spacing", "4");
        ajText.setAttribute("fill", "#d0b071");

        ajText.textContent = "AJ";

        svg.appendChild(ajText);

        /*
         * Fox head
         */
        const foxHead = document.createElementNS(SVG_NS, "path");

        foxHead.setAttribute(
            "d",
            "M54 93 L42 118 L51 111 L57 145 Q64 180 110 192 Q156 180 163 145 L169 111 L178 118 L166 93 L151 105 Q132 94 110 94 Q88 94 69 105 Z"
        );

        foxHead.setAttribute("fill", "#020202");
        foxHead.setAttribute("stroke", "#242424");
        foxHead.setAttribute("stroke-width", "3");
        foxHead.setAttribute("stroke-linejoin", "round");

        svg.appendChild(foxHead);

        /*
         * Face planes
         */
        const leftPlane = document.createElementNS(SVG_NS, "path");

        leftPlane.setAttribute(
            "d",
            "M110 111 L110 180 Q81 172 70 146 Q67 128 81 116 Q95 108 110 111 Z"
        );

        leftPlane.setAttribute("fill", "#0b0b0b");

        svg.appendChild(leftPlane);

        const rightPlane = document.createElementNS(SVG_NS, "path");

        rightPlane.setAttribute(
            "d",
            "M110 111 L110 180 Q139 172 150 146 Q153 128 139 116 Q125 108 110 111 Z"
        );

        rightPlane.setAttribute("fill", "#070707");

        svg.appendChild(rightPlane);

        /*
         * Eyes
         */
        const eyeLeft = document.createElementNS(SVG_NS, "path");

        eyeLeft.setAttribute(
            "d",
            "M69 126 Q83 116 98 126 Q84 132 70 130 Z"
        );

        eyeLeft.setAttribute("fill", "#d5d5d5");

        svg.appendChild(eyeLeft);

        const eyeRight = document.createElementNS(SVG_NS, "path");

        eyeRight.setAttribute(
            "d",
            "M122 126 Q137 116 151 126 Q137 132 122 130 Z"
        );

        eyeRight.setAttribute("fill", "#d5d5d5");

        svg.appendChild(eyeRight);

        /*
         * Nose
         */
        const nose = document.createElementNS(SVG_NS, "path");

        nose.setAttribute(
            "d",
            "M100 151 Q110 144 120 151 L110 160 Z"
        );

        nose.setAttribute("fill", "#555");

        svg.appendChild(nose);

        /*
         * Mouth
         */
        const mouth = document.createElementNS(SVG_NS, "path");

        mouth.setAttribute(
            "d",
            "M92 164 Q110 174 128 164"
        );

        mouth.setAttribute("fill", "none");
        mouth.setAttribute("stroke", "#777");
        mouth.setAttribute("stroke-width", "2");
        mouth.setAttribute("stroke-linecap", "round");

        svg.appendChild(mouth);

        return svg;
    }

    /*
     * ---------------------------------------------------------
     * 4. HELPERS
     * ---------------------------------------------------------
     */

    function createElement(tag, className, text) {
        const element = document.createElement(tag);

        if (className) {
            element.className = className;
        }

        if (typeof text === "string") {
            element.textContent = text;
        }

        return element;
    }

    function getAnimeCatalog() {
        const candidates = [
            window.AJVYRA_FINAL_ANIME_CATALOG,
            window.AJVYRA_ANIME_CATALOG,
            window.AJVYRA_WATCHABLE_CATALOG
        ];

        for (const catalog of candidates) {
            if (Array.isArray(catalog)) {
                return catalog;
            }

            if (
                catalog &&
                Array.isArray(catalog.films)
            ) {
                return catalog.films;
            }

            if (
                catalog &&
                Array.isArray(catalog.anime)
            ) {
                return catalog.anime;
            }
        }

        return [];
    }

    function getGameCatalog() {
        const candidates = [
            window.AJVYRA_FINAL_GAME_CATALOG,
            window.AJVYRA_GAME_CATALOG
        ];

        for (const catalog of candidates) {
            if (Array.isArray(catalog)) {
                return catalog;
            }

            if (
                catalog &&
                Array.isArray(catalog.games)
            ) {
                return catalog.games;
            }
        }

        return [];
    }

    function normalizeItem(item, index, type) {
        if (typeof item === "string") {
            return {
                title: item,
                poster: "",
                mediaUrl: "",
                type,
                index
            };
        }

        if (!item || typeof item !== "object") {
            return {
                title: `${type} ${index + 1}`,
                poster: "",
                mediaUrl: "",
                type,
                index
            };
        }

        return {
            title:
                item.title ||
                item.name ||
                `${type} ${index + 1}`,

            poster:
                item.poster ||
                item.posterUrl ||
                item.cover ||
                item.coverUrl ||
                "",

            mediaUrl:
                item.mediaUrl ||
                item.videoUrl ||
                item.url ||
                item.file ||
                "",

            type,
            index
        };
    }

    /*
     * ---------------------------------------------------------
     * 5. ROOT
     * ---------------------------------------------------------
     */

    const root = createElement("div");

    root.id = ROOT_ID;

    /*
     * ---------------------------------------------------------
     * 6. HEADER
     * ---------------------------------------------------------
     */

    const header = createElement("header", "ajv-header");

    const brand = createElement("a", "ajv-brand");

    brand.href = "#home";
    brand.setAttribute("aria-label", "AJVYRA home");

    brand.appendChild(createFoxLogo(48));

    const brandWord = createElement("span", "aj-brand-word");

    brandWord.appendChild(
        createElement("span", "aj-brand-name", "AJVYRA")
    );

    brandWord.appendChild(
        createElement(
            "span",
            "aj-brand-sub",
            "Dark Worlds / New Stories"
        )
    );

    brand.appendChild(brandWord);

    header.appendChild(brand);

    const nav = createElement("nav", "aj-nav");

    const navItems = [
        ["home", "Home"],
        ["anime", "Anime"],
        ["games", "Games"],
        ["library", "Library"]
    ];

    navItems.forEach(([id, label]) => {
        const button = createElement(
            "button",
            "aj-nav-btn",
            label
        );

        button.type = "button";
        button.dataset.section = id;

        nav.appendChild(button);
    });

    header.appendChild(nav);

    const actions = createElement(
        "div",
        "aj-header-actions"
    );

    const searchButton = createElement(
        "button",
        "aj-icon-btn",
        "⌕"
    );

    searchButton.type = "button";
    searchButton.setAttribute(
        "aria-label",
        "Open search"
    );

    actions.appendChild(searchButton);

    const menuButton = createElement(
        "button",
        "aj-icon-btn",
        "☰"
    );

    menuButton.type = "button";
    menuButton.setAttribute(
        "aria-label",
        "Open menu"
    );

    actions.appendChild(menuButton);

    header.appendChild(actions);

    root.appendChild(header);

    /*
     * ---------------------------------------------------------
     * 7. SEARCH
     * ---------------------------------------------------------
     */

    const searchPanel = createElement(
        "div",
        "ajv-search-panel"
    );

    const searchInput = document.createElement("input");

    searchInput.className = "ajv-search-input";
    searchInput.type = "search";
    searchInput.placeholder =
        "Search anime, games, worlds...";
    searchInput.setAttribute(
        "aria-label",
        "Search AJVYRA"
    );

    searchPanel.appendChild(searchInput);

    root.appendChild(searchPanel);

    /*
     * ---------------------------------------------------------
     * 8. MAIN
     * ---------------------------------------------------------
     */

    const main = document.createElement("main");

    main.id = "home";

    /*
     * HERO
     */

    const hero = createElement("section", "ajv-hero");

    const heroShell = createElement(
        "div",
        "ajv-shell"
    );

    const heroInner = createElement(
        "div",
        "ajv-hero-inner"
    );

    heroInner.appendChild(
        createElement(
            "div",
            "ajv-eyebrow",
            "AJVYRA ORIGINAL PLATFORM"
        )
    );

    const heroTitle = createElement(
        "h1",
        "ajv-title"
    );

    heroTitle.innerHTML =
        "DARK WORLDS.<br><span>NEW STORIES.</span>";

    heroInner.appendChild(heroTitle);

    heroInner.appendChild(
        createElement(
            "p",
            "ajv-description",
            "A cinematic home for original anime worlds, games, characters and stories — built as one independent universe."
        )
    );

    const heroActions = createElement(
        "div",
        "ajv-hero-actions"
    );

    const exploreButton = createElement(
        "button",
        "ajv-primary",
        "Explore Anime"
    );

    exploreButton.type = "button";
    exploreButton.dataset.sectionTarget = "anime";

    const gamesButton = createElement(
        "button",
        "ajv-secondary",
        "Enter Games"
    );

    gamesButton.type = "button";
    gamesButton.dataset.sectionTarget = "games";

    heroActions.appendChild(exploreButton);
    heroActions.appendChild(gamesButton);

    heroInner.appendChild(heroActions);
    heroShell.appendChild(heroInner);
    hero.appendChild(heroShell);
    main.appendChild(hero);

    /*
     * ---------------------------------------------------------
     * 9. ANIME SECTION
     * ---------------------------------------------------------
     */

    const animeSection = createElement(
        "section",
        "ajv-section"
    );

    animeSection.id = "anime";

    const animeShell = createElement(
        "div",
        "ajv-shell"
    );

    const animeHeader = createElement(
        "div",
        "ajv-section-header"
    );

    const animeHeadingGroup = document.createElement("div");

    animeHeadingGroup.appendChild(
        createElement(
            "p",
            "ajv-section-kicker",
            "Cinema"
        )
    );

    animeHeadingGroup.appendChild(
        createElement(
            "h2",
            "ajv-section-title",
            "Anime Worlds"
        )
    );

    animeHeader.appendChild(animeHeadingGroup);

    animeHeader.appendChild(
        createElement(
            "span",
            "ajv-section-note",
            "Finished releases only"
        )
    );

    animeShell.appendChild(animeHeader);

    const animeGrid = createElement(
        "div",
        "ajv-grid"
    );

    animeGrid.id = "ajv-anime-grid";

    animeShell.appendChild(animeGrid);
    animeSection.appendChild(animeShell);
    main.appendChild(animeSection);

    /*
     * ---------------------------------------------------------
     * 10. GAMES SECTION
     * ---------------------------------------------------------
     */

    const gamesSection = createElement(
        "section",
        "ajv-section"
    );

    gamesSection.id = "games";

    const gamesShell = createElement(
        "div",
        "ajv-shell"
    );

    const gamesHeader = createElement(
        "div",
        "ajv-section-header"
    );

    const gamesHeadingGroup = document.createElement("div");

    gamesHeadingGroup.appendChild(
        createElement(
            "p",
            "ajv-section-kicker",
            "Play"
        )
    );

    gamesHeadingGroup.appendChild(
        createElement(
            "h2",
            "ajv-section-title",
            "Games"
        )
    );

    gamesHeader.appendChild(gamesHeadingGroup);

    gamesHeader.appendChild(
        createElement(
            "span",
            "ajv-section-note",
            "Original AJVYRA experiences"
        )
    );

    gamesShell.appendChild(gamesHeader);

    const gamesGrid = createElement(
        "div",
        "ajv-grid"
    );

    gamesGrid.id = "ajv-games-grid";

    gamesShell.appendChild(gamesGrid);
    gamesSection.appendChild(gamesShell);
    main.appendChild(gamesSection);

    /*
     * ---------------------------------------------------------
     * 11. LIBRARY SECTION
     * ---------------------------------------------------------
     */

    const librarySection = createElement(
        "section",
        "ajv-section"
    );

    librarySection.id = "library";

    const libraryShell = createElement(
        "div",
        "ajv-shell"
    );

    const libraryHeader = createElement(
        "div",
        "ajv-section-header"
    );

    const libraryHeadingGroup = document.createElement("div");

    libraryHeadingGroup.appendChild(
        createElement(
            "p",
            "ajv-section-kicker",
            "Your Space"
        )
    );

    libraryHeadingGroup.appendChild(
        createElement(
            "h2",
            "ajv-section-title",
            "Library"
        )
    );

    libraryHeader.appendChild(libraryHeadingGroup);

    libraryShell.appendChild(libraryHeader);

    const libraryGrid = createElement(
        "div",
        "ajv-grid"
    );

    libraryGrid.id = "ajv-library-grid";

    libraryShell.appendChild(libraryGrid);
    librarySection.appendChild(libraryShell);
    main.appendChild(librarySection);

    root.appendChild(main);

    /*
     * ---------------------------------------------------------
     * 12. FOOTER
     * ---------------------------------------------------------
     */

    const footer = createElement(
        "footer",
        "ajv-footer"
    );

    const footerShell = createElement(
        "div",
        "ajv-shell"
    );

    const footerInner = createElement(
        "div",
        "ajv-footer-inner"
    );

    footerInner.appendChild(
        createElement(
            "div",
            "ajv-footer-brand",
            "AJVYRA"
        )
    );

    footerInner.appendChild(
        createElement(
            "div",
            "ajv-footer-copy",
            "Original worlds. Original stories."
        )
    );

    footerShell.appendChild(footerInner);
    footer.appendChild(footerShell);
    root.appendChild(footer);

    document.body.appendChild(root);

    /*
     * ---------------------------------------------------------
     * 13. CARD RENDERER
     * ---------------------------------------------------------
     */

    function renderCatalog(grid, items, type) {
        grid.innerHTML = "";

        if (!Array.isArray(items) || items.length === 0) {
            const empty = createElement(
                "div",
                "ajv-empty",
                type === "anime"
                    ? "No released anime assets are connected yet."
                    : "No released games are connected yet."
            );

            grid.appendChild(empty);
            return;
        }

        const normalized = items
            .map((item, index) =>
                normalizeItem(item, index, type)
            )
            .slice(0, 100);

        normalized.forEach((item) => {
            const card = createElement(
                "article",
                "ajv-card"
            );

            card.dataset.title =
                item.title.toLowerCase();

            const poster = createElement(
                "div",
                "ajv-poster"
            );

            if (item.poster) {
                const image =
                    document.createElement("img");

                image.src = item.poster;
                image.alt = `${item.title} poster`;
                image.loading = "lazy";

                poster.appendChild(image);
            }

            const body = createElement(
                "div",
                "ajv-card-body"
            );

            body.appendChild(
                createElement(
                    "h3",
                    "ajv-card-title",
                    item.title
                )
            );

            body.appendChild(
                createElement(
                    "div",
                    "ajv-card-meta",
                    type === "anime"
                        ? "Anime"
                        : "Game"
                )
            );

            card.appendChild(poster);
            card.appendChild(body);

            card.addEventListener("click", () => {
                if (item.mediaUrl) {
                    window.dispatchEvent(
                        new CustomEvent(
                            "ajvyra:open-release",
                            {
                                detail: item
                            }
                        )
                    );
                }
            });

            grid.appendChild(card);
        });
    }

    /*
     * ---------------------------------------------------------
     * 14. LIBRARY
     * ---------------------------------------------------------
     */

    function renderLibrary() {
        libraryGrid.innerHTML = "";

        const storedLibrary =
            Array.isArray(window.AJVYRA_LIBRARY)
                ? window.AJVYRA_LIBRARY
                : [];

        if (storedLibrary.length === 0) {
            libraryGrid.appendChild(
                createElement(
                    "div",
                    "ajv-empty",
                    "Your saved worlds will appear here."
                )
            );

            return;
        }

        renderCatalog(
            libraryGrid,
            storedLibrary,
            "anime"
        );
    }

    /*
     * ---------------------------------------------------------
     * 15. SEARCH
     * ---------------------------------------------------------
     */

    function applySearch() {
        const query =
            searchInput.value
                .trim()
                .toLowerCase();

        const cards =
            root.querySelectorAll(".ajv-card");

        cards.forEach((card) => {
            const title =
                card.dataset.title || "";

            card.style.display =
                !query || title.includes(query)
                    ? ""
                    : "none";
        });
    }

    searchInput.addEventListener(
        "input",
        applySearch
    );

    searchButton.addEventListener(
        "click",
        () => {
            searchPanel.classList.toggle("open");

            if (searchPanel.classList.contains("open")) {
                searchInput.focus();
            }
        }
    );

    /*
     * ---------------------------------------------------------
     * 16. NAVIGATION
     * ---------------------------------------------------------
     */

    function goToSection(sectionId) {
        const target =
            document.getElementById(sectionId);

        if (!target) {
            return;
        }

        target.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

        document
            .querySelectorAll(".ajv-nav-btn")
            .forEach((button) => {
                button.classList.toggle(
                    "active",
                    button.dataset.section === sectionId
                );
            });
    }

    nav.addEventListener(
        "click",
        (event) => {
            const button =
                event.target.closest(".ajv-nav-btn");

            if (!button) {
                return;
            }

            goToSection(button.dataset.section);
        }
    );

    root.querySelectorAll(
        "[data-section-target]"
    ).forEach((button) => {
        button.addEventListener(
            "click",
            () => {
                goToSection(
                    button.dataset.sectionTarget
                );
            }
        );
    });

    menuButton.addEventListener(
        "click",
        () => {
            const isOpen =
                nav.style.display === "flex";

            nav.style.display =
                isOpen ? "" : "flex";

            if (!isOpen) {
                nav.style.flexDirection = "column";
                nav.style.position = "absolute";
                nav.style.top = "68px";
                nav.style.left = "16px";
                nav.style.right = "16px";
                nav.style.padding = "12px";
                nav.style.background = "#090909";
                nav.style.border =
                    "1px solid rgba(255,255,255,.09)";
                nav.style.borderRadius = "16px";
            }
        }
    );

    /*
     * ---------------------------------------------------------
     * 17. LOAD REAL RELEASE CATALOGS
     * ---------------------------------------------------------
     */

    renderCatalog(
        animeGrid,
        getAnimeCatalog(),
        "anime"
    );

    renderCatalog(
        gamesGrid,
        getGameCatalog(),
        "games"
    );

    renderLibrary();

    /*
     * ---------------------------------------------------------
     * 18. PUBLIC API
     * ---------------------------------------------------------
     */

    window.AJVYRAFinalBrandUI = {
        root,
        logo: createFoxLogo,

        refresh() {
            renderCatalog(
                animeGrid,
                getAnimeCatalog(),
                "anime"
            );

            renderCatalog(
                gamesGrid,
                getGameCatalog(),
                "games"
            );

            renderLibrary();

            applySearch();
        },

        goToSection,

        openSearch() {
            searchPanel.classList.add("open");
            searchInput.focus();
        }
    };

    /*
     * ---------------------------------------------------------
     * 19. INITIAL STATE
     * ---------------------------------------------------------
     */

    const homeButton =
        nav.querySelector(
            '[data-section="home"]'
        );

    if (homeButton) {
        homeButton.classList.add("active");
    }

})();
