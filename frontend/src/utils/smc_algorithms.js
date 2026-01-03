// --- SMART MONEY CONCEPTS ENGINE ---

export const calculateSMC = (data) => {
    const fvgs = [];
    const orderBlocks = [];
    const markers = [];
    const coloredCandles = []; // To override colors for FVG
    const priceLines = []; // To draw zones

    // We need at least 3 candles to find an FVG
    for (let i = 2; i < data.length; i++) {
        const curr = data[i];
        const prev = data[i-1];
        const prev2 = data[i-2];

        // --- 1. FAIR VALUE GAPS (FVG) ---
        
        // Bullish FVG: (High of Candle i-2) < (Low of Candle i)
        if (prev2.high < curr.low) {
            // Check for significant size (optional, keeps chart clean)
            const gapSize = curr.low - prev2.high;
            if (gapSize > (curr.close * 0.0005)) { // 0.05% filter
                fvgs.push({
                    type: 'Bullish FVG',
                    top: curr.low,
                    bottom: prev2.high,
                    index: i-1 // The middle candle is the FVG candle
                });
                // Color the middle candle Yellow (Imbalance)
                coloredCandles.push({ time: prev.time, color: '#FBBF24', wickColor: '#FBBF24', borderColor: '#FBBF24' });
            }
        }

        // Bearish FVG: (Low of Candle i-2) > (High of Candle i)
        if (prev2.low > curr.high) {
            const gapSize = prev2.low - curr.high;
            if (gapSize > (curr.close * 0.0005)) {
                fvgs.push({
                    type: 'Bearish FVG',
                    top: prev2.low,
                    bottom: curr.high,
                    index: i-1
                });
                // Color the middle candle Purple (Imbalance)
                coloredCandles.push({ time: prev.time, color: '#A855F7', wickColor: '#A855F7', borderColor: '#A855F7' });
            }
        }

        // --- 2. ORDER BLOCKS (Simplified) ---
        // Bullish OB: Lowest Down-candle before a strong Up-move that breaks structure
        // Logic: Current is Green, Previous was Red, Current Body engulfs Previous
        const isBullishEngulfing = curr.close > curr.open && prev.close < prev.open && curr.close > prev.open && curr.open < prev.close;
        
        if (isBullishEngulfing) {
            orderBlocks.push({ type: 'Bullish OB', price: prev.low, time: prev.time });
            markers.push({
                time: prev.time,
                position: 'belowBar',
                color: '#3FB950',
                shape: 'arrowUp',
                text: 'OB',
            });
        }

        // Bearish OB
        const isBearishEngulfing = curr.close < curr.open && prev.close > prev.open && curr.close < prev.open && curr.open > prev.close;
        
        if (isBearishEngulfing) {
            orderBlocks.push({ type: 'Bearish OB', price: prev.high, time: prev.time });
            markers.push({
                time: prev.time,
                position: 'aboveBar',
                color: '#F85149',
                shape: 'arrowDown',
                text: 'OB',
            });
        }
    }

    // --- 3. CALCULATE ACTIVE ZONES (For Price Lines) ---
    // We only take the last 2 valid FVGs to avoid clutter
    const recentFVGs = fvgs.slice(-2);
    
    recentFVGs.forEach(fvg => {
        if (fvg.type === 'Bullish FVG') {
            priceLines.push({ price: fvg.bottom, color: '#FBBF24', title: 'Demand Gap' });
        } else {
            priceLines.push({ price: fvg.top, color: '#A855F7', title: 'Supply Gap' });
        }
    });

    return { markers, coloredCandles, priceLines };
};