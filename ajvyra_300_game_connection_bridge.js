/* ============================================================
   AJVYRA — 300 GAME CONNECTION BRIDGE
   Connects existing game definitions to:
   Runtime + Quality Layer + Registry
   ============================================================ */

(function AJVYRA_300_GAME_BRIDGE() {

    "use strict";

    /* --------------------------------------------------------
       REQUIRE CORE
       -------------------------------------------------------- */

    if (
        typeof AJVYRA_RUNTIME === "undefined" ||
        typeof AJVYRA_GAMES === "undefined" ||
        typeof AJVYRA_QUALITY === "undefined"
    ) {
        throw new Error(
            "AJVYRA: Core runtime is not loaded."
        );
    }

    /* --------------------------------------------------------
       GAME CONFIGURATION
       -------------------------------------------------------- */

    const GAME_COUNT = 300;

    const connectedGames = new Map();

    const gameState = {

        currentId: null,

        startedAt: 0,

        completed: new Set(),

        unlocked: new Set(["game-001"]),

        statistics: new Map()
    };


    /* --------------------------------------------------------
       NORMALIZE GAME DEFINITION
       -------------------------------------------------------- */

    function normalizeGame(id, definition) {

        if (!definition) {
            return null;
        }

        const normalized = {

            id,

            title:
                definition.title ||
                id,

            genre:
                definition.genre ||
                "action",

            description:
                definition.description ||
                "",

            init:
                typeof definition.init === "function"
                    ? definition.init
                    : function () {},

            update:
                typeof definition.update === "function"
                    ? definition.update
                    : function () {},

            draw:
                typeof definition.draw === "function"
                    ? definition.draw
                    : function () {},

            reset:
                typeof definition.reset === "function"
                    ? definition.reset
                    : null,

            quality:
                definition.quality ||
                "high",

            mobile:
                definition.mobile !== false,

            desktop:
                definition.desktop !== false,

            controls:
                definition.controls ||
                {},

            difficulty:
                definition.difficulty ||
                "normal"
        };

        return normalized;
    }


    /* --------------------------------------------------------
       SAFE GAME WRAPPER
       -------------------------------------------------------- */

    function wrapGame(id, definition) {

        const game =
            normalizeGame(
                id,
                definition
            );

        if (!game) {
            return null;
        }

        return {

            id: game.id,

            title: game.title,

            genre: game.genre,

            description:
                game.description,

            quality:
                game.quality,

            mobile:
                game.mobile,

            desktop:
                game.desktop,

            controls:
                game.controls,

            difficulty:
                game.difficulty,


            init(runtime) {

                gameState.currentId = id;
                gameState.startedAt =
                    performance.now();

                if (
                    game.quality === "low"
                ) {
                    AJVYRA_QUALITY.setQuality(
                        "low"
                    );

                } else if (
                    game.quality === "medium"
                ) {
                    AJVYRA_QUALITY.setQuality(
                        "medium"
                    );

                } else {

                    AJVYRA_QUALITY.setQuality(
                        "high"
                    );
                }

                runtime.player = null;

                game.init(
                    runtime,
                    AJVYRA_QUALITY
                );
            },


            update(runtime, dt) {

                game.update(
                    runtime,
                    dt,
                    AJVYRA_QUALITY
                );

                AJVYRA_QUALITY.update(dt);

                AJVYRA_QUALITY.drawProjectiles();
            },


            draw(runtime) {

                game.draw(
                    runtime,
                    AJVYRA_QUALITY
                );

                AJVYRA_QUALITY.draw();
            }
        };
    }


    /* --------------------------------------------------------
       REGISTER ONE GAME
       -------------------------------------------------------- */

    function connectGame(id, definition) {

        const wrapped =
            wrapGame(
                id,
                definition
            );

        if (!wrapped) {
            return false;
        }

        try {

            AJVYRA_GAMES.register(
                id,
                wrapped
            );

            connectedGames.set(
                id,
                wrapped
            );

            return true;

        } catch (error) {

            console.error(
                "AJVYRA game connection failed:",
                id,
                error
            );

            return false;
        }
    }


    /* --------------------------------------------------------
       CONNECT EXISTING GAME COLLECTION
       -------------------------------------------------------- */

    function connectCollection(collection) {

        if (!collection) {
            return 0;
        }

        let connected = 0;

        /* Array */

        if (Array.isArray(collection)) {

            collection.forEach(
                (definition, index) => {

                    const number =
                        String(index + 1)
                            .padStart(3, "0");

                    const id =
                        definition.id ||
                        `game-${number}`;

                    if (
                        connectGame(
                            id,
                            definition
                        )
                    ) {
                        connected++;
                    }
                }
            );

            return connected;
        }


        /* Object */

        if (
            typeof collection ===
            "object"
        ) {

            for (
                const [
                    key,
                    definition
                ]
                of Object.entries(collection)
            ) {

                const id =
                    definition.id ||
                    key;

                if (
                    connectGame(
                        id,
                        definition
                    )
                ) {
                    connected++;
                }
            }
        }

        return connected;
    }


    /* --------------------------------------------------------
       CONNECT GLOBAL AJVYRA GAME DATA
       -------------------------------------------------------- */

    const possibleSources = [

        window.AJVYRA_GAME_DEFINITIONS,

        window.AJVYRA_GAMES_DATA,

        window.AJVYRA_GAME_LIBRARY,

        window.AJVYRA_300_GAMES,

        window.AJVYRA_GAMES_LIST
    ];

    let totalConnected = 0;

    for (
        const source
        of possibleSources
    ) {

        if (!source) {
            continue;
        }

        totalConnected +=
            connectCollection(
                source
            );
    }


    /* --------------------------------------------------------
       DIRECT REGISTRY BRIDGE
       -------------------------------------------------------- */

    function connectFromRegistry() {

        if (
            !window.AJVYRA_GAME_REGISTRY_DATA
        ) {
            return 0;
        }

        return connectCollection(
            window.AJVYRA_GAME_REGISTRY_DATA
        );
    }

    totalConnected +=
        connectFromRegistry();


    /* --------------------------------------------------------
       PLAY
       -------------------------------------------------------- */

    function play(id) {

        if (!connectedGames.has(id)) {

            console.warn(
                `AJVYRA: ${id} is not connected.`
            );

            return false;
        }

        const game =
            connectedGames.get(id);

        gameState.currentId = id;

        AJVYRA_RUNTIME.loadGame(
            game
        );

        return true;
    }


    /* --------------------------------------------------------
       NEXT GAME
       -------------------------------------------------------- */

    function next() {

        const ids =
            Array.from(
                connectedGames.keys()
            );

        if (!ids.length) {
            return false;
        }

        const currentIndex =
            ids.indexOf(
                gameState.currentId
            );

        const nextIndex =
            currentIndex < 0
                ? 0
                : (currentIndex + 1) %
                  ids.length;

        return play(
            ids[nextIndex]
        );
    }


    /* --------------------------------------------------------
       PREVIOUS GAME
       -------------------------------------------------------- */

    function previous() {

        const ids =
            Array.from(
                connectedGames.keys()
            );

        if (!ids.length) {
            return false;
        }

        const currentIndex =
            ids.indexOf(
                gameState.currentId
            );

        const previousIndex =
            currentIndex <= 0
                ? ids.length - 1
                : currentIndex - 1;

        return play(
            ids[previousIndex]
        );
    }


    /* --------------------------------------------------------
       GAME COMPLETION
       -------------------------------------------------------- */

    function complete(id) {

        if (
            !connectedGames.has(id)
        ) {
            return false;
        }

        gameState.completed.add(id);

        const number =
            parseInt(
                id.replace(/\D/g, ""),
                10
            );

        if (
            Number.isFinite(number)
        ) {

            const nextNumber =
                number + 1;

            if (
                nextNumber <= GAME_COUNT
            ) {

                gameState.unlocked.add(
                    `game-${String(
                        nextNumber
                    ).padStart(3, "0")}`
                );
            }
        }

        return true;
    }


    /* --------------------------------------------------------
       STATISTICS
       -------------------------------------------------------- */

    function recordResult(
        id,
        result = {}
    ) {

        const existing =
            gameState.statistics.get(
                id
            ) || {

                plays: 0,

                wins: 0,

                deaths: 0,

                bestScore: 0,

                totalTime: 0
            };


        existing.plays++;


        if (result.win) {
            existing.wins++;
        }


        if (result.death) {
            existing.deaths++;
        }


        if (
            Number.isFinite(
                result.score
            )
        ) {

            existing.bestScore =
                Math.max(
                    existing.bestScore,
                    result.score
                );
        }


        if (
            Number.isFinite(
                result.time
            )
        ) {

            existing.totalTime +=
                result.time;
        }


        gameState.statistics.set(
            id,
            existing
        );
    }


    /* --------------------------------------------------------
       AUTOMATIC COMPLETION HOOK
       -------------------------------------------------------- */

    function checkGameState() {

        const id =
            gameState.currentId;

        if (!id) {
            return;
        }

        const runtime =
            AJVYRA_RUNTIME;

        if (
            runtime.player &&
            runtime.player.custom &&
            runtime.player.custom.gameWon
        ) {

            complete(id);

            recordResult(
                id,
                {
                    win: true,
                    score:
                        runtime.score
                }
            );

            runtime.player.custom.gameWon =
                false;
        }
    }


    /* --------------------------------------------------------
       GAME MANAGER LOOP
       -------------------------------------------------------- */

    const originalUpdate =
        AJVYRA_RUNTIME.game;

    void originalUpdate;

    setInterval(
        checkGameState,
        250
    );


    /* --------------------------------------------------------
       PUBLIC API
       -------------------------------------------------------- */

    window.AJVYRA_300 = {

        count:
            GAME_COUNT,

        connectedGames,

        state:
            gameState,

        connectGame,

        connectCollection,

        play,

        next,

        previous,

        complete,

        recordResult,

        getConnectedCount() {

            return connectedGames.size;
        },

        getRemainingCount() {

            return Math.max(
                0,
                GAME_COUNT -
                connectedGames.size
            );
        },

        getCompletedCount() {

            return gameState
                .completed
                .size;
        },

        getGame(id) {

            return connectedGames.get(
                id
            ) || null;
        },

        list() {

            return Array.from(
                connectedGames.values()
            ).map(game => ({

                id: game.id,

                title: game.title,

                genre: game.genre,

                difficulty:
                    game.difficulty,

                quality:
                    game.quality,

                mobile:
                    game.mobile,

                desktop:
                    game.desktop
            }));
        }
    };


    /* --------------------------------------------------------
       DEVELOPMENT REPORT
       -------------------------------------------------------- */

    console.info(
        "AJVYRA 300 GAME BRIDGE READY",
        {
            target: GAME_COUNT,
            connected: connectedGames.size,
            remaining:
                Math.max(
                    0,
                    GAME_COUNT -
                    connectedGames.size
                )
        }
    );

})();
