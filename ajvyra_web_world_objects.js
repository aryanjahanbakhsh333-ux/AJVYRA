class AJVYRAWebWorldObject {
    constructor(data = {}) {
        this.id = String(data.id || "");
        this.type = String(
            data.type || "object"
        );

        this.x = Number(data.x) || 0;
        this.y = Number(data.y) || 0;

        this.width = Math.max(
            1,
            Number(data.width) || 32
        );

        this.height = Math.max(
            1,
            Number(data.height) || 32
        );

        this.active =
            data.active !== false;

        this.solid =
            Boolean(data.solid);

        this.interactable =
            Boolean(data.interactable);

        this.properties =
            data.properties || {};
    }

    containsPoint(x, y) {
        return (
            x >= this.x &&
            x <= this.x + this.width &&
            y >= this.y &&
            y <= this.y + this.height
        );
    }

    intersects(other) {
        if (!other) {
            return false;
        }

        return (
            this.x <
                other.x + other.width &&
            this.x + this.width >
                other.x &&
            this.y <
                other.y + other.height &&
            this.y + this.height >
                other.y
        );
    }

    setPosition(x, y) {
        this.x = Number(x) || 0;
        this.y = Number(y) || 0;
    }

    toJSON() {
        return {
            id: this.id,
            type: this.type,
            x: this.x,
            y: this.y,
            width: this.width,
            height: this.height,
            active: this.active,
            solid: this.solid,
            interactable: this.interactable,
            properties: this.properties
        };
    }
}


class AJVYRAWebWorldObjectManager {
    constructor() {
        this.objects = new Map();
    }

    add(data) {
        const object =
            data instanceof AJVYRAWebWorldObject
                ? data
                : new AJVYRAWebWorldObject(data);

        if (!object.id) {
            return null;
        }

        this.objects.set(
            object.id,
            object
        );

        return object;
    }

    remove(id) {
        return this.objects.delete(
            String(id)
        );
    }

    get(id) {
        return this.objects.get(
            String(id)
        ) || null;
    }

    getByType(type) {
        return Array.from(
            this.objects.values()
        ).filter(
            object =>
                object.type === String(type) &&
                object.active
        );
    }

    findAt(x, y) {
        return Array.from(
            this.objects.values()
        ).filter(
            object =>
                object.active &&
                object.containsPoint(x, y)
        );
    }

    getSolidObjects() {
        return Array.from(
            this.objects.values()
        ).filter(
            object =>
                object.active &&
                object.solid
        );
    }

    clear() {
        this.objects.clear();
    }

    toJSON() {
        return Array.from(
            this.objects.values()
        ).map(
            object => object.toJSON()
        );
    }
}
