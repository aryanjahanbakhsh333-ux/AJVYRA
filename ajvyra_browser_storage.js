(() => {
    "use strict";

    class AJVYRA_BrowserStorage {
        constructor(prefix = "AJVYRA_") {
            this.prefix = prefix;
        }

        key(id) {
            return `${this.prefix}${id}`;
        }

        save(id, data) {
            try {
                localStorage.setItem(
                    this.key(id),
                    JSON.stringify(data)
                );

                return true;
            } catch {
                return false;
            }
        }

        load(id, fallback = null) {
            try {
                const raw =
                    localStorage.getItem(
                        this.key(id)
                    );

                if (!raw) return fallback;

                return JSON.parse(raw);
            } catch {
                return fallback;
            }
        }

        remove(id) {
            try {
                localStorage.removeItem(
                    this.key(id)
                );
            } catch {}
        }

        clearGame(id) {
            this.remove(id);
        }
    }

    window.AJVYRA_BrowserStorage =
        AJVYRA_BrowserStorage;
})();
