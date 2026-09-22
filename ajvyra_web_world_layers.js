class AJVYRAWebWorldLayer {
    constructor(options = {}) {
        this.id = String(options.id || "");
        this.name = String(options.name || this.id);
        this.type = String(
            options.type || "tilemap"
        );

        this.visible =
            options.visible !== false;

        this.opacity = Math.max(
            0,
            Math.min(
                1,
                Number(options.opacity) || 1
            )
        );

        this.zIndex = Number(
            options.zIndex
        ) || 0;

        this.data = options.data || null;
    }
}


class AJVYRAWebWorldLayerManager {
    constructor() {
        this.layers = new Map();
    }

    addLayer(data) {
        const layer =
            data instanceof AJVYRAWebWorldLayer
                ? data
                : new AJVYRAWebWorldLayer(data);

        if (!layer.id) {
            return null;
        }

        this.layers.set(layer.id, layer);

        return layer;
    }

    removeLayer(id) {
        return this.layers.delete(String(id));
    }

    getLayer(id) {
        return this.layers.get(String(id)) || null;
    }

    setVisible(id, visible) {
        const layer = this.getLayer(id);

        if (!layer) {
            return false;
        }

        layer.visible = Boolean(visible);
        return true;
    }

    getRenderOrder() {
        return Array.from(
            this.layers.values()
        )
            .filter(layer => layer.visible)
            .sort(
                (a, b) =>
                    a.zIndex - b.zIndex
            );
    }

    clear() {
        this.layers.clear();
    }

    toJSON() {
        return Array.from(
            this.layers.values()
        ).map(layer => ({
            id: layer.id,
            name: layer.name,
            type: layer.type,
            visible: layer.visible,
            opacity: layer.opacity,
            zIndex: layer.zIndex,
            data: layer.data
        }));
    }
}
