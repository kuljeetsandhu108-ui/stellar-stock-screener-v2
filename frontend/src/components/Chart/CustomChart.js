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
import { RSI, MACD, StochasticRSI, SMA, EMA, ADX, ATR, VWAP } from 'technicalindicators';
import { 
  FaLayerGroup, FaTimes, FaPlus, FaMousePointer, 
  FaMinus, FaSlash, FaVectorSquare, FaListOl, FaBalanceScale, FaEraser, FaUndo, FaPencilAlt, FaTrash, FaSpinner, FaExclamationTriangle, FaPlug, FaWifi
} from 'react-icons/fa';
import { FyersClientEngine } from '../../utils/FyersClientEngine';

// ==========================================
// 1. HIGH-END STYLED COMPONENTS
// ==========================================

const ChartWrapper = styled.div`
  position: relative;
  width: 100%;
  height: 650px;
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
  z-index: 20;
`;

const DrawingSidebar = styled.div`
  position: absolute;
  top: 60px;
  left: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: rgba(22, 27, 34, 0.95);
  backdrop-filter: blur(10px);
  padding: 8px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  z-index: 30;
  box-shadow: 4px 0 20px rgba(0,0,0,0.4);
`;

const ToolBtn = styled.button`
  width: 36px;
  height: 36px;
  border-radius: 6px;
  border: 1px solid ${({ active }) => active ? 'var(--color-primary)' : 'transparent'};
  background: ${({ active }) => active ? 'rgba(88, 166, 255, 0.2)' : 'transparent'};
  color: ${({ active }) => active ? 'var(--color-primary)' : 'var(--color-text-secondary)'};
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1rem;
  position: relative;

  &:hover {
    background: rgba(255,255,255,0.1);
    color: #fff;
  }
`;

const LayersPanel = styled.div`
  position: absolute;
  top: 60px;
  right: 10px;
  width: 260px;
  background: rgba(22, 27, 34, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 10px;
  z-index: 30;
  box-shadow: -4px 0 20px rgba(0,0,0,0.4);
  max-height: 400px;
  overflow-y: auto;
  
  &::-webkit-scrollbar { width: 4px; }
  &::-webkit-scrollbar-thumb { background: #30363D; border-radius: 2px; }
`;

const LayerHeader = styled.div`
  color: #8b949e;
  font-size: 0.75rem;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const LayerItem = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255,255,255,0.03);
  padding: 8px 10px;
  border-radius: 6px;
  margin-bottom: 6px;
  font-size: 0.85rem;
  border: 1px solid transparent;
  transition: all 0.2s;
  
  &:hover {
    border-color: var(--color-primary);
    background: rgba(255,255,255,0.05);
  }
`;

const LayerActions = styled.div`
  display: flex;
  gap: 8px;
`;

const IconButton = styled.button`
  background: transparent;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 2px;
  display: flex;
  &:hover { color: #fff; }
  &.delete:hover { color: #F85149; }
`;

const EditModal = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #1C2128;
  border: 1px solid var(--color-primary);
  padding: 20px;
  border-radius: 12px;
  z-index: 100;
  box-shadow: 0 20px 50px rgba(0,0,0,0.9);
  width: 320px;
`;

const ModalTitle = styled.h4`margin: 0 0 15px 0; color: #fff; font-size: 1.1rem;`;
const ModalInput = styled.div`
  margin-bottom: 12px;
  label { display: block; font-size: 0.75rem; color: #8b949e; margin-bottom: 4px; text-transform: uppercase; }
  input { width: 100%; background: #0D1117; border: 1px solid #30363D; color: #fff; padding: 8px; border-radius: 6px; font-family: 'Roboto Mono', monospace; }
  input:focus { border-color: var(--color-primary); outline: none; }
`;
const ModalActions = styled.div`display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px;`;

const LeftGroup = styled.div`display: flex; gap: 10px; align-items: center; flex-wrap: wrap;`;
const RangeButton = styled.button`background: ${({ active }) => active ? 'var(--color-primary)' : 'transparent'}; color: ${({ active }) => active ? '#fff' : 'var(--color-text-secondary)'}; border: 1px solid ${({ active }) => active ? 'var(--color-primary)' : 'transparent'}; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: all 0.2s; &:hover { background: ${({ active }) => active ? 'var(--color-primary)' : 'rgba(255,255,255,0.05)'}; color: #fff; }`;
const IndicatorButton = styled.button`display: flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.05); border: 1px solid var(--color-border); color: var(--color-text-primary); padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; cursor: pointer; position: relative; &:hover { background: rgba(255,255,255,0.1); }`;
const Dropdown = styled.div`position: absolute; top: 40px; left: 0; background: #1C2128; border: 1px solid var(--color-border); border-radius: 8px; padding: 10px; z-index: 50; box-shadow: 0 4px 20px rgba(0,0,0,0.5); display: flex; flex-direction: column; gap: 8px; width: 220px;`;
const InputGroup = styled.div`display: flex; gap: 5px; align-items: center;`;
const StyledInput = styled.input`background: #0D1117; border: 1px solid var(--color-border); color: white; padding: 4px; border-radius: 4px; width: 60px; font-size: 0.8rem;`;
const AddButton = styled.button`background: var(--color-success); border: none; color: white; padding: 6px; border-radius: 4px; cursor: pointer; font-weight: 600; margin-top: 5px; font-size: 0.8rem; &:hover { opacity: 0.9; }`;
const ActiveIndicatorsList = styled.div`display: flex; gap: 8px; overflow-x: auto; padding: 4px 0; align-items: center; &::-webkit-scrollbar { display: none; }`;
const IndicatorTag = styled.div`background: rgba(56, 139, 253, 0.15); border: 1px solid var(--color-primary); color: var(--color-primary); padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; display: flex; align-items: center; gap: 6px; white-space: nowrap;`;
const CloseIcon = styled(FaTimes)`cursor: pointer; &:hover { color: #fff; }`;
const ChartContainer = styled.div`flex-grow: 1; width: 100%; cursor: ${({ crosshair }) => crosshair ? 'crosshair' : 'default'};`;
const StatusText = styled.span`font-size: 0.75rem; color: ${({ isLive }) => isLive ? '#3FB950' : 'var(--color-text-secondary)'}; margin-left: auto; font-weight: 600; display: flex; align-items: center; gap: 6px;`;
const PulseDot = styled.div`width: 6px; height: 6px; border-radius: 50%; background-color: #3FB950; box-shadow: 0 0 5px #3FB950; animation: pulse 2s infinite; @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }`;
const HelperText = styled.div`position: absolute; top: 60px; left: 60px; background: rgba(0,0,0,0.7); color: #fff; padding: 5px 10px; border-radius: 4px; font-size: 0.8rem; pointer-events: none; z-index: 25;`;
const LoadingOverlay = styled.div`position: absolute; top: 50px; left: 0; right: 0; bottom: 0; background: rgba(13, 17, 23, 0.4); backdrop-filter: blur(2px); z-index: 15; display: flex; align-items: center; justify-content: center; color: var(--color-primary); font-size: 2rem;`;
const Spinner = styled(FaSpinner)`animation: spin 1s linear infinite; @keyframes spin { 100% { transform: rotate(360deg); } }`;
const NoDataOverlay = styled.div`position: absolute; top: 50px; left: 0; right: 0; bottom: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; color: var(--color-text-secondary); z-index: 10; font-size: 1.2rem; gap: 10px;`;

// ==========================================
// 2. MATH ALGORITHMS (Client-Side)
// ==========================================

const calculateSuperTrend = (data, period = 10, multiplier = 3) => {
    if (!data || data.length < period) return [];
    const atr = ATR.calculate({ period, high: data.map(d=>d.high), low: data.map(d=>d.low), close: data.map(d=>d.close) });
    const st = [];
    let prevFinalUpper = 0; let prevFinalLower = 0; let prevTrend = 1;
    for (let i = 0; i < data.length; i++) {
        const atrIndex = i - (period - 1);
        if (atrIndex < 0) continue;
        const curr = data[i]; const prev = data[i-1]; const currAtr = atr[atrIndex];
        const basicUpper = (curr.high + curr.low) / 2 + multiplier * currAtr;
        const basicLower = (curr.high + curr.low) / 2 - multiplier * currAtr;
        let finalUpper = basicUpper;
        if (prev && prevFinalUpper) { if (basicUpper < prevFinalUpper || prev.close > prevFinalUpper) finalUpper = basicUpper; else finalUpper = prevFinalUpper; }
        let finalLower = basicLower;
        if (prev && prevFinalLower) { if (basicLower > prevFinalLower || prev.close < prevFinalLower) finalLower = basicLower; else finalLower = prevFinalLower; }
        let trend = prevTrend;
        if (prevTrend === 1 && curr.close < finalLower) trend = -1; else if (prevTrend === -1 && curr.close > finalUpper) trend = 1;
        st.push({ time: curr.time, value: trend === 1 ? finalLower : finalUpper, color: trend === 1 ? '#00E676' : '#FF1744' });
        prevFinalUpper = finalUpper; prevFinalLower = finalLower; prevTrend = trend;
    }
    return st;
};

const calculateSMC = (data) => {
    const markers = []; const coloredCandles = []; const priceLines = []; 
    if (!data || data.length < 5) return { markers, coloredCandles, priceLines };
    for (let i = 2; i < data.length - 1; i++) {
        const curr = data[i]; const prev = data[i-1]; const prev2 = data[i-2];
        if (curr.low > prev2.high) {
            coloredCandles.push({ time: prev.time, color: '#FBBF24', wickColor: '#FBBF24', borderColor: '#FBBF24' });
            if (i > data.length - 80) priceLines.push({ price: prev2.high, color: '#FBBF24', title: 'DEMAND GAP' });
        }
        if (curr.high < prev2.low) {
            coloredCandles.push({ time: prev.time, color: '#D500F9', wickColor: '#D500F9', borderColor: '#D500F9' });
            if (i > data.length - 80) priceLines.push({ price: prev2.low, color: '#D500F9', title: 'SUPPLY GAP' });
        }
        const isRedPrev = prev.close < prev.open; const isGreenCurr = curr.close > curr.open; const engulfsBull = curr.close > prev.open; 
        if (isRedPrev && isGreenCurr && engulfsBull) markers.push({ time: prev.time, position: 'belowBar', color: '#3FB950', shape: 'arrowUp', text: 'OB', size: 1 });
        const isGreenPrev = prev.close > prev.open; const isRedCurr = curr.close < curr.open; const engulfsBear = curr.close < prev.open;
        if (isGreenPrev && isRedCurr && engulfsBear) markers.push({ time: prev.time, position: 'aboveBar', color: '#F85149', shape: 'arrowDown', text: 'OB', size: 1 });
    }
    return { markers, coloredCandles, priceLines };
};

// ==========================================
// 3. MAIN COMPONENT
// ==========================================

const CustomChart = ({ symbol }) => {
  const chartContainerRef = useRef();
  
  // Instance Refs
  const chartRef = useRef(null);
  const candleSeriesRef = useRef(null);
  const volumeSeriesRef = useRef(null);
  const abortControllerRef = useRef(null);
  const fyersEngineRef = useRef(null);

  // Drawing & State Refs
  const priceLinesRef = useRef([]); 
  const drawingLinesRef = useRef([]); 
  const drawingSeriesRef = useRef([]); 
  const previewObjectsRef = useRef([]); 
  const lastCandleRef = useRef(null); 
  const isMounted = useRef(true);

  // State
  const [timeframe, setTimeframe] = useState('1D'); 
  const [chartData, setChartData] = useState([]);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeIndicators, setActiveIndicators] = useState([]);
  const [isLive, setIsLive] = useState(false);
  const [connectionType, setConnectionType] = useState("Server");
  const [isChartLoading, setIsChartLoading] = useState(false);
  const [hasError, setHasError] = useState(false);
  
  const [drawMode, setDrawMode] = useState('cursor'); 
  const [tempPoints, setTempPoints] = useState([]);
  const [userDrawings, setUserDrawings] = useState([]); 
  const [editingDrawing, setEditingDrawing] = useState(null);
  const [editValues, setEditValues] = useState({});
  const drawModeRef = useRef(drawMode); 
  const tempPointsRef = useRef(tempPoints);

  const [selectedInd, setSelectedInd] = useState('SMC');
  const [param1, setParam1] = useState(20);
  const [param2, setParam2] = useState(26);
  const [param3, setParam3] = useState(9);

  // Constants
  const isIndian = symbol?.includes('.NS') || symbol?.includes('.BO') || symbol?.includes('NIFTY') || symbol?.includes('SENSEX') || symbol?.includes('BANK');

  const istFormatter = (timestamp) => {
      const date = new Date(timestamp * 1000);
      if (isIndian) {
          if (!['1D', '1W', '1M'].includes(timeframe)) {
              return new Intl.DateTimeFormat('en-IN', { timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit', hour12: false }).format(date);
          }
          return new Intl.DateTimeFormat('en-IN', { timeZone: 'Asia/Kolkata', day: '2-digit', month: 'short', year: '2-digit' }).format(date);
      }
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  useEffect(() => { 
      drawModeRef.current = drawMode; 
      if(drawMode === 'cursor') { setTempPoints([]); clearPreview(); }
  }, [drawMode]);
  
  useEffect(() => { tempPointsRef.current = tempPoints; }, [tempPoints]);
  useEffect(() => { userDrawingsRef.current = userDrawings; }, [userDrawings]);

  const mapData = (values, chartData) => {
    const output = [];
    for (let i = 0; i < values.length; i++) {
        const dIndex = chartData.length - 1 - i; const vIndex = values.length - 1 - i;
        if (dIndex >= 0) output.unshift({ time: chartData[dIndex].time, value: values[vIndex] });
    }
    return output;
  };

  // --- INITIALIZE CHART ---
  useEffect(() => {
    isMounted.current = true;
    if (!chartContainerRef.current) return;
    chartContainerRef.current.innerHTML = '';
    
    // Clear refs
    priceLinesRef.current = []; drawingLinesRef.current = []; drawingSeriesRef.current = []; previewObjectsRef.current = [];

    const chart = createChart(chartContainerRef.current, {
      layout: { background: { type: ColorType.Solid, color: '#0D1117' }, textColor: '#8B949E' },
      grid: { vertLines: { color: '#21262D' }, horzLines: { color: '#21262D' } },
      width: chartContainerRef.current.clientWidth,
      height: chartContainerRef.current.clientHeight,
      crosshair: { mode: CrosshairMode.Normal },
      timeScale: { borderColor: '#30363D', timeVisible: true, secondsVisible: false, tickMarkFormatter: (time) => istFormatter(time) },
      localization: { timeFormatter: (time) => istFormatter(time) },
      rightPriceScale: { borderColor: '#30363D' },
    });

    const candleSeries = chart.addSeries(CandlestickSeries, {
      upColor: '#3FB950', downColor: '#F85149', borderVisible: false, wickUpColor: '#3FB950', wickDownColor: '#F85149',
    });

    const volumeSeries = chart.addSeries(HistogramSeries, {
      color: '#26a69a', priceFormat: { type: 'volume' }, priceScaleId: '',
    });
    volumeSeries.priceScale().applyOptions({ scaleMargins: { top: 0.85, bottom: 0 } });

    // Click Listener
    chart.subscribeClick((param) => {
      // ZOMBIE CHECK
      if (!isMounted.current || !chartRef.current || !candleSeries) return;
      if (!param.point || !param.time) return;
      const price = candleSeries.coordinateToPrice(param.point.y);
      const time = param.time;
      const mode = drawModeRef.current;
      const id = Date.now();
      if (mode === 'cursor') return;
      if (mode === 'horizontal') { setUserDrawings(prev => [...prev, { id, type: 'horizontal', price, title: 'H-Line' }]); setDrawMode('cursor'); return; }
      if (mode === 'rect') { setUserDrawings(prev => [...prev, { id, type: 'rect', price, title: 'Zone' }]); return; }
      if (['fib', 'trend', 'longshort'].includes(mode)) { handleMultiClickTool(price, time, mode === 'longshort' ? 3 : 2, (points) => { setUserDrawings(prev => [...prev, { id, type: mode, points }]); }); }
    });

    // Crosshair Listener
    chart.subscribeCrosshairMove((param) => {
        if (!isMounted.current || !chartRef.current) return;
        const mode = drawModeRef.current;
        const currentPoints = tempPointsRef.current;
        if (mode === 'cursor' || currentPoints.length === 0 || !param.point || !param.time) return;
        const currentPrice = candleSeries.coordinateToPrice(param.point.y);
        const currentTime = param.time;
        const start = currentPoints[0];
        if (currentTime === start.time) return; 
        drawPreviewShape(mode, start, { price: currentPrice, time: currentTime }, chart, candleSeries);
    });

    chartRef.current = chart;
    candleSeriesRef.current = candleSeries;
    volumeSeriesRef.current = volumeSeries;

    const resizeObserver = new ResizeObserver(entries => {
        if (!isMounted.current || !chartRef.current) return;
        const newRect = entries[0].contentRect;
        if (newRect.width > 0 && newRect.height > 0) {
            try { chartRef.current.applyOptions({ width: newRect.width, height: newRect.height }); chartRef.current.timeScale().fitContent(); } catch(e) {}
        }
    });
    resizeObserver.observe(chartContainerRef.current);

    return () => {
      isMounted.current = false;
      resizeObserver.disconnect();
      if (fyersEngineRef.current) fyersEngineRef.current.disconnect();
      if (chartRef.current) { 
          try { chartRef.current.remove(); } catch(e) {} 
          chartRef.current = null; candleSeriesRef.current = null; volumeSeriesRef.current = null; 
      }
    };
  }, [symbol, timeframe]);

  // --- DRAWING HELPERS ---
  const handleMultiClickTool = (price, time, requiredClicks, callback) => { setTempPoints(prev => { const newPoints = [...prev, { price, time }]; if (newPoints.length === requiredClicks) { clearPreview(); callback(newPoints); setDrawMode('cursor'); return []; } return newPoints; }); };
  const clearPreview = () => { previewObjectsRef.current.forEach(obj => { if (obj.type === 'line' && candleSeriesRef.current) try{ candleSeriesRef.current.removePriceLine(obj.ref); } catch(e){} if (obj.type === 'series' && chartRef.current) try{ chartRef.current.removeSeries(obj.ref); } catch(e){} }); previewObjectsRef.current = []; };
  const drawPreviewShape = (type, p1, p2, chart, series) => { clearPreview(); if (type === 'trend') { const sorted = p1.time > p2.time ? [p2, p1] : [p1, p2]; const data = [{ time: sorted[0].time, value: sorted[0].price }, { time: sorted[1].time, value: sorted[1].price }]; const lineSeries = chart.addSeries(LineSeries, { color: '#ffffff', lineWidth: 1, lastValueVisible: false, priceLineVisible: false }); lineSeries.setData(data); previewObjectsRef.current.push({ type: 'series', ref: lineSeries }); } else if (type === 'fib') { const low = Math.min(p1.price, p2.price); const high = Math.max(p1.price, p2.price); const diff = high - low; const levels = [0, 0.5, 1]; levels.forEach(lvl => { const line = series.createPriceLine({ price: low + (diff * lvl), color: '#FFD700', lineWidth: 1, lineStyle: 2, axisLabelVisible: false }); previewObjectsRef.current.push({ type: 'line', ref: line }); }); } else if (type === 'longshort') { const l1 = series.createPriceLine({ price: p1.price, color: '#888', title: 'ENTRY' }); const l2 = series.createPriceLine({ price: p2.price, color: '#3FB950', title: 'TARGET' }); previewObjectsRef.current.push({ type: 'line', ref: l1 }, { type: 'line', ref: l2 }); } };
  const handleEdit = (d) => { setEditingDrawing(d.id); if (d.points) { setEditValues({ p1: d.points[0]?.price, p2: d.points[1]?.price, p3: d.points[2]?.price }); } else { setEditValues({ p1: d.price }); } };
  const saveEdit = () => { setUserDrawings(prev => prev.map(d => { if (d.id !== editingDrawing) return d; if (d.points) { const newPoints = [...d.points]; if (editValues.p1) newPoints[0].price = parseFloat(editValues.p1); if (editValues.p2) newPoints[1].price = parseFloat(editValues.p2); if (editValues.p3 && newPoints[2]) newPoints[2].price = parseFloat(editValues.p3); return { ...d, points: newPoints }; } else { return { ...d, price: parseFloat(editValues.p1) }; } })); setEditingDrawing(null); };
  const deleteDrawing = (id) => setUserDrawings(prev => prev.filter(d => d.id !== id));
  const clearDrawings = () => { setUserDrawings([]); };
  const undoLastDrawing = () => { if (userDrawings.length > 0) setUserDrawings(prev => prev.slice(0, -1)); };

  useEffect(() => { if (!isMounted.current || !candleSeriesRef.current) return; drawingLinesRef.current.forEach(item => { try { candleSeriesRef.current.removePriceLine(item.ref); } catch(e){} }); drawingLinesRef.current = []; drawingSeriesRef.current.forEach(item => { try { chartRef.current.removeSeries(item.ref); } catch(e){} }); drawingSeriesRef.current = []; userDrawings.forEach(d => { if (d.type === 'horizontal') { const line = candleSeriesRef.current.createPriceLine({ price: d.price, color: '#38bdf8', lineWidth: 2, lineStyle: 0, axisLabelVisible: true, title: d.title }); drawingLinesRef.current.push({ type: 'line', ref: line }); } else if (d.type === 'rect') { const line = candleSeriesRef.current.createPriceLine({ price: d.price, color: '#FBBF24', lineWidth: 3, lineStyle: 2, axisLabelVisible: false, title: d.title }); drawingLinesRef.current.push({ type: 'line', ref: line }); } else if (d.type === 'fib') { const p1 = d.points[0]; const p2 = d.points[1]; const low = Math.min(p1.price, p2.price); const high = Math.max(p1.price, p2.price); const diff = high - low; const levels = [{l:0,c:'#fff',w:1},{l:0.382,c:'#FFD700',w:2},{l:0.5,c:'#3FB950',w:2},{l:0.618,c:'#FFD700',w:2},{l:1,c:'#fff',w:1}]; levels.forEach(lvl => { const line = candleSeriesRef.current.createPriceLine({ price: low + (diff * lvl.l), color: lvl.c, lineWidth: lvl.w, lineStyle: 2, axisLabelVisible: true, title: `Fib ${lvl.l}` }); drawingLinesRef.current.push({ type: 'line', ref: line }); }); } else if (d.type === 'trend') { const sorted = d.points[0].time > d.points[1].time ? [d.points[1], d.points[0]] : [d.points[0], d.points[1]]; const data = [{ time: sorted[0].time, value: sorted[0].price }, { time: sorted[1].time, value: sorted[1].price }]; const series = chartRef.current.addSeries(LineSeries, { color: '#ffffff', lineWidth: 2, lastValueVisible: false, priceLineVisible: false }); series.setData(data); drawingSeriesRef.current.push({ type: 'series', ref: series }); } else if (d.type === 'longshort') { const entry = d.points[0].price; const stop = d.points[1].price; const target = d.points[2].price; const rr = Math.abs((target - entry) / (entry - stop)).toFixed(2); const l1 = candleSeriesRef.current.createPriceLine({ price: entry, color: '#888', title: 'ENTRY' }); const l2 = candleSeriesRef.current.createPriceLine({ price: stop, color: '#F85149', title: 'STOP' }); const l3 = candleSeriesRef.current.createPriceLine({ price: target, color: '#3FB950', title: `TARGET R:R ${rr}` }); drawingLinesRef.current.push({ type: 'line', ref: l1 }, { type: 'line', ref: l2 }, { type: 'line', ref: l3 }); } }); }, [userDrawings]);

  const updateLayout = () => { if (!isMounted.current || !chartRef.current || !volumeSeriesRef.current) return; const paneIndicators = activeIndicators.filter(i => ['RSI', 'MACD', 'StochRSI', 'ADX', 'ATR'].includes(i.type)); const paneCount = paneIndicators.length; const PANE_HEIGHT = 0.2; const mainChartHeight = 1.0 - (paneCount * PANE_HEIGHT); chartRef.current.priceScale('right').applyOptions({ scaleMargins: { top: 0.05, bottom: paneCount * PANE_HEIGHT } }); volumeSeriesRef.current.priceScale().applyOptions({ scaleMargins: { top: mainChartHeight - 0.15, bottom: paneCount * PANE_HEIGHT } }); paneIndicators.forEach((ind, index) => { const bottomPos = index * PANE_HEIGHT; const topPos = 1.0 - ((index + 1) * PANE_HEIGHT); if (ind.paneId) chartRef.current.priceScale(ind.paneId).applyOptions({ scaleMargins: { top: topPos, bottom: bottomPos } }); }); };
  useEffect(() => { updateLayout(); }, [activeIndicators]);

  // --- FETCH DATA ---
  const fetchData = useCallback(async (isSilent = false) => {
    if (!symbol) return;
    if (!isSilent && abortControllerRef.current) abortControllerRef.current.abort();
    if (!isSilent) abortControllerRef.current = new AbortController();

    try {
      if (!isSilent) { setIsChartLoading(true); setHasError(false); }
      const response = await axios.get(`/api/stocks/${symbol}/chart?range=${timeframe}`, { signal: !isSilent ? abortControllerRef.current.signal : undefined });
      const data = response.data;
      const validData = (data || []).filter(d => d && d.time && typeof d.open === 'number');

      if (isMounted.current && chartRef.current && candleSeriesRef.current) {
          if (validData.length > 0) {
              setChartData(validData);
              lastCandleRef.current = validData[validData.length - 1];
              
              const isSMC = activeIndicators.some(i => i.type === 'SMC');
              if (isSMC) applySMC(validData); 
              else candleSeriesRef.current.setData(validData);
              
              if (volumeSeriesRef.current) volumeSeriesRef.current.setData(validData.map(d => ({ time: d.time, value: d.volume || 0, color: d.close >= d.open ? 'rgba(63, 185, 80, 0.4)' : 'rgba(248, 81, 73, 0.4)' })));
              if (!isSilent) chartRef.current.timeScale().fitContent();
              setIsLive(true);
          } else { setHasError(true); setChartData([]); }
      }
    } catch (err) { if (!axios.isCancel(err)) setHasError(true); setIsLive(false); } finally { if (!isSilent && isMounted.current) setIsChartLoading(false); }
  }, [symbol, timeframe]);
  useEffect(() => { fetchData(false); }, [symbol, timeframe]);

  // --- HYBRID SOCKET ENGINE ---
  useEffect(() => {
    if (!symbol) return;
    const userToken = localStorage.getItem('fyers_token');
    let pingInterval = null;
    let ws = null;
    
    // A. DIRECT BROKER CONNECTION
    if (userToken && isIndian && window.FyersSocket) {
        setConnectionType("Broker");
        const fyersSymbol = `NSE:${symbol.replace('.NS', '-EQ').replace('.BO', '-EQ')}`;
        try {
            const fyersSocket = new window.FyersSocket(userToken);
            fyersSocket.onmessage = (msg) => {
                const tick = msg.d?.[0] || msg[0];
                if (tick && tick.v && tick.v.lp) {
                     const price = parseFloat(tick.v.lp);
                     if (lastCandleRef.current && candleSeriesRef.current) {
                         const last = lastCandleRef.current;
                         const updatedCandle = { ...last, close: price, high: Math.max(last.high, price), low: Math.min(last.low, price) };
                         lastCandleRef.current = updatedCandle;
                         try { candleSeriesRef.current.update(updatedCandle); } catch(e){}
                     }
                }
            };
            fyersSocket.connect();
            fyersSocket.subscribe([fyersSymbol]);
            fyersEngineRef.current = { disconnect: () => fyersSocket.close() }; 
        } catch(e) {}
        
    } else {
        // B. SERVER BROADCAST
        setConnectionType("Server");
        const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
        const wsHost = isLocal ? '127.0.0.1:8000' : window.location.host;
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${wsHost}/ws/live/${symbol}`;

        const connect = () => {
            try {
                ws = new WebSocket(wsUrl);
                ws.onopen = () => { pingInterval = setInterval(() => { if (isMounted.current && ws.readyState === WebSocket.OPEN) { ws.send("ping"); } }, 10000); };
                ws.onmessage = (event) => {
                    if (!chartRef.current || !candleSeriesRef.current || !isMounted.current) return;
                    try {
                        const data = JSON.parse(event.data);
                        const currentPrice = data.price;
                        if (currentPrice && lastCandleRef.current) {
                            const last = lastCandleRef.current;
                            const updatedCandle = { ...last, close: currentPrice, high: Math.max(last.high, currentPrice), low: Math.min(last.low, currentPrice) };
                            lastCandleRef.current = updatedCandle;
                            try { candleSeriesRef.current.update(updatedCandle); } catch(e){}
                        }
                    } catch(e) {}
                };
                ws.onclose = () => { if (pingInterval) clearInterval(pingInterval); if (isMounted.current) setTimeout(connect, 3000); };
            } catch (e) {}
        };
        connect();
    }
    return () => { 
        if (pingInterval) clearInterval(pingInterval);
        if (ws) ws.close();
        if (fyersEngineRef.current) fyersEngineRef.current.disconnect();
    };
  }, [symbol, isIndian]);

  // --- INDICATORS ---
  const applySMC = (data) => { if (!isMounted.current || !candleSeriesRef.current) return; const { markers, coloredCandles, priceLines } = calculateSMC(data); const coloredData = data.map(d => { const override = coloredCandles.find(c => c.time === d.time); return override ? { ...d, ...override } : d; }); candleSeriesRef.current.setData(coloredData); if (candleSeriesRef.current.setMarkers) candleSeriesRef.current.setMarkers(markers); priceLinesRef.current.forEach(line => { try { candleSeriesRef.current.removePriceLine(line); } catch(e){} }); priceLinesRef.current = []; priceLines.slice(-5).forEach(lineData => { if (candleSeriesRef.current.createPriceLine) { const lineObj = candleSeriesRef.current.createPriceLine({ price: lineData.price, color: lineData.color, lineWidth: 2, lineStyle: 0, axisLabelVisible: true, title: lineData.title, }); priceLinesRef.current.push(lineObj); } }); };
  useEffect(() => { if (!isMounted.current || !chartRef.current || chartData.length === 0) return; const isSMC = activeIndicators.some(i => i.type === 'SMC'); if (isSMC) applySMC(chartData); else { candleSeriesRef.current.setData(chartData); if (candleSeriesRef.current.setMarkers) candleSeriesRef.current.setMarkers([]); priceLinesRef.current.forEach(line => { try { candleSeriesRef.current.removePriceLine(line); } catch(e){} }); priceLinesRef.current = []; } }, [chartData, activeIndicators]);

  const addIndicator = () => {
    if (!isMounted.current || !chartData.length || !chartRef.current) return;
    const closePrices = chartData.map(d => d.close);
    const highs = chartData.map(d => d.high);
    const lows = chartData.map(d => d.low);
    const volumes = chartData.map(d => d.volume);
    const id = Date.now();
    let newSeries = [];
    let paneId = ['RSI', 'MACD', 'StochRSI', 'ADX', 'ATR'].includes(selectedInd) ? `pane_${id}` : undefined;
    let paramsLabel = '';

    try {
        if (selectedInd === 'SMC') {} 
        else if (selectedInd === 'SMA') {
            const period = parseInt(param1);
            const res = SMA.calculate({period, values: closePrices});
            const series = chartRef.current.addSeries(LineSeries, { color: '#FF9800', lineWidth: 2, title: `SMA ${period}` });
            series.setData(mapData(res, chartData));
            newSeries.push(series);
            paramsLabel = `${period}`;
        }
        else if (selectedInd === 'EMA') {
            const period = parseInt(param1);
            const res = EMA.calculate({period, values: closePrices});
            const series = chartRef.current.addSeries(LineSeries, { color: '#2962FF', lineWidth: 2, title: `EMA ${period}` });
            series.setData(mapData(res, chartData));
            newSeries.push(series);
            paramsLabel = `${period}`;
        }
        else if (selectedInd === 'SuperTrend') {
            const period = parseInt(param1);
            const mult = parseFloat(param3);
            const stData = calculateSuperTrend(chartData, period, mult);
            const series = chartRef.current.addSeries(LineSeries, { color: '#00E676', lineWidth: 2, title: `ST ${period}/${mult}` });
            series.setData(stData);
            newSeries.push(series);
            paramsLabel = `${period}, ${mult}`;
        }
        else if (selectedInd === 'VWAP') {
            const res = VWAP.calculate({ high: highs, low: lows, close: closePrices, volume: volumes });
            const series = chartRef.current.addSeries(LineSeries, { color: '#FFD700', lineWidth: 2, title: `VWAP` });
            series.setData(mapData(res, chartData));
            newSeries.push(series);
        }
        else if (selectedInd === 'RSI') {
            const res = RSI.calculate({ values: closePrices, period: parseInt(param1) });
            const series = chartRef.current.addSeries(LineSeries, { color: '#A855F7', lineWidth: 2, priceScaleId: paneId, title: `RSI (${param1})` });
            series.setData(mapData(res, chartData));
            newSeries.push(series);
            chartRef.current.priceScale(paneId).applyOptions({ scaleMargins: { top: 0.8, bottom: 0 } });
            paramsLabel = `${param1}`;
        }
        else if (selectedInd === 'MACD') {
            const macdInput = { values: closePrices, fastPeriod: parseInt(param1), slowPeriod: parseInt(param2), signalPeriod: parseInt(param3), SimpleMAOscillator: false, SimpleMASignal: false };
            const res = MACD.calculate(macdInput);
            const mLine = []; const sLine = []; const hLine = [];
            for(let i=0; i<res.length; i++){ const dIndex = chartData.length - 1 - i; const rIndex = res.length - 1 - i; if (dIndex >= 0){ const t = chartData[dIndex].time; const m = res[rIndex]; mLine.unshift({ time: t, value: m.MACD }); sLine.unshift({ time: t, value: m.signal }); hLine.unshift({ time: t, value: m.histogram, color: m.histogram >= 0 ? '#26a69a' : '#ef5350' }); } }
            const hSeries = chartRef.current.addSeries(HistogramSeries, { priceScaleId: paneId });
            const mSeries = chartRef.current.addSeries(LineSeries, { color: '#2962FF', lineWidth: 2, priceScaleId: paneId });
            const sSeries = chartRef.current.addSeries(LineSeries, { color: '#FF6D00', lineWidth: 2, priceScaleId: paneId });
            hSeries.setData(hLine); mSeries.setData(mLine); sSeries.setData(sLine);
            newSeries = [hSeries, mSeries, sSeries];
            chartRef.current.priceScale(paneId).applyOptions({ scaleMargins: { top: 0.8, bottom: 0 } });
            paramsLabel = `${param1},${param2},${param3}`;
        }
        else if (selectedInd === 'StochRSI') {
            const stochInput = { values: closePrices, rsiPeriod: parseInt(param1), stochasticPeriod: parseInt(param2), kPeriod: 3, dPeriod: 3 };
            const res = StochasticRSI.calculate(stochInput);
            const kLine = []; const dLine = [];
            for(let i=0; i<res.length; i++){ const dIndex = chartData.length - 1 - i; const sIndex = res.length - 1 - i; if (dIndex >= 0) { kLine.unshift({ time: chartData[dIndex].time, value: res[sIndex].k }); dLine.unshift({ time: chartData[dIndex].time, value: res[sIndex].d }); } }
            const kSeries = chartRef.current.addSeries(LineSeries, { color: '#2962FF', title: '%K', priceScaleId: paneId });
            const dSeries = chartRef.current.addSeries(LineSeries, { color: '#FF6D00', title: '%D', priceScaleId: paneId });
            kSeries.setData(kLine); dSeries.setData(dLine);
            newSeries = [kSeries, dSeries];
            chartRef.current.priceScale(paneId).applyOptions({ scaleMargins: { top: 0.8, bottom: 0 } });
            paramsLabel = `${param1},${param2}`;
        }
        else if (selectedInd === 'ADX') {
            const res = ADX.calculate({ high: highs, low: lows, close: closePrices, period: parseInt(param1) });
            const series = chartRef.current.addSeries(LineSeries, { color: '#FF0055', lineWidth: 2, priceScaleId: paneId, title: `ADX (${param1})` });
            series.setData(mapData(res.map(r=>r.adx), chartData));
            newSeries.push(series);
            paramsLabel = `${param1}`;
        }
        else if (selectedInd === 'ATR') {
            const res = ATR.calculate({ high: highs, low: lows, close: closePrices, period: parseInt(param1) });
            const series = chartRef.current.addSeries(LineSeries, { color: '#AB47BC', lineWidth: 2, priceScaleId: paneId, title: `ATR (${param1})` });
            series.setData(mapData(res, chartData));
            newSeries.push(series);
            paramsLabel = `${param1}`;
        }
        else if (selectedInd === 'Combo_9_21') {
             const ema1 = EMA.calculate({ period: 9, values: closePrices });
             const ema2 = EMA.calculate({ period: 21, values: closePrices });
             const s1 = chartRef.current.addSeries(LineSeries, { color: '#2962FF', lineWidth: 2, title: `EMA 9` });
             const s2 = chartRef.current.addSeries(LineSeries, { color: '#FF6D00', lineWidth: 2, title: `EMA 21` });
             s1.setData(mapData(ema1, chartData));
             s2.setData(mapData(ema2, chartData));
             newSeries.push(s1, s2);
             paramsLabel = `9, 21`;
        }
        else if (selectedInd === 'Combo_12_21') {
             const ema1 = EMA.calculate({ period: 12, values: closePrices });
             const ema2 = EMA.calculate({ period: 21, values: closePrices });
             const s1 = chartRef.current.addSeries(LineSeries, { color: '#2962FF', lineWidth: 2, title: `EMA 12` });
             const s2 = chartRef.current.addSeries(LineSeries, { color: '#FF6D00', lineWidth: 2, title: `EMA 21` });
             s1.setData(mapData(ema1, chartData));
             s2.setData(mapData(ema2, chartData));
             newSeries.push(s1, s2);
             paramsLabel = `12, 21`;
        }

        setActiveIndicators([...activeIndicators, { id, type: selectedInd, series: newSeries, paneId, params: paramsLabel }]);
        setIsMenuOpen(false);
    } catch (e) {
        console.error("Indicator Error", e);
    }
  };

  const handleDropdownChange = (e) => { const val = e.target.value; setSelectedInd(val); if (val === 'Combo_9_21') { setParam1(9); setParam2(21); } else if (val === 'Combo_12_21') { setParam1(12); setParam2(21); } };
  const removeIndicator = (id) => { const indToRemove = activeIndicators.find(i => i.id === id); if (!indToRemove) return; if (indToRemove.type !== 'SMC') { if (chartRef.current) indToRemove.series.forEach(s => chartRef.current.removeSeries(s)); } setActiveIndicators(activeIndicators.filter(i => i.id !== id)); };

  const timeframesList = ['5M', '15M', '1H', '4H', '1D', '1W', '1M'];
  let helpText = ''; if (drawMode === 'fib') helpText = 'Click Low then High'; if (drawMode === 'trend') helpText = 'Click Start then End'; if (drawMode === 'longshort') helpText = 'Click Entry, Stop, Target';

  return (
    <ChartWrapper>
      {/* ... (UI Components) ... */}
      <DrawingSidebar><ToolBtn active={drawMode === 'cursor'} onClick={() => setDrawMode('cursor')} title="Cursor"><FaMousePointer /></ToolBtn><ToolBtn active={drawMode === 'horizontal'} onClick={() => setDrawMode('horizontal')} title="Horizontal Line"><FaMinus /></ToolBtn><ToolBtn active={drawMode === 'trend'} onClick={() => setDrawMode('trend')} title="Trend Line"><FaSlash /></ToolBtn><ToolBtn active={drawMode === 'fib'} onClick={() => setDrawMode('fib')} title="Fibonacci Retracement"><FaListOl /></ToolBtn><ToolBtn active={drawMode === 'rect'} onClick={() => setDrawMode('rect')} title="Zone (Box)"><FaVectorSquare /></ToolBtn><ToolBtn active={drawMode === 'longshort'} onClick={() => setDrawMode('longshort')} title="Long/Short Tool"><FaBalanceScale /></ToolBtn><ToolBtn onClick={undoLastDrawing} title="Undo Last"><FaUndo /></ToolBtn><ToolBtn onClick={clearDrawings} title="Clear All" style={{color: '#F85149'}}><FaEraser /></ToolBtn></DrawingSidebar>
      {userDrawings.length > 0 && (<LayersPanel><LayerHeader><span>Drawing Layers</span></LayerHeader>{userDrawings.map((d, i) => (<LayerItem key={d.id}><span>{d.type === 'horizontal' ? 'H-Line' : d.type === 'rect' ? 'Zone' : d.type === 'fib' ? 'Fibonacci' : d.type.toUpperCase()}</span><LayerActions><IconButton onClick={() => handleEdit(d)}><FaPencilAlt size={10} /></IconButton><IconButton className="delete" onClick={() => deleteDrawing(d.id)}><FaTrash size={10} /></IconButton></LayerActions></LayerItem>))}</LayersPanel>)}
      {editingDrawing && (<EditModal><ModalTitle>Edit Drawing</ModalTitle><ModalInput><label>Price / Level 1</label><input type="number" value={editValues.p1} onChange={e=>setEditValues({...editValues, p1: e.target.value})} /></ModalInput>{editValues.p2 !== undefined && <ModalInput><label>Price / Level 2</label><input type="number" value={editValues.p2} onChange={e=>setEditValues({...editValues, p2: e.target.value})} /></ModalInput>}{editValues.p3 !== undefined && <ModalInput><label>Price / Level 3</label><input type="number" value={editValues.p3} onChange={e=>setEditValues({...editValues, p3: e.target.value})} /></ModalInput>}<ModalActions><AddButton onClick={() => setEditingDrawing(null)} style={{background:'#30363D'}}>Cancel</AddButton><AddButton onClick={saveEdit}>Save Changes</AddButton></ModalActions></EditModal>)}
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
                        <select style={{background: '#0D1117', color:'white', padding:'5px', borderRadius:'4px', width:'100%'}} value={selectedInd} onChange={handleDropdownChange}>
                            <option value="SMC">⚡ SMC</option><option value="Combo_9_21">🚀 9/21 EMA</option><option value="Combo_12_21">🚀 12/21 EMA</option><option value="SuperTrend">SuperTrend</option><option value="VWAP">VWAP</option><option value="SMA">SMA</option><option value="EMA">EMA</option><option value="RSI">RSI</option><option value="MACD">MACD</option><option value="StochRSI">Stoch RSI</option><option value="ADX">ADX</option><option value="ATR">ATR</option>
                        </select>
                        {selectedInd !== 'SMC' && selectedInd !== 'VWAP' && ( <><div style={{fontSize:'0.8rem', color:'#8b949e'}}>Settings:</div><InputGroup><StyledInput type="number" value={param1} onChange={e=>setParam1(e.target.value)} title="Period/Fast" />{['MACD', 'StochRSI'].includes(selectedInd) && (<><StyledInput type="number" value={param2} onChange={e=>setParam2(e.target.value)} title="Slow" /><StyledInput type="number" value={param3} onChange={e=>setParam3(e.target.value)} title="Signal" /></>)}{selectedInd === 'SuperTrend' && ( <StyledInput type="number" value={param3} onChange={e=>setParam3(e.target.value)} title="Multiplier" /> )}</InputGroup></> )}
                        <AddButton onClick={addIndicator}>Add {selectedInd}</AddButton>
                    </Dropdown>
                )}
            </div>
        </LeftGroup>
        <div style={{display:'flex', gap:'5px', overflowX:'auto'}}>
            {activeIndicators.map(ind => (
                <IndicatorTag key={ind.id}>{ind.type} {ind.params && `(${ind.params})`}<CloseIcon onClick={() => removeIndicator(ind.id)} /></IndicatorTag>
            ))}
        </div>
        <StatusText isLive={isLive}>
            {isLive ? (
                <>
                    <PulseDot /> {connectionType === "Broker" ? "BROKER FEED" : "LIVE"}
                    {connectionType === "Broker" && <FaPlug style={{marginLeft:'5px'}} />}
                </>
            ) : <><FaSpinner className="fa-spin" style={{fontSize:'0.8rem'}}/> LOADING...</>}
        </StatusText>
      </Toolbar>
      
      {isChartLoading && ( <LoadingOverlay><FaSpinner className="fa-spin" /></LoadingOverlay> )}
      {hasError && !isChartLoading && (
          <NoDataOverlay>
              <FaExclamationTriangle style={{fontSize: '2rem', marginBottom: '10px'}} />
              <span>Chart Data Unavailable</span>
          </NoDataOverlay>
      )}
      {drawMode !== 'cursor' && <HelperText>{helpText}</HelperText>}
      <ChartContainer ref={chartContainerRef} crosshair={drawMode !== 'cursor'} />
    </ChartWrapper>
  );
};

export default CustomChart;