(function (global) {
    "use strict";

    class AJVYRAProfessionalGameSave {
        constructor(options = {}) {
            this.dbName =
                options.dbName ||
                "AJVYRA_PROFESSIONAL_GAMES";

            this.version = 1;

            this.storeName =
                "game_progress";

            this.db = null;
        }

        async open() {
            if (
                this.db
            ) {
                return this.db;
            }

            if (
                !("indexedDB" in window)
            ) {
                throw new Error(
                    "IndexedDB is not available."
                );
            }

            this.db =
                await new Promise(
                    (resolve, reject) => {
                        const request =
                            indexedDB.open(
                                this.dbName,
                                this.version
                            );

                        request.onupgradeneeded =
                            () => {
                                const db =
                                    request.result;

                                if (
                                    !db.objectStoreNames.contains(
                                        this.storeName
                                    )
                                ) {
                                    db.createObjectStore(
                                        this.storeName,
                                        {
                                            keyPath:
                                                "gameId"
                                        }
                                    );
                                }
                            };

                        request.onsuccess =
                            () => {
                                resolve(
                                    request.result
                                );
                            };

                        request.onerror =
                            () => {
                                reject(
                                    request.error ||
                                    new Error(
                                        "Failed to open game database."
                                    )
                                );
                            };
                    }
                );

            return this.db;
        }

        async save(
            gameId,
            payload
        ) {
            const db =
                await this.open();

            const record = {
                gameId: String(gameId),
                payload:
                    JSON.parse(
                        JSON.stringify(
                            payload || {}
                        )
                    ),
                updatedAt:
                    Date.now()
            };

            return new Promise(
                (resolve, reject) => {
                    const transaction =
                        db.transaction(
                            [this.storeName],
                            "readwrite"
                        );

                    const store =
                        transaction.objectStore(
                            this.storeName
                        );

                    store.put(record);

                    transaction.oncomplete =
                        () => {
                            resolve(record);
                        };

                    transaction.onerror =
                        () => {
                            reject(
                                transaction.error ||
                                new Error(
                                    "Game save failed."
                                )
                            );
                        };
                }
            );
        }

        async load(gameId) {
            const db =
                await this.open();

            return new Promise(
                (resolve, reject) => {
                    const transaction =
                        db.transaction(
                            [this.storeName],
                            "readonly"
                        );

                    const store =
                        transaction.objectStore(
                            this.storeName
                        );

                    const request =
                        store.get(
                            String(gameId)
                        );

                    request.onsuccess =
                        () => {
                            resolve(
                                request.result ||
                                null
                            );
                        };

                    request.onerror =
                        () => {
                            reject(
                                request.error ||
                                new Error(
                                    "Game load failed."
                                )
                            );
                        };
                }
            );
        }

        async remove(gameId) {
            const db =
                await this.open();

            return new Promise(
                (resolve, reject) => {
                    const transaction =
                        db.transaction(
                            [this.storeName],
                            "readwrite"
                        );

                    transaction
                        .objectStore(
                            this.storeName
                        )
                        .delete(
                            String(gameId)
                        );

                    transaction.oncomplete =
                        () => resolve(true);

                    transaction.onerror =
                        () =>
                            reject(
                                transaction.error
                            );
                }
            );
        }

        async list() {
            const db =
                await this.open();

            return new Promise(
                (resolve, reject) => {
                    const transaction =
                        db.transaction(
                            [this.storeName],
                            "readonly"
                        );

                    const request =
                        transaction
                            .objectStore(
                                this.storeName
                            )
                            .getAll();

                    request.onsuccess =
                        () => {
                            resolve(
                                request.result || []
                            );
                        };

                    request.onerror =
                        () => {
                            reject(
                                request.error
                            );
                        };
                }
            );
        }

        async clear() {
            const db =
                await this.open();

            return new Promise(
                (resolve, reject) => {
                    const transaction =
                        db.transaction(
                            [this.storeName],
                            "readwrite"
                        );

                    transaction
                        .objectStore(
                            this.storeName
                        )
                        .clear();

                    transaction.oncomplete =
                        () => resolve(true);

                    transaction.onerror =
                        () =>
                            reject(
                                transaction.error
                            );
                }
            );
        }
    }

    global.AJVYRAProfessionalGameSave =
        AJVYRAProfessionalGameSave;

})(window);
