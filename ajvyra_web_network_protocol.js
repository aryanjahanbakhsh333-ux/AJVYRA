class AJVYRAWebNetworkProtocol {
    constructor(options = {}) {
        this.version = options.version || "1.0";
        this.gameId = options.gameId || "unknown";
        this.sessionId = options.sessionId || null;
    }

    createMessage(type, payload = {}, options = {}) {
        return {
            protocol: "AJVYRA",
            version: this.version,
            type,
            gameId: options.gameId || this.gameId,
            sessionId: options.sessionId || this.sessionId,
            timestamp: Date.now(),
            sequence: Number.isInteger(options.sequence)
                ? options.sequence
                : 0,
            payload
        };
    }

    encode(message) {
        return JSON.stringify(message);
    }

    decode(raw) {
        if (typeof raw !== "string") {
            throw new TypeError("Network message must be a string.");
        }

        const message = JSON.parse(raw);

        if (!message || typeof message !== "object") {
            throw new Error("Invalid AJVYRA network message.");
        }

        if (message.protocol !== "AJVYRA") {
            throw new Error("Unknown network protocol.");
        }

        if (!message.type) {
            throw new Error("Network message type is missing.");
        }

        return message;
    }

    createJoinRequest(player) {
        return this.createMessage("session.join", {
            playerId: player.id,
            displayName: player.displayName || player.name || "Player"
        });
    }

    createLeaveRequest(playerId) {
        return this.createMessage("session.leave", {
            playerId
        });
    }

    createPlayerState(playerId, state) {
        return this.createMessage("player.state", {
            playerId,
            state
        });
    }

    createGameEvent(eventName, data = {}) {
        return this.createMessage("game.event", {
            eventName,
            data
        });
    }

    createChatMessage(playerId, text) {
        return this.createMessage("social.chat", {
            playerId,
            text: String(text).slice(0, 500)
        });
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebNetworkProtocol = AJVYRAWebNetworkProtocol;
}
