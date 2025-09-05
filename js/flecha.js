class ArrowDrawer {
    constructor(overlayId, targetId) {
        this.canvas = document.getElementById(overlayId);
        this.ctx = this.canvas.getContext("2d");
        this.target = document.getElementById(targetId);

        this.mouse = { x: null, y: null };

        this.updateCanvasSize = this.updateCanvasSize.bind(this);
        this.handleMouseMove = this.handleMouseMove.bind(this);
        this.animate = this.animate.bind(this);

        this.init();
    }

    init() {
        this.updateCanvasSize();
        window.addEventListener("resize", this.updateCanvasSize);
        window.addEventListener("mousemove", this.handleMouseMove);
        requestAnimationFrame(this.animate);
    }

    updateCanvasSize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    handleMouseMove(e) {
        this.mouse.x = e.clientX;
        this.mouse.y = e.clientY;
    }

    drawArrow() {
        const { x: x0, y: y0 } = this.mouse;

        if (x0 === null || y0 === null) return;

        const rect = this.target.getBoundingClientRect();
        const cx = rect.left + rect.width / 2;
        const cy = rect.top + rect.height / 2;

        const angle = Math.atan2(cy - y0, cx - x0);
        const x1 = cx - Math.cos(angle) * (rect.width / 2 + 12);
        const y1 = cy - Math.sin(angle) * (rect.height / 2 + 12);

        const midX = (x0 + x1) / 2;
        const midY = (y0 + y1) / 2;
        const offset = Math.min(200, Math.hypot(x1 - x0, y1 - y0) * 0.5);
        const t = Math.max(-1, Math.min(1, (y0 - y1) / 200));
        const controlX = midX;
        const controlY = midY + offset * t;

        const r = Math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2);
        const opacity = Math.min(0.75, (r - Math.max(rect.width, rect.height) / 2) / 750);

        const ctx = this.ctx;
        ctx.strokeStyle = `rgba(212,154,54,${opacity})`;
        ctx.lineWidth = 1;

        ctx.save();
        ctx.beginPath();
        ctx.moveTo(x0, y0);
        ctx.quadraticCurveTo(controlX, controlY, x1, y1);
        ctx.setLineDash([10, 4]);
        ctx.stroke();
        ctx.restore();

        const headAngle = Math.atan2(y1 - controlY, x1 - controlX);
        const headLength = 10;
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(
            x1 - headLength * Math.cos(headAngle - Math.PI / 6),
            y1 - headLength * Math.sin(headAngle - Math.PI / 6)
        );
        ctx.moveTo(x1, y1);
        ctx.lineTo(
            x1 - headLength * Math.cos(headAngle + Math.PI / 6),
            y1 - headLength * Math.sin(headAngle + Math.PI / 6)
        );
        ctx.stroke();
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.drawArrow();
        requestAnimationFrame(this.animate);
    }
}
