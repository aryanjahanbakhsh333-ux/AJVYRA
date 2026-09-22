class AJVYRAWebMultiplayerSession {
    constructor(options = {}) {
        this.sessionId = options.sessionId || null;
        this.localPlayerId = options.localPlayerId || null;

        this.players = new Map();
        this.state = "idle";

        this.maxPlayers = Math.max(
            1,
            options.maxPlayers || 16
        );

        this.listeners = new Map();
    }

    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, new Set());
        }

        this.listeners.get(event).add(callback);

        return () => this.off(event, callback);
    }

    off(event, callback) {
        const listeners = this.listeners.get(event);

        if (!listeners) {
            return;
        }

        listeners.delete(callback);
    }

    emit(event, data) {
        const listeners = this.listeners.get(event);

        if (!listeners) {
            return;
        }

        for (const callback of [...listeners]) {
            callback(data);
        }
    }

    start(sessionId) {
        if (!sessionId) {
            throw new Error("Multiplayer session ID is required.");
        }

        this.sessionId = sessionId;
        this.state = "active";

        this.emit("started", {
            sessionId
        });
    }

    addPlayer(player) {
        if (!player || !player.id) {
            throw new Error("Player must contain an id.");
        }

        if (
            this.players.size >= this.maxPlayers &&
            !this.players.has(player.id)
        ) {
            return false;
        }

        this.players.set(player.id, {
            ...player,
            connectedAt: Date.now()
        });

        this.emit("playerJoined", this.players.get(player.id));

        return true;
    }

    removePlayer(playerId) {
        const player = this.players.get(playerId);

        if (!player) {
            return false;
        }

        this.players.delete(playerId);

        this.emit("playerLeft", player);

        return true;
    }

    updatePlayerState(playerId, state) {
        const player = this.players.get(playerId);

        if (!player) {
            return false;
        }

        player.state = {
            ...(player.state || {}),
            ...state
        };

        player.lastUpdate = Date.now();

        this.emit("playerState", {
            playerId,
            state: player.state
        });

        return true;
    }

    getPlayer(playerId) {
        return this.players.get(playerId) || null;
    }

    getPlayers() {
        return [...this.players.values()];
    }

    getRemotePlayers() {
        return this.getPlayers().filter(
            player => player.id !== this.localPlayerId
        );
    }

    isFull() {
        return this.players.size >= this.maxPlayers;
    }

    end() {
        this.state = "ended";

        this.emit("ended", {
            sessionId: this.sessionId
        });

        this.players.clear();
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebMultiplayerSession =
        AJVYRAWebMultiplayerSession;
}
