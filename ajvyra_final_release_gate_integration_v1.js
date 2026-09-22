/*
 * AJVYRA — Final Release Gate Integration
 * File: ajvyra_final_release_gate_integration_v1.js
 *
 * Rule:
 * 30/30 anime must be READY + PUBLISHED + have video URLs.
 */

(function () {
    "use strict";

    if (window.__AJVYRA_FINAL_RELEASE_GATE_V1__) {
        return;
    }

    window.__AJVYRA_FINAL_RELEASE_GATE_V1__ = true;

    const EXPECTED_ANIME = 30;

    function createGateScreen(message) {
        let gate =
            document.getElementById(
                "ajvyra-final-release-gate"
            );

        if (gate) {
            return gate;
        }

        gate =
            document.createElement("main");

        gate.id =
            "ajvyra-final-release-gate";

        gate.innerHTML = `
            <section
                style="
                    min-height:100vh;
                    background:#030303;
                    color:#fff;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    padding:32px;
                    font-family:Inter,-apple-system,BlinkMacSystemFont,sans-serif;
                "
            >
                <div
                    style="
                        width:min(680px,100%);
                        border:1px solid rgba(255,255,255,.08);
                        background:#090909;
                        padding:42px;
                        border-radius:22px;
                    "
                >
                    <div
                        style="
                            color:#c9a86a;
                            font-size:10px;
                            letter-spacing:.3em;
                            margin-bottom:18px;
                        "
                    >
                        AJVYRA RELEASE CONTROL
                    </div>

                    <h1
                        style="
                            margin:0;
                            font-size:clamp(32px,7vw,64px);
                            line-height:.95;
                        "
                    >
                        Release Locked
                    </h1>

                    <p
                        id="ajvyra-gate-message"
                        style="
                            margin:24px 0 0;
                            color:#888;
                            line-height:1.8;
                            font-size:14px;
                        "
                    >
                        ${message}
                    </p>

                    <div
                        style="
                            margin-top:30px;
                            padding-top:20px;
                            border-top:1px solid rgba(255,255,255,.07);
                            color:#555;
                            font-size:11px;
                        "
                    >
                        AJVYRA will not present an incomplete
                        cinematic catalog as a final release.
                    </div>
                </div>
            </section>
        `;

        document.body.innerHTML = "";
        document.body.appendChild(gate);

        return gate;
    }

    function evaluate(state) {
        if (!state) {
            createGateScreen(
                "No final release state was supplied."
            );

            return false;
        }

        const valid =
            state.ready === true &&
            state.animeCount === EXPECTED_ANIME &&
            Array.isArray(state.errors) &&
            state.errors.length === 0;

        if (!valid) {
            createGateScreen(
                state.errors &&
                state.errors.length
                    ? state.errors
                        .slice(0, 6)
                        .join(" ")
                    : "The final 30-film release has not passed validation."
            );

            return false;
        }

        window.AJVYRA_FINAL_RELEASE_APPROVED =
            true;

        window.dispatchEvent(
            new CustomEvent(
                "ajvyra:release-approved"
            )
        );

        return true;
    }

    window.addEventListener(
        "ajvyra:release-catalog-ready",
        function (event) {
            evaluate(event.detail);
        }
    );

    window.AJVYRAReleaseGate = {
        evaluate
    };

})();
