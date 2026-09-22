class AJVYRAWebNetworkClient {
    constructor(options = {}) {
        this.url = options.url || null;
        this.socket = null;

        this.connected = false;
        this.connecting = false;

        this.reconnect = options.reconnect !== false;
        this.reconnectDelay = Math.max(250, options.reconnectDelay || 1500);
        this.maxReconnectDelay = Math.max(
            this.reconnectDelay,
            options.maxReconnectDelay || 10000
        );

        this.currentReconnectDelay = this.reconnectDelay;

        this.listeners = new Map();
    }

    on(event, callback) {
        if (typeof callback !== "function") {
            throw new TypeError("Network listener must be a function.");
        }

        if (!this.listeners.has(event)) {
            this.listeners.set(event, new Set());
        }

        this.listeners.get(event).add(callback);

        return () => {
            this.off(event, callback);
        };
    }

    off(event, callback) {
        const listeners = this.listeners.get(event);

        if (!listeners) {
            return;
        }

        listeners.delete(callback);

        if (listeners.size === 0) {
            this.listeners.delete(event);
        }
    }

    emit(event, data) {
        const listeners = this.listeners.get(event);

        if (!listeners) {
            return;
        }

        for (const callback of [...listeners]) {
            try {
                callback(data);
            } catch (error) {
                console.error("AJVYRA network listener error:", error);
            }
        }
    }

    connect(url = this.url) {
        if (typeof WebSocket === "undefined") {
            throw new Error("WebSocket is not available in this browser.");
        }

        if (this.connected || this.connecting) {
            return;
        }

        if (!url) {
            throw new Error("Network server URL is required.");
        }

        this.url = url;
        this.connecting = true;

        this.socket = new WebSocket(url);

        this.socket.addEventListener("open", () => {
            this.connected = true;
            this.connecting = false;
            this.currentReconnectDelay = this.reconnectDelay;

            this.emit("open");
        });

        this.socket.addEventListener("message", event => {
            this.emit("message", event.data);
        });

        this.socket.addEventListener("error", error => {
            this.emit("error", error);
        });

        this.socket.addEventListener("close", event => {
            this.connected = false;
            this.connecting = false;

            this.emit("close", event);

            if (this.reconnect && this.url) {
                this.scheduleReconnect();
            }
        });
    }

    scheduleReconnect() {
        const delay = this.currentReconnectDelay;

        setTimeout(() => {
            if (this.connected || this.connecting || !this.reconnect) {
                return;
            }

            try {
                this.connect(this.url);
            } catch (error) {
                this.emit("error", error);
            }

            this.currentReconnectDelay = Math.min(
                this.currentReconnectDelay * 2,
                this.maxReconnectDelay
            );
        }, delay);
    }

    send(data) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            return false;
        }

        const serialized =
            typeof data === "string"
                ? data
                : JSON.stringify(data);

        this.socket.send(serialized);
        return true;
    }

    close() {
        this.reconnect = false;

        if (this.socket) {
            this.socket.close();
        }

        this.socket = null;
        this.connected = false;
        this.connecting = false;
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebNetworkClient = AJVYRAWebNetworkClient;
}
