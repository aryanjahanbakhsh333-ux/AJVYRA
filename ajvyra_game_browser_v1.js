"use strict";

const state = {
    manifest: null,
    sessionId: null,
    gameId: null,
    running: false,
    localState: {},
};

const catalogScreen =
    document.getElementById("catalogScreen");

const gameScreen =
    document.getElementById("gameScreen");

const gameGrid =
    document.getElementById("gameGrid");

const canvas =
    document.getElementById("gameCanvas");

const ctx =
    canvas.getContext("2d");

const title =
    document.getElementById("gameTitle");

const status =
    document.getElementById("gameStatus");

const backButton =
    document.getElementById("backButton");


async function loadManifest() {
    const response = await fetch(
        "ajvyra_game_manifest.json",
        { cache: "no-store" }
    );

    if (!response.ok) {
        throw new Error("Game manifest unavailable.");
    }

    state.manifest = await response.json();

    renderCatalog();
}


function renderCatalog() {
    gameGrid.innerHTML = "";

    for (const game of state.manifest.games) {
        const card = document.createElement("button");

        card.className = "gameCard";

        card.innerHTML = `
            <div class="gameNumber">
                GAME ${String(game.id).padStart(3, "0")}
            </div>
            <div class="gameName">
                ${escapeHtml(game.title)}
            </div>
        `;

        card.addEventListener(
            "click",
            () => launchGame(game.id)
        );

        gameGrid.appendChild(card);
    }
}


async function launchGame(gameId) {
    try {
        const response = await fetch(
            "/api/game/launch",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    game_id: gameId
                })
            }
        );

        const result = await response.json();

        if (!result.ok) {
            throw new Error(result.error);
        }

        state.sessionId =
            result.session.session_id;

        state.gameId = gameId;
        state.running = true;
        state.localState =
            result.session.state || {};

        const game =
            state.manifest.games.find(
                item => item.id === gameId
            );

        title.textContent =
            game ? game.title : `GAME ${gameId}`;

        catalogScreen.classList.add("hidden");
        gameScreen.classList.remove("hidden");

        resizeCanvas();
        renderFrame();

    } catch (error) {
        showError(error);
    }
}


async function sendAction(
    action,
    params = {}
) {
    if (!state.running) {
        return;
    }

    try {
        const response = await fetch(
            "/api/game/action",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    session_id: state.sessionId,
                    action: action,
                    params: params
                })
            }
        );

        const result = await response.json();

        if (!result.ok) {
            showError(result.error);
            return;
        }

        state.localState =
            result.state || {};

        renderFrame();

    } catch (error) {
        showError(error);
    }
}


function renderFrame() {
    const width = canvas.width;
    const height = canvas.height;

    ctx.clearRect(
        0,
        0,
        width,
        height
    );

    ctx.fillStyle = "#050505";
    ctx.fillRect(
        0,
        0,
        width,
        height
    );

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 24px Arial";

    ctx.fillText(
        title.textContent,
        30,
        45
    );

    ctx.fillStyle = "#888";
    ctx.font = "14px Arial";

    const lines =
        flattenState(
            state.localState
        );

    let y = 78;

    for (const line of lines.slice(0, 20)) {
        ctx.fillText(
            line,
            30,
            y
        );

        y += 23;
    }

    status.textContent =
        `GAME ${state.gameId} • READY`;
}


function flattenState(value, prefix = "") {
    const lines = [];

    if (
        value === null ||
        value === undefined
    ) {
        return lines;
    }

    if (
        typeof value !== "object"
    ) {
        lines.push(
            `${prefix}: ${String(value)}`
        );

        return lines;
    }

    for (const [key, item] of Object.entries(value)) {
        const next =
            prefix
                ? `${prefix}.${key}`
                : key;

        if (
            item !== null &&
            typeof item === "object"
        ) {
            lines.push(
                ...flattenState(
                    item,
                    next
                )
            );
        } else {
            lines.push(
                `${next}: ${String(item)}`
            );
        }
    }

    return lines;
}


function resizeCanvas() {
    const rect =
        canvas.getBoundingClientRect();

    const dpr =
        window.devicePixelRatio || 1;

    canvas.width =
        Math.floor(rect.width * dpr);

    canvas.height =
        Math.floor(rect.height * dpr);

    ctx.scale(dpr, dpr);
}


function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function showError(error) {
    console.error(error);
    status.textContent =
        `ERROR: ${error.message || error}`;
}


backButton.addEventListener(
    "click",
    async () => {
        if (state.sessionId) {
            try {
                await fetch(
                    "/api/game/stop",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type":
                                "application/json"
                        },
                        body: JSON.stringify({
                            session_id:
                                state.sessionId
                        })
                    }
                );
            } catch (_) {}
        }

        state.running = false;
        state.sessionId = null;

        gameScreen.classList.add("hidden");
        catalogScreen.classList.remove("hidden");

        title.textContent = "SELECT A GAME";
    }
);


document.querySelectorAll(
    "#touchControls button"
).forEach(button => {
    button.addEventListener(
        "pointerdown",
        event => {
            event.preventDefault();

            sendAction(
                button.dataset.action
            );
        }
    );
});


window.addEventListener(
    "keydown",
    event => {
        const map = {
            ArrowUp: "up",
            ArrowDown: "down",
            ArrowLeft: "left",
            ArrowRight: "right",
            w: "up",
            W: "up",
            s: "down",
            S: "down",
            a: "left",
            A: "left",
            d: "right",
            D: "right",
            " ": "primary",
            Enter: "primary",
            Shift: "secondary",
        };

        const action = map[event.key];

        if (action) {
            event.preventDefault();
            sendAction(action);
        }
    }
);


window.addEventListener(
    "resize",
    () => {
        if (!gameScreen.classList.contains("hidden")) {
            resizeCanvas();
            renderFrame();
        }
    }
);


loadManifest().catch(showError);
