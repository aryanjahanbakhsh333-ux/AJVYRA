class FinalSave {
    constructor() {
        this.key = "ajvyra_black_run_final";
    }

    save(data) {
        try {
            localStorage.setItem(
                this.key,
                JSON.stringify({
                    score: Number(data.score) || 0,
                    orbs: Number(data.orbs) || 0,
                    timestamp: Date.now()
                })
            );
        } catch (error) {
            console.warn("Save unavailable.");
        }
    }

    load() {
        try {
            const raw =
                localStorage.getItem(this.key);

            if (!raw) return null;

            return JSON.parse(raw);
        } catch (error) {
            return null;
        }
    }

    clear() {
        localStorage.removeItem(this.key);
    }
}
