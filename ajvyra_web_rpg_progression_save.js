class AJVYRAWebRPGProgressionSave {
    constructor(options = {}) {
        this.databaseName =
            options.databaseName || "AJVYRA_GAME_DATABASE";

        this.storeName =
            options.storeName || "game_saves";

        this.version = 1;
        this.db = null;
    }

    async open() {
        if (this.db) {
            return this.db;
        }

        if (!("indexedDB" in window)) {
            throw new Error("IndexedDB is not supported.");
        }

        this.db = await new Promise((resolve, reject) => {
            const request = indexedDB.open(
                this.databaseName,
                this.version
            );

            request.onerror = () => {
                reject(request.error);
            };

            request.onsuccess = () => {
                resolve(request.result);
            };

            request.onupgradeneeded = event => {
                const database = event.target.result;

                if (!database.objectStoreNames.contains(this.storeName)) {
                    database.createObjectStore(
                        this.storeName,
                        { keyPath: "saveId" }
                    );
                }
            };
        });

        return this.db;
    }

    async save(saveId, state) {
        const database = await this.open();

        const payload = {
            saveId: String(saveId),
            updatedAt: Date.now(),
            state
        };

        return new Promise((resolve, reject) => {
            const transaction = database.transaction(
                this.storeName,
                "readwrite"
            );

            const store = transaction.objectStore(
                this.storeName
            );

            const request = store.put(payload);

            request.onsuccess = () => resolve(true);
            request.onerror = () => reject(request.error);
        });
    }

    async load(saveId) {
        const database = await this.open();

        return new Promise((resolve, reject) => {
            const transaction = database.transaction(
                this.storeName,
                "readonly"
            );

            const store = transaction.objectStore(
                this.storeName
            );

            const request = store.get(String(saveId));

            request.onsuccess = () => {
                resolve(request.result?.state || null);
            };

            request.onerror = () => reject(request.error);
        });
    }

    async delete(saveId) {
        const database = await this.open();

        return new Promise((resolve, reject) => {
            const transaction = database.transaction(
                this.storeName,
                "readwrite"
            );

            const store = transaction.objectStore(
                this.storeName
            );

            const request = store.delete(String(saveId));

            request.onsuccess = () => resolve(true);
            request.onerror = () => reject(request.error);
        });
    }

    async listSaves() {
        const database = await this.open();

        return new Promise((resolve, reject) => {
            const transaction = database.transaction(
                this.storeName,
                "readonly"
            );

            const store = transaction.objectStore(
                this.storeName
            );

            const request = store.getAll();

            request.onsuccess = () => {
                resolve(
                    request.result.map(item => ({
                        saveId: item.saveId,
                        updatedAt: item.updatedAt
                    }))
                );
            };

            request.onerror = () => reject(request.error);
        });
    }

    async saveGameState(saveId, gameState) {
        return this.save(saveId, gameState);
    }

    async loadGameState(saveId) {
        return this.load(saveId);
    }
}
