import React, { useEffect, useRef, useState, useCallback } from 'react';
import { 
  createChart, 
  ColorType, 
  CrosshairMode, 
  CandlestickSeries, 
  HistogramSeries,
  LineSeries
} from 'lightweight-charts';
import styled from 'styled-components';
import axios from 'axios';
import { RSI, MACD, StochasticRSI, SMA, EMA } from 'technicalindicators';
import { FaLayerGroup, FaTimes, FaPlus } from 'react-icons/fa';

// --- STYLED COMPONENTS ---

const ChartWrapper = styled.div`
  position: relative;
  width: 100%;
  height: 600px;
  background-color: #0D1117;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
  display: flex;
  flex-direction: column;
`;

const Toolbar = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background-color: #161B22;
  border-bottom: 1px solid var(--color-border);
  flex-wrap: wrap;
  gap: 10px;
`;

const LeftGroup = styled.div`
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
`;

const RangeButton = styled.button`
  background: ${({ active }) => active ? 'var(--color-primary)' : 'transparent'};
  color: ${({ active }) => active ? '#fff' : 'var(--color-text-secondary)'};
  border: 1px solid ${({ active }) => active ? 'var(--color-primary)' : 'transparent'};
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: ${({ active }) => active ? 'var(--color-primary)' : 'rgba(255,255,255,0.05)'};
    color: #fff;
  }
`;

const IndicatorButton = styled.button`
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--color-border);
  color: var(--color-text-primary);
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
  position: relative;

  &:hover {
    background: rgba(255,255,255,0.1);
  }
`;

const Dropdown = styled.div`
  position: absolute;
  top: 40px;
  left: 0;
  background: #1C2128;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 10px;
  z-index: 50;
  box-shadow: 0 4px 20px rgba(0,0,0,0.5);
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 220px;
`;

const InputGroup = styled.div`
  display: flex;
  gap: 5px;
  align-items: center;
`;

const StyledInput = styled.input`
  background: #0D1117;
  border: 1px solid var(--color-border);
  color: white;
  padding: 4px;
  border-radius: 4px;
  width: 60px;
  font-size: 0.8rem;
`;

const AddButton = styled.button`
  background: var(--color-success);
  border: none;
  color: white;
  padding: 6px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  margin-top: 5px;
  font-size: 0.8rem;
  
  &:hover { opacity: 0.9; }
`;

const ActiveIndicatorsList = styled.div`
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 4px 0;
  align-items: center;
  &::-webkit-scrollbar { display: none; }
`;

const IndicatorTag = styled.div`
  background: rgba(56, 139, 253, 0.15);
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
`;

const CloseIcon = styled(FaTimes)`
  cursor: pointer;
  &:hover { color: #fff; }
`;

const ChartContainer = styled.div`
  flex-grow: 1;
  width: 100%;
`;

const StatusText = styled.span`
  font-size: 0.75rem;
  color: ${({ isLive }) => isLive ? '#3FB950' : 'var(--color-text-secondary)'};
  margin-left: auto;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
`;

const PulseDot = styled.div`
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #3FB950;
  box-shadow: 0 0 5px #3FB950;
  animation: pulse 2s infinite;
  
  @keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.4; }
    100% { opacity: 1; }
  }
`;

// --- ENHANCED SMC ENGINE ---
const calculateSMC = (data) => {
    const markers = [];
    const coloredCandles = []; 
    const priceLines = []; 

    if (!data || data.length < 5) return { markers, coloredCandles, priceLines };

    for (let i = 2; i < data.length - 1; i++) {
        const curr = data[i];     
        const prev = data[i-1];   
        const prev2 = data[i-2];  

        // --- 1. FAIR VALUE GAPS (FVG) ---
        // We removed the strict threshold so ALL gaps show up.
        
        // Bullish Gap
        if (curr.low > prev2.high) {
            coloredCandles.push({ 
                time: prev.time, 
                color: '#FBBF24', // Yellow
                wickColor: '#FBBF24', 
                borderColor: '#FBBF24' 
            });
            // Draw Demand Zone (limit to recent)
            if (i > data.length - 80) {
                 priceLines.push({ price: prev2.high, color: '#FBBF24', title: 'DEMAND GAP' });
            }
        }

        // Bearish Gap
        if (curr.high < prev2.low) {
            coloredCandles.push({ 
                time: prev.time, 
                color: '#D500F9', // Purple
                wickColor: '#D500F9', 
                borderColor: '#D500F9' 
            });
            // Draw Supply Zone
            if (i > data.length - 80) {
                priceLines.push({ price: prev2.low, color: '#D500F9', title: 'SUPPLY GAP' });
            }
        }

        // --- 2. ORDER BLOCKS (Independent Price Action Logic) ---
        
        // Bullish OB: Red candle followed by Green that closes above Red's Open (Engulfing)
        const isRedPrev = prev.close < prev.open;
        const isGreenCurr = curr.close > curr.open;
        const engulfsBull = curr.close > prev.open; // Simple engulfing definition

        if (isRedPrev && isGreenCurr && engulfsBull) {
            markers.push({ 
                time: prev.time, // Mark the Order Block candle
                position: 'belowBar', 
                color: '#00E676', // Bright Green
                shape: 'arrowUp', 
                text: 'OB',
                size: 1
            });
        }
        
        // Bearish OB: Green candle followed by Red that closes below Green's Open
        const isGreenPrev = prev.close > prev.open;
        const isRedCurr = curr.close < curr.open;
        const engulfsBear = curr.close < prev.open;

        if (isGreenPrev && isRedCurr && engulfsBear) {
            markers.push({ 
                time: prev.time, 
                position: 'aboveBar', 
                color: '#FF1744', // Bright Red
                shape: 'arrowDown', 
                text: 'OB',
                size: 1
            });
        }
    }
    
    // Sort markers by time
    markers.sort((a, b) => a.time - b.time);
    
    // Deduplicate markers (keep only one per candle to avoid clutter)
    const uniqueMarkers = [];
    const seenTimes = new Set();
    for (let m of markers) {
        if (!seenTimes.has(m.time)) {
            uniqueMarkers.push(m);
            seenTimes.add(m.time);
        }
    }

    return { markers: uniqueMarkers, coloredCandles, priceLines };
};

// --- MAIN COMPONENT ---

const CustomChart = ({ symbol }) => {
  const chartContainerRef = useRef();
  
  const chartRef = useRef(null);
  const candleSeriesRef = useRef(null);
  const volumeSeriesRef = useRef(null);
  const priceLinesRef = useRef([]); 
  
  const [timeframe, setTimeframe] = useState('1D'); 
  const [chartData, setChartData] = useState([]);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeIndicators, setActiveIndicators] = useState([]);
  const [isLive, setIsLive] = useState(false);
  
  const [selectedInd, setSelectedInd] = useState('SMC');
  const [param1, setParam1] = useState(20);
  const [param2, setParam2] = useState(26);
  const [param3, setParam3] = useState(9);

  // --- 1. INITIALIZATION ---
  useEffect(() => {
    if (!chartContainerRef.current) return;
    chartContainerRef.current.innerHTML = '';

    const chart = createChart(chartContainerRef.current, {
      layout: { background: { type: ColorType.Solid, color: '#0D1117' }, textColor: '#8B949E' },
      grid: { vertLines: { color: '#21262D' }, horzLines: { color: '#21262D' } },
      width: chartContainerRef.current.clientWidth,
      height: chartContainerRef.current.clientHeight,
      crosshair: { mode: CrosshairMode.Normal },
      timeScale: { borderColor: '#30363D', timeVisible: true },
      rightPriceScale: { borderColor: '#30363D' },
    });

    const candleSeries = chart.addSeries(CandlestickSeries, {
      upColor: '#3FB950', downColor: '#F85149',
      borderVisible: false, wickUpColor: '#3FB950', wickDownColor: '#F85149',
    });

    const volumeSeries = chart.addSeries(HistogramSeries, {
      color: '#26a69a', priceFormat: { type: 'volume' }, priceScaleId: '',
    });
    volumeSeries.priceScale().applyOptions({ scaleMargins: { top: 0.85, bottom: 0 } });

    chartRef.current = chart;
    candleSeriesRef.current = candleSeries;
    volumeSeriesRef.current = volumeSeries;

    const resizeObserver = new ResizeObserver(entries => {
        if (!chartRef.current) return;
        const newRect = entries[0].contentRect;
        if (newRect.width > 0 && newRect.height > 0) {
            chartRef.current.applyOptions({ width: newRect.width, height: newRect.height });
            chartRef.current.timeScale().fitContent(); 
        }
    });
    resizeObserver.observe(chartContainerRef.current);

    return () => {
      resizeObserver.disconnect();
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
      }
    };
  }, []);

  // --- 2. DATA FETCHING ---
  const fetchData = useCallback(async () => {
    if (!symbol) return;
    try {
      const response = await axios.get(`/api/stocks/${symbol}/chart?range=${timeframe}`);
      const data = response.data;

      if (chartRef.current && candleSeriesRef.current && data.length > 0) {
        setChartData(data);
        setIsLive(true);
      }
    } catch (err) {
      console.error("Chart Error:", err);
      setIsLive(false);
    }
  }, [symbol, timeframe]);

  // --- 3. APPLY INDICATORS ---
  useEffect(() => {
    if (!chartRef.current || !candleSeriesRef.current || chartData.length === 0) return;

    const isSMC = activeIndicators.some(i => i.type === 'SMC');

    if (isSMC) {
        const { markers, coloredCandles, priceLines } = calculateSMC(chartData);

        // 1. Apply Colors (FVG)
        const coloredData = chartData.map(d => {
            const override = coloredCandles.find(c => c.time === d.time);
            return override ? { ...d, ...override } : d;
        });
        candleSeriesRef.current.setData(coloredData);

        // 2. Apply Markers (OB)
        if (candleSeriesRef.current.setMarkers) {
             candleSeriesRef.current.setMarkers(markers);
        }

        // 3. Apply Lines
        // Clear old lines
        priceLinesRef.current.forEach(line => {
             if(chartRef.current && candleSeriesRef.current) {
                 try { candleSeriesRef.current.removePriceLine(line); } catch(e){}
             }
        });
        priceLinesRef.current = [];

        // Draw new lines (Limit last 5 for performance)
        const recentLines = priceLines.slice(-5);
        recentLines.forEach(lineData => {
            if (candleSeriesRef.current.createPriceLine) {
                const lineObj = candleSeriesRef.current.createPriceLine({
                    price: lineData.price,
                    color: lineData.color,
                    lineWidth: 2,
                    lineStyle: 0, 
                    axisLabelVisible: true,
                    title: lineData.title,
                });
                priceLinesRef.current.push(lineObj);
            }
        });

    } else {
        // Normal Mode
        candleSeriesRef.current.setData(chartData);
        if (candleSeriesRef.current.setMarkers) {
            candleSeriesRef.current.setMarkers([]);
        }
        // Clear SMC lines
        priceLinesRef.current.forEach(line => {
             if(chartRef.current && candleSeriesRef.current) {
                 try { candleSeriesRef.current.removePriceLine(line); } catch(e){}
             }
        });
        priceLinesRef.current = [];
    }

    // Update Volume
    if (volumeSeriesRef.current) {
        const volData = chartData.map(d => ({
          time: d.time, value: d.volume,
          color: d.close >= d.open ? 'rgba(63, 185, 80, 0.4)' : 'rgba(248, 81, 73, 0.4)'
        }));
        volumeSeriesRef.current.setData(volData);
    }

  }, [chartData, activeIndicators]);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, [fetchData]);

  // --- 4. HANDLERS ---
  const addIndicator = () => {
    if (!chartData.length || !chartRef.current) return;
    const closePrices = chartData.map(d => d.close);
    const id = Date.now();
    let newSeries = [];
    let paneId = `pane_${id}`;

    try {
      if (selectedInd === 'SMC') { 
          // Logic handled in useEffect
      }
      else if (selectedInd === 'SMA') {
        const period = parseInt(param1);
        const res = SMA.calculate({ period, values: closePrices });
        const lineData = [];
        for (let i = 0; i < res.length; i++) {
            const dIndex = chartData.length - 1 - i; const rIndex = res.length - 1 - i;
            if (dIndex >= 0) lineData.unshift({ time: chartData[dIndex].time, value: res[rIndex] });
        }
        const series = chartRef.current.addSeries(LineSeries, { color: '#FF9800', lineWidth: 2, title: `SMA ${period}` });
        series.setData(lineData);
        newSeries.push(series);
      }
      else if (selectedInd === 'EMA') {
        const period = parseInt(param1);
        const res = EMA.calculate({ period, values: closePrices });
        const lineData = [];
        for (let i = 0; i < res.length; i++) {
            const dIndex = chartData.length - 1 - i; const rIndex = res.length - 1 - i;
            if (dIndex >= 0) lineData.unshift({ time: chartData[dIndex].time, value: res[rIndex] });
        }
        const series = chartRef.current.addSeries(LineSeries, { color: '#2962FF', lineWidth: 2, title: `EMA ${period}` });
        series.setData(lineData);
        newSeries.push(series);
      }
      else if (selectedInd === 'RSI') {
        const res = RSI.calculate({ values: closePrices, period: parseInt(param1) });
        const lineData = [];
        for (let i = 0; i < res.length; i++) {
            const dIndex = chartData.length - 1 - i; const rIndex = res.length - 1 - i;
            if (dIndex >= 0) lineData.unshift({ time: chartData[dIndex].time, value: res[rIndex] });
        }
        const series = chartRef.current.addSeries(LineSeries, { color: '#A855F7', lineWidth: 2, priceScaleId: paneId, title: `RSI (${param1})` });
        series.setData(lineData);
        newSeries.push(series);
        chartRef.current.priceScale(paneId).applyOptions({ scaleMargins: { top: 0.8, bottom: 0 } });
      }
      else if (selectedInd === 'MACD') {
        const macdInput = { values: closePrices, fastPeriod: parseInt(param1), slowPeriod: parseInt(param2), signalPeriod: parseInt(param3), SimpleMAOscillator: false, SimpleMASignal: false };
        const res = MACD.calculate(macdInput);
        const mLine = []; const sLine = []; const hLine = [];
        for(let i=0; i<res.length; i++){
            const dIndex = chartData.length - 1 - i; const rIndex = res.length - 1 - i;
            if (dIndex >= 0){
                const t = chartData[dIndex].time; const m = res[rIndex];
                mLine.unshift({ time: t, value: m.MACD });
                sLine.unshift({ time: t, value: m.signal });
                hLine.unshift({ time: t, value: m.histogram, color: m.histogram >= 0 ? '#26a69a' : '#ef5350' });
            }
        }
        const hSeries = chartRef.current.addSeries(HistogramSeries, { priceScaleId: paneId });
        const mSeries = chartRef.current.addSeries(LineSeries, { color: '#2962FF', lineWidth: 2, priceScaleId: paneId });
        const sSeries = chartRef.current.addSeries(LineSeries, { color: '#FF6D00', lineWidth: 2, priceScaleId: paneId });
        hSeries.setData(hLine); mSeries.setData(mLine); sSeries.setData(sLine);
        newSeries = [hSeries, mSeries, sSeries];
        chartRef.current.priceScale(paneId).applyOptions({ scaleMargins: { top: 0.8, bottom: 0 } });
      }

      setActiveIndicators([...activeIndicators, { id, type: selectedInd, series: newSeries, params: `${param1}${selectedInd === 'SMA' || selectedInd === 'EMA' ? '' : ','+param2+','+param3}` }]);
      setIsMenuOpen(false);
    } catch (e) { console.error("Indicator Calc Error", e); }
  };

  const removeIndicator = (id) => {
      const indToRemove = activeIndicators.find(i => i.id === id);
      if (!indToRemove) return;

      if (indToRemove.type !== 'SMC') {
          if (chartRef.current) {
              indToRemove.series.forEach(s => chartRef.current.removeSeries(s));
          }
      }
      setActiveIndicators(activeIndicators.filter(i => i.id !== id));
  };

  const timeframesList = ['5M', '15M', '1H', '4H', '1D'];

  return (
    <ChartWrapper>
      <Toolbar>
        <LeftGroup>
            <div style={{display:'flex', gap:'4px'}}>
            {timeframesList.map((tf) => (
                <RangeButton key={tf} active={timeframe === tf} onClick={() => setTimeframe(tf)}>{tf}</RangeButton>
            ))}
            </div>
            <div style={{position: 'relative'}}>
                <IndicatorButton onClick={() => setIsMenuOpen(!isMenuOpen)}><FaLayerGroup /> Indicators <FaPlus size={10}/></IndicatorButton>
                {isMenuOpen && (
                    <Dropdown>
                        <select style={{background: '#0D1117', color:'white', padding:'5px', borderRadius:'4px', width:'100%'}} value={selectedInd} onChange={(e) => setSelectedInd(e.target.value)}>
                            <option value="SMC">⚡ SMC (Smart Money)</option>
                            <option value="SMA">SMA</option><option value="EMA">EMA</option><option value="RSI">RSI</option><option value="MACD">MACD</option>
                        </select>
                        {selectedInd !== 'SMC' && (
                            <>
                            <div style={{fontSize:'0.8rem', color:'#8b949e'}}>Settings:</div>
                            <InputGroup>
                                <StyledInput type="number" value={param1} onChange={e=>setParam1(e.target.value)} title="Period/Fast" />
                                {['MACD'].includes(selectedInd) && (
                                    <><StyledInput type="number" value={param2} onChange={e=>setParam2(e.target.value)} title="Slow" /><StyledInput type="number" value={param3} onChange={e=>setParam3(e.target.value)} title="Signal" /></>
                                )}
                            </InputGroup>
                            </>
                        )}
                        <AddButton onClick={addIndicator}>Add {selectedInd}</AddButton>
                    </Dropdown>
                )}
            </div>
        </LeftGroup>
        <div style={{display:'flex', gap:'5px', overflowX:'auto'}}>
            {activeIndicators.map(ind => (
                <IndicatorTag key={ind.id}>{ind.type}<CloseIcon onClick={() => removeIndicator(ind.id)} /></IndicatorTag>
            ))}
        </div>
        <StatusText isLive={isLive}>{isLive && <PulseDot />}{isLive ? 'LIVE' : 'CONNECTING...'}</StatusText>
      </Toolbar>
      <ChartContainer ref={chartContainerRef} />
    </ChartWrapper>
  );
};

export default CustomChart;