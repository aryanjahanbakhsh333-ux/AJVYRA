class AJVYRAWebWorldTileMap {
    constructor(options = {}) {
        this.id = String(options.id || "map");
        this.columns = Math.max(
            1,
            Math.floor(Number(options.columns) || 1)
        );
        this.rows = Math.max(
            1,
            Math.floor(Number(options.rows) || 1)
        );
        this.tileSize = Math.max(
            1,
            Number(options.tileSize) || 32
        );

        this.tiles = Array.isArray(options.tiles)
            ? [...options.tiles]
            : new Array(this.columns * this.rows).fill(0);

        this.collision = Array.isArray(options.collision)
            ? [...options.collision]
            : new Array(this.columns * this.rows).fill(0);

        this.ensureSize();
    }

    ensureSize() {
        const total = this.columns * this.rows;

        if (this.tiles.length < total) {
            this.tiles.push(
                ...new Array(total - this.tiles.length).fill(0)
            );
        }

        if (this.collision.length < total) {
            this.collision.push(
                ...new Array(
                    total - this.collision.length
                ).fill(0)
            );
        }

        this.tiles.length = total;
        this.collision.length = total;
    }

    index(column, row) {
        return row * this.columns + column;
    }

    isInside(column, row) {
        return (
            column >= 0 &&
            row >= 0 &&
            column < this.columns &&
            row < this.rows
        );
    }

    getTile(column, row) {
        if (!this.isInside(column, row)) {
            return null;
        }

        return this.tiles[
            this.index(column, row)
        ];
    }

    setTile(column, row, tileId) {
        if (!this.isInside(column, row)) {
            return false;
        }

        this.tiles[
            this.index(column, row)
        ] = tileId;

        return true;
    }

    getCollision(column, row) {
        if (!this.isInside(column, row)) {
            return 1;
        }

        return this.collision[
            this.index(column, row)
        ];
    }

    setCollision(column, row, value) {
        if (!this.isInside(column, row)) {
            return false;
        }

        this.collision[
            this.index(column, row)
        ] = value ? 1 : 0;

        return true;
    }

    worldToTile(x, y) {
        return {
            column: Math.floor(x / this.tileSize),
            row: Math.floor(y / this.tileSize)
        };
    }

    tileToWorld(column, row) {
        return {
            x: column * this.tileSize,
            y: row * this.tileSize
        };
    }

    isBlocked(column, row) {
        return this.getCollision(column, row) === 1;
    }

    getVisibleRange(camera, width, height) {
        const left = Math.max(
            0,
            Math.floor(camera.x / this.tileSize)
        );

        const top = Math.max(
            0,
            Math.floor(camera.y / this.tileSize)
        );

        const right = Math.min(
            this.columns - 1,
            Math.ceil(
                (camera.x + width) /
                this.tileSize
            )
        );

        const bottom = Math.min(
            this.rows - 1,
            Math.ceil(
                (camera.y + height) /
                this.tileSize
            )
        );

        return {
            left,
            top,
            right,
            bottom
        };
    }

    toJSON() {
        return {
            id: this.id,
            columns: this.columns,
            rows: this.rows,
            tileSize: this.tileSize,
            tiles: [...this.tiles],
            collision: [...this.collision]
        };
    }

    static fromJSON(data) {
        return new AJVYRAWebWorldTileMap(data);
    }
}
