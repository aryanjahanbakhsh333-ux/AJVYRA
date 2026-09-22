class AJVYRAWebNetworkManager {
    constructor(options = {}) {
        this.gameId = options.gameId || "unknown";

        this.protocol =
            options.protocol ||
            new AJVYRAWebNetworkProtocol({
                gameId: this.gameId
            });

        this.client =
            options.client ||
            new AJVYRAWebNetworkClient({
                url: options.url,
                reconnect: options.reconnect
            });

        this.session =
            options.session ||
            new AJVYRAWebMultiplayerSession({
                localPlayerId: options.localPlayerId,
                maxPlayers: options.maxPlayers
            });

        this.social =
            options.social ||
            new AJVYRAWebRealtimeSocial();

        this.sequence = 0;

        this.listeners = new Map();

        this.bindClient();
    }

    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, new Set());
        }

        this.listeners.get(event).add(callback);

        return () => {
            this.listeners.get(event)?.delete(callback);
        };
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

    bindClient() {
        this.client.on("open", () => {
            this.emit("connected");
        });

        this.client.on("close", event => {
            this.emit("disconnected", event);
        });

        this.client.on("error", error => {
            this.emit("error", error);
        });

        this.client.on("message", raw => {
            this.handleIncoming(raw);
        });
    }

    connect(url) {
        this.client.connect(url);
    }

    sendMessage(type, payload = {}) {
        const message = this.protocol.createMessage(
            type,
            payload,
            {
                sequence: ++this.sequence
            }
        );

        return this.client.send(message);
    }

    joinSession(player) {
        if (!player || !player.id) {
            throw new Error("A valid player is required.");
        }

        this.session.localPlayerId = player.id;

        return this.sendMessage(
            "session.join",
            {
                playerId: player.id,
                displayName:
                    player.displayName ||
                    player.name ||
                    "Player"
            }
        );
    }

    leaveSession() {
        const playerId = this.session.localPlayerId;

        if (!playerId) {
            return false;
        }

        return this.sendMessage(
            "session.leave",
            {
                playerId
            }
        );
    }

    sendPlayerState(state) {
        const playerId =
            this.session.localPlayerId;

        if (!playerId) {
            return false;
        }

        return this.sendMessage(
            "player.state",
            {
                playerId,
                state
            }
        );
    }

    sendChat(text) {
        const playerId =
            this.session.localPlayerId;

        if (!playerId) {
            return false;
        }

        return this.sendMessage(
            "social.chat",
            {
                playerId,
                text: String(text).slice(0, 500)
            }
        );
    }

    sendGameEvent(eventName, data = {}) {
        return this.sendMessage(
            "game.event",
            {
                eventName,
                data
            }
        );
    }

    handleIncoming(raw) {
        let message;

        try {
            message =
                typeof raw === "string"
                    ? this.protocol.decode(raw)
                    : raw;
        } catch (error) {
            this.emit("protocolError", error);
            return;
        }

        switch (message.type) {
            case "session.join":
                this.session.addPlayer({
                    id: message.payload.playerId,
                    displayName:
                        message.payload.displayName
                });
                break;

            case "session.leave":
                this.session.removePlayer(
                    message.payload.playerId
                );
                break;

            case "player.state":
                this.session.updatePlayerState(
                    message.payload.playerId,
                    message.payload.state || {}
                );
                break;

            case "social.chat":
                this.social.addChatMessage({
                    playerId:
                        message.payload.playerId,
                    text:
                        message.payload.text,
                    timestamp:
                        message.timestamp
                });
                break;

            case "game.event":
                this.emit(
                    "gameEvent",
                    message.payload
                );
                break;

            default:
                this.emit(
                    "unknownMessage",
                    message
                );
        }

        this.emit("message", message);
    }

    disconnect() {
        this.client.close();
        this.session.end();
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebNetworkManager =
        AJVYRAWebNetworkManager;
}
