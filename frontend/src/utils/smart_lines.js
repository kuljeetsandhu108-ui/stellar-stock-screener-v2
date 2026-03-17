export const calculateSmartLines = (data) => {
    const horizontalLines = [];
    const trendLines =[];
    if (!data || data.length < 50) return { horizontalLines, trendLines };

    const pivots = { highs: [], lows:[] };
    const leftBars = 10;
    const rightBars = 10;

    // 1. Detect Major Institutional Pivots
    for (let i = leftBars; i < data.length - rightBars; i++) {
        let isHigh = true;
        let isLow = true;
        for (let j = 1; j <= leftBars; j++) {
            if (data[i-j].high >= data[i].high) isHigh = false;
            if (data[i-j].low <= data[i].low) isLow = false;
        }
        for (let j = 1; j <= rightBars; j++) {
            if (data[i+j].high > data[i].high) isHigh = false;
            if (data[i+j].low < data[i].low) isLow = false;
        }
        if (isHigh) pivots.highs.push({ index: i, time: data[i].time, price: data[i].high });
        if (isLow) pivots.lows.push({ index: i, time: data[i].time, price: data[i].low });
    }

    const currentPrice = data[data.length - 1].close;
    const hTolerance = currentPrice * 0.005; // 0.5% tolerance

    // 2. Horizontal S/R (1D K-Means Clustering Concept)
    const clusters = [];[...pivots.highs, ...pivots.lows].forEach(p => {
        let found = false;
        for (let c of clusters) {
            if (Math.abs(c.center - p.price) <= hTolerance) {
                c.prices.push(p.price);
                c.center = c.prices.reduce((a,b) => a+b, 0) / c.prices.length;
                found = true; break;
            }
        }
        if (!found) clusters.push({ center: p.price, prices: [p.price] });
    });

    const topClusters = clusters.filter(c => c.prices.length >= 3)
                                .sort((a,b) => b.prices.length - a.prices.length)
                                .slice(0, 5);

    topClusters.forEach(c => {
        horizontalLines.push({
            price: c.center,
            color: c.center > currentPrice ? 'rgba(248, 81, 73, 0.8)' : 'rgba(63, 185, 80, 0.8)',
            title: `S/R Zone (${c.prices.length} Hits)`,
        });
    });

    // 3. Diagonal Trendlines (Dense Vector Projection)
    const findBestTrendline = (pivotArr, isSupport) => {
        let bestLineData = null;
        let maxScore = 0; 
        const recent = pivotArr.slice(-20);

        for (let i = 0; i < recent.length - 1; i++) {
            for (let j = i + 1; j < recent.length; j++) {
                const p1 = recent[i];
                const p2 = recent[j];
                const slope = (p2.price - p1.price) / (p2.index - p1.index);
                
                const priceChangePct = Math.abs(p2.price - p1.price) / p1.price;
                const barChange = p2.index - p1.index;
                if (priceChangePct / barChange > 0.02) continue; 

                let isValid = true;
                let touches = 2;
                let breakCount = 0;
                const diagTolerance = currentPrice * 0.003; 

                for (let k = p1.index + 1; k < data.length; k++) {
                    if (k === p2.index) continue;
                    const proj = p1.price + slope * (k - p1.index);
                    const candle = data[k];

                    if (isSupport) {
                        if (candle.close < proj - diagTolerance) breakCount++;
                        if (Math.abs(candle.low - proj) <= diagTolerance) touches++;
                    } else {
                        if (candle.close > proj + diagTolerance) breakCount++;
                        if (Math.abs(candle.high - proj) <= diagTolerance) touches++;
                    }
                }

                if (breakCount <= 3) {
                    const score = touches + ((data.length - p1.index) / 100); 
                    if (score > maxScore) {
                        maxScore = score;
                        // Dense Projection: Calculate a point for EVERY candle so Lightweight Charts draws it perfectly
                        const lineData =[];
                        for (let k = p1.index; k < data.length; k++) {
                            const pointPrice = p1.price + slope * (k - p1.index);
                            lineData.push({ time: data[k].time, value: pointPrice });
                        }
                        bestLineData = lineData;
                    }
                }
            }
        }
        return bestLineData;
    };

    const resLine = findBestTrendline(pivots.highs, false);
    const supLine = findBestTrendline(pivots.lows, true);

    if (resLine) trendLines.push({ data: resLine, color: '#FF1744' }); 
    if (supLine) trendLines.push({ data: supLine, color: '#00E676' }); 

    return { horizontalLines, trendLines };
};
