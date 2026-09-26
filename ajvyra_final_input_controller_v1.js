export class AJVYRAInputController {
    constructor({ action }) {
        this.action = action;
        this.keys = new Set();

        window.addEventListener("keydown", (event) => {
            if (this.keys.has(event.code)) return;

            this.keys.add(event.code);

            const mapped = {
                Space: "primary",
                Enter: "primary",
                KeyE: "utility",
                KeyF: "finish",
                KeyR: "secondary",
                ArrowUp: "primary",
                ArrowRight: "primary",
                ArrowLeft: "secondary",
                ShiftLeft: "utility",
            }[event.code];

            if (mapped) this.action(mapped);
        });

        window.addEventListener("keyup", (event) => {
            this.keys.delete(event.code);
        });

        document.querySelectorAll("[data-action]")
            .forEach(button => {
                const handler = () => {
                    this.action(button.dataset.action);
                };

                button.addEventListener("click", handler);
                button.addEventListener("touchstart", handler, {
                    passive: true,
                });
            });
    }
}
