export class AJVYRAFinalRenderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext("2d");
        this.frame = null;
        this.profile = {};
        this.time = 0;

        this.resize();
        window.addEventListener("resize", () => this.resize());
    }

    resize() {
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        const rect = this.canvas.getBoundingClientRect();

        this.canvas.width = Math.max(1, rect.width * dpr);
        this.canvas.height = Math.max(1, rect.height * dpr);

        this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        this.width = rect.width;
        this.height = rect.height;
    }

    setFrame(frame, profile) {
        this.frame = frame;
        this.profile = profile || {};
    }

    start() {
        const loop = (t) => {
            this.time = t / 1000;
            this.render();
            requestAnimationFrame(loop);
        };

        requestAnimationFrame(loop);
    }

    render() {
        if (!this.frame) return;

        const ctx = this.ctx;
        const w = this.width;
        const h = this.height;

        ctx.clearRect(0, 0, w, h);

        this.background(ctx, w, h);
        this.world(ctx, w, h);
        this.hud(ctx, w, h);
    }

    background(ctx, w, h) {
        const type = this.profile.background || "dark";

        ctx.fillStyle = "#050505";
        ctx.fillRect(0, 0, w, h);

        if (type === "space") {
            ctx.fillStyle = "#11152b";

            for (let i = 0; i < 90; i++) {
                const x = (i * 97) % w;
                const y = (i * 53) % h;
                ctx.fillRect(x, y, 1.5, 1.5);
            }
        }

        if (type === "road") {
            ctx.fillStyle = "#161616";
            ctx.fillRect(0, h * 0.55, w, h * 0.45);

            ctx.strokeStyle = "#777";
            ctx.setLineDash([30, 25]);
            ctx.beginPath();
            ctx.moveTo(0, h * 0.77);
            ctx.lineTo(w, h * 0.77);
            ctx.stroke();
            ctx.setLineDash([]);
        }

        if (type === "grid") {
            ctx.strokeStyle = "#202020";

            for (let x = 0; x < w; x += 50) {
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, h);
                ctx.stroke();
            }

            for (let y = 0; y < h; y += 50) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(w, y);
                ctx.stroke();
            }
        }
    }

    world(ctx, w, h) {
        const primary = this.profile.primary || "player";
        const pulse = Math.sin(this.time * 3) * 4;

        ctx.save();
        ctx.translate(w / 2, h / 2);

        ctx.beginPath();
        ctx.arc(0, pulse, 42, 0, Math.PI * 2);
        ctx.fillStyle = "#181818";
        ctx.fill();
        ctx.strokeStyle = "#f1f1f1";
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.font = "bold 14px system-ui";
        ctx.textAlign = "center";
        ctx.fillStyle = "#fff";
        ctx.fillText(primary.toUpperCase(), 0, 5);

        ctx.restore();
    }

    hud(ctx, w, h) {
        ctx.fillStyle = "rgba(0,0,0,.75)";
        ctx.fillRect(0, 0, w, 76);

        ctx.fillStyle = "#fff";
        ctx.font = "bold 18px system-ui";
        ctx.fillText(this.frame.title, 18, 28);

        ctx.font = "13px system-ui";
        ctx.fillStyle = "#aaa";

        const state = this.frame.state || {};
        const entries = Object.entries(state)
            .filter(([_, value]) =>
                typeof value === "number" ||
                typeof value === "string" ||
                typeof value === "boolean"
            )
            .slice(0, 5);

        entries.forEach(([key, value], i) => {
            ctx.fillText(
                `${key}: ${value}`,
                18 + i * Math.min(180, w / 5),
                54
            );
        });

        if (this.frame.completed) {
            ctx.fillStyle = "#fff";
            ctx.font = "bold 30px system-ui";
            ctx.textAlign = "center";
            ctx.fillText("COMPLETED", w / 2, h / 2 - 75);
            ctx.textAlign = "left";
        }
    }
}
