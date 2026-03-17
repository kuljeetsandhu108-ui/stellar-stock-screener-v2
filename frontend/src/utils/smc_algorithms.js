// --- BIG BELUGA SMART MONEY CONCEPTS (SMC) ENGINE ---

export const calculateSMC = (data) => {
    const markers =[];
    const coloredCandles = [];
    const lines =[];

    // Guard: Need enough data to calculate 5-bar fractals
    if (!data || !Array.isArray(data) || data.length < 20) return { markers, coloredCandles, lines };

    let swings =[];
    let trend = 0; 
    let lastSwingHigh = null;
    let lastSwingLow = null;
    
    let activeBullishOB =[];
    let activeBearishOB = [];
    let activeBullishFVG =[];
    let activeBearishFVG = [];

    // Dynamic threshold: filter out microscopic noise
    const minGap = data[data.length-1].close * 0.0005;
    const lastTime = data[data.length-1].time;

    // --- MAIN PASS: PROCESS EVERY CANDLE ---
    for (let i = 5; i < data.length - 5; i++) {
        const curr = data[i];
        const prev = data[i-1];
        const prev2 = data[i-2];

        if (!curr || !prev || !prev2) continue;

        // 1. FAIR VALUE GAPS (FVG)
        if (prev2.high < curr.low && (curr.low - prev2.high) > minGap) {
            activeBullishFVG.push({ top: curr.low, bottom: prev2.high, time: prev.time, mitigated: false });
        }
        if (prev2.low > curr.high && (prev2.low - curr.high) > minGap) {
            activeBearishFVG.push({ top: prev2.low, bottom: curr.high, time: prev.time, mitigated: false });
        }

        // 2. FRACTAL SWINGS
        let isHigh = true, isLow = true;
        for (let j = 1; j <= 5; j++) {
            if (!data[i-j] || !data[i+j]) continue;
            if (data[i-j].high >= curr.high || data[i+j].high >= curr.high) isHigh = false;
            if (data[i-j].low <= curr.low || data[i+j].low <= curr.low) isLow = false;
        }

        if (isHigh) {
            lastSwingHigh = { index: i, time: curr.time, price: curr.high };
            swings.push({ ...lastSwingHigh, type: 'high' });
        }
        if (isLow) {
            lastSwingLow = { index: i, time: curr.time, price: curr.low };
            swings.push({ ...lastSwingLow, type: 'low' });
        }

        // 3. MARKET STRUCTURE & ORDER BLOCKS
        if (lastSwingHigh && curr.close > lastSwingHigh.price) {
            const isChoch = trend === -1 || trend === 0;
            trend = 1;
            
            // Structure Line
            lines.push({
                data:[{ time: lastSwingHigh.time, value: lastSwingHigh.price }, { time: curr.time, value: lastSwingHigh.price }],
                color: '#089981', lineWidth: 1, lineStyle: isChoch ? 0 : 2, showLabel: false
            });
            // FIX: Valid shape 'arrowUp' with text overlay
            markers.push({ time: curr.time, position: 'belowBar', color: '#089981', shape: 'arrowUp', text: isChoch ? 'CHoCH' : 'BOS', size: 1 });

            if (lastSwingLow) {
                let obCandle = data[lastSwingLow.index];
                for (let k = lastSwingLow.index; k < i; k++) {
                    if (data[k] && data[k].close < data[k].open && data[k].low <= obCandle.low) obCandle = data[k];
                }
                activeBullishOB.push({ top: obCandle.high, bottom: obCandle.low, time: obCandle.time, mitigated: false });
            }
            lastSwingHigh = null; 
        }

        if (lastSwingLow && curr.close < lastSwingLow.price) {
            const isChoch = trend === 1 || trend === 0;
            trend = -1;

            lines.push({
                data:[{ time: lastSwingLow.time, value: lastSwingLow.price }, { time: curr.time, value: lastSwingLow.price }],
                color: '#f23645', lineWidth: 1, lineStyle: isChoch ? 0 : 2, showLabel: false
            });
            // FIX: Valid shape 'arrowDown' with text overlay
            markers.push({ time: curr.time, position: 'aboveBar', color: '#f23645', shape: 'arrowDown', text: isChoch ? 'CHoCH' : 'BOS', size: 1 });

            if (lastSwingHigh) {
                let obCandle = data[lastSwingHigh.index];
                for (let k = lastSwingHigh.index; k < i; k++) {
                    if (data[k] && data[k].close > data[k].open && data[k].high >= obCandle.high) obCandle = data[k];
                }
                activeBearishOB.push({ top: obCandle.high, bottom: obCandle.low, time: obCandle.time, mitigated: false });
            }
            lastSwingLow = null; 
        }

        // 4. MITIGATION ENGINE
        const mt = curr.close * 0.0001; 
        activeBullishFVG.forEach(f => { if (curr.low <= f.bottom + mt) f.mitigated = true; });
        activeBearishFVG.forEach(f => { if (curr.high >= f.top - mt) f.mitigated = true; });
        activeBullishOB.forEach(o => { if (curr.low <= o.bottom + mt) o.mitigated = true; });
        activeBearishOB.forEach(o => { if (curr.high >= o.top - mt) o.mitigated = true; });

        activeBullishFVG = activeBullishFVG.filter(f => !f.mitigated);
        activeBearishFVG = activeBearishFVG.filter(f => !f.mitigated);
        activeBullishOB = activeBullishOB.filter(o => !o.mitigated);
        activeBearishOB = activeBearishOB.filter(o => !o.mitigated);
    }

    // --- OUTPUT PREPARATION ---
    const displayBullFVG = activeBullishFVG.slice(-3);
    const displayBearFVG = activeBearishFVG.slice(-3);
    const displayBullOB = activeBullishOB.slice(-3);
    const displayBearOB = activeBearishOB.slice(-3);

    const calcPct = (top, btm) => ((Math.abs(top - btm) / btm) * 100).toFixed(2);

    // FVGs
    displayBullFVG.forEach(z => {
        coloredCandles.push({ time: z.time, color: 'rgba(8, 153, 129, 0.3)', wickColor: '#089981' });
        // showLabel: true puts the text right on the price axis exactly like the screenshot
        lines.push({ data:[{time: z.time, value: z.top}, {time: lastTime, value: z.top}], color: '#089981', lineWidth: 1, lineStyle: 2, showLabel: true, title: `${calcPct(z.top, z.bottom)}% FVG` });
        lines.push({ data:[{time: z.time, value: z.bottom}, {time: lastTime, value: z.bottom}], color: '#089981', lineWidth: 1, lineStyle: 2, showLabel: false });
    });
    
    displayBearFVG.forEach(z => {
        coloredCandles.push({ time: z.time, color: 'rgba(242, 54, 69, 0.3)', wickColor: '#f23645' });
        lines.push({ data:[{time: z.time, value: z.top}, {time: lastTime, value: z.top}], color: '#f23645', lineWidth: 1, lineStyle: 2, showLabel: true, title: `${calcPct(z.top, z.bottom)}% FVG` });
        lines.push({ data:[{time: z.time, value: z.bottom}, {time: lastTime, value: z.bottom}], color: '#f23645', lineWidth: 1, lineStyle: 2, showLabel: false });
    });

    // OBs
    displayBullOB.forEach(z => {
        lines.push({ data:[{time: z.time, value: z.top}, {time: lastTime, value: z.top}], color: 'rgba(8, 153, 129, 0.9)', lineWidth: 2, lineStyle: 0, showLabel: true, title: `${calcPct(z.top, z.bottom)}% +OB` });
        lines.push({ data:[{time: z.time, value: z.bottom}, {time: lastTime, value: z.bottom}], color: 'rgba(8, 153, 129, 0.9)', lineWidth: 2, lineStyle: 0, showLabel: false });
    });
    
    displayBearOB.forEach(z => {
        lines.push({ data:[{time: z.time, value: z.top}, {time: lastTime, value: z.top}], color: 'rgba(242, 54, 69, 0.9)', lineWidth: 2, lineStyle: 0, showLabel: true, title: `${calcPct(z.top, z.bottom)}% -OB` });
        lines.push({ data:[{time: z.time, value: z.bottom}, {time: lastTime, value: z.bottom}], color: 'rgba(242, 54, 69, 0.9)', lineWidth: 2, lineStyle: 0, showLabel: false });
    });

    const displaySwings = swings.slice(-6);
    displaySwings.forEach(s => {
        markers.push({
            time: s.time,
            position: s.type === 'high' ? 'aboveBar' : 'belowBar',
            color: '#EBCB8B',
            shape: 'circle',
            text: s.type === 'high' ? 'SH' : 'SL',
            size: 0.1
        });
    });

    // CRITICAL: Lightweight Charts crashes if markers aren't perfectly sorted by time
    markers.sort((a, b) => a.time - b.time);

    return { markers, coloredCandles, lines };
};
