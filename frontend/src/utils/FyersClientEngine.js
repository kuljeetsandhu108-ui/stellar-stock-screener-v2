export class FyersClientEngine {
    constructor(token, symbol, onTick) {
        this.token = token;
        this.symbol = symbol;
        this.onTick = onTick;
        this.socket = null;
        this.isConnected = false;
        this.lastPrice = null;
    }

    connect() {
        if (!window.FyersSocket || !this.token) return;

        this.socket = new window.FyersSocket(this.token);

        this.socket.onopen = () => {
            this.isConnected = true;
            this.subscribe();
        };

        this.socket.onmessage = (msg) => {
            try {
                const tick = msg.d?.[0] || msg[0]; 
                if (tick && tick.v && tick.v.lp) {
                    const price = parseFloat(tick.v.lp);
                    if (this.onTick) this.onTick({ price: price });
                }
            } catch (e) {}
        };

        this.socket.connect();
    }

    subscribe() {
        if (this.socket && this.isConnected) {
            this.socket.subscribe([this.symbol]); 
            this.socket.mode(this.socket.MODE_LTP);
        }
    }

    disconnect() {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
    }
}