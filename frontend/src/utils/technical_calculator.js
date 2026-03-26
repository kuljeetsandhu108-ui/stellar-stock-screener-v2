export const calculateTechnicalSignal = (techs, mas, currentPrice) => {
    let buy = 0, sell = 0, neutral = 0;
    const items =[];
    
    const addSignal = (name, value, signal) => {
        if (signal === 'BUY') buy++;
        else if (signal === 'SELL') sell++;
        else neutral++;
        items.push({ name, value, signal });
    };

    if (techs) {
        const { rsi, macd, macdsignal, adx, stochasticsk, williamsr } = techs;
        
        let sRsi = 'NEUTRAL';
        if (rsi !== null && rsi !== undefined) {
            if (rsi < 30) sRsi = 'BUY'; else if (rsi > 70) sRsi = 'SELL';
        }
        addSignal('RSI (14)', rsi, sRsi);
        
        let sStoch = 'NEUTRAL';
        if (stochasticsk !== null && stochasticsk !== undefined) {
            if (stochasticsk < 20) sStoch = 'BUY'; else if (stochasticsk > 80) sStoch = 'SELL';
        }
        addSignal('Stoch (14,3)', stochasticsk, sStoch);
        
        let sMacd = 'NEUTRAL';
        if (macd !== null && macdsignal !== null && macd !== undefined) {
            sMacd = macd > macdsignal ? 'BUY' : 'SELL';
        }
        addSignal('MACD (12,26)', macd, sMacd);
        
        let sAdx = 'NEUTRAL';
        if (adx !== null && adx !== undefined) {
            if (adx > 25) {
                sAdx = (mas && currentPrice > mas['50']) ? 'BUY' : 'SELL';
            }
        }
        addSignal('ADX (14)', adx, sAdx);
        
        let sWill = 'NEUTRAL';
        if (williamsr !== null && williamsr !== undefined) {
            if (williamsr < -80) sWill = 'BUY'; else if (williamsr > -20) sWill = 'SELL';
        }
        addSignal('Williams %R', williamsr, sWill);
    } else {
        addSignal('RSI (14)', null, 'NEUTRAL');
        addSignal('Stoch (14,3)', null, 'NEUTRAL');
        addSignal('MACD (12,26)', null, 'NEUTRAL');
        addSignal('ADX (14)', null, 'NEUTRAL');
        addSignal('Williams %R', null, 'NEUTRAL');
    }

    if (mas && currentPrice) {
        const checkMa = (val) => (val !== null && val !== undefined) ? (currentPrice > val ? 'BUY' : 'SELL') : 'NEUTRAL';
        addSignal('SMA 10', mas['10'], checkMa(mas['10']));
        addSignal('SMA 20', mas['20'], checkMa(mas['20']));
        addSignal('SMA 50', mas['50'], checkMa(mas['50']));
        addSignal('SMA 200', mas['200'], checkMa(mas['200']));
    } else {
        addSignal('SMA 10', null, 'NEUTRAL');
        addSignal('SMA 20', null, 'NEUTRAL');
        addSignal('SMA 50', null, 'NEUTRAL');
        addSignal('SMA 200', null, 'NEUTRAL');
    }

    const total = buy + sell + neutral;
    const sentiment = total > 0 ? (buy / total) * 100 : 50;
    
    let verdict = "NEUTRAL";
    let color = "#EDBB5A";
    if (buy > sell && buy >= neutral) { verdict = "BUY"; color = "#3FB950"; }
    if (buy > sell * 2) { verdict = "STRONG BUY"; color = "#3FB950"; }
    if (sell > buy && sell >= neutral) { verdict = "SELL"; color = "#F85149"; }
    if (sell > buy * 2) { verdict = "STRONG SELL"; color = "#F85149"; }

    return { buy, sell, neutral, items, sentiment, verdict, color };
};
