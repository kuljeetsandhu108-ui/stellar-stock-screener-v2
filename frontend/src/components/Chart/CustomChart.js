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
  FaMinus, FaSlash, FaVectorSquare, FaListOl, FaBalanceScale, FaEraser, FaUndo, FaPencilAlt, FaTrash
} from 'react-icons/fa';

// --- STYLED COMPONENTS ---

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
  box-shadow: 4px 0 15px rgba(0,0,0,0.3);
`;

const ToolBtn = styled.button`
  width: 36px;
  height: 36px;
  border-radius: 6px;
  border: 1px solid ${({ active }) => active ? 'var(--color-primary)' : 'transparent'};
  background: ${({ active }) => active ? 'rgba(88, 166, 255, 0.15)' : 'transparent'};
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
  top: 50%; left: 50%;
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


// --- SMC & SUPERTREND HELPERS ---
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
    markers.sort((a, b) => a.time - b.time);
    const uniqueMarkers = []; const seenTimes = new Set();
    for (let m of markers) { if (!seenTimes.has(m.time)) { uniqueMarkers.push(m); seenTimes.add(m.time); } }
    return { markers: uniqueMarkers, coloredCandles, priceLines };
};

// --- MAIN COMPONENT ---

const CustomChart = ({ symbol }) => {
  const chartContainerRef = useRef();
  
  // Instance Refs
  const chartRef = useRef(null);
  const candleSeriesRef = useRef(null);
  const volumeSeriesRef = useRef(null);
  
  // Refs for drawings
  const priceLinesRef = useRef([]); // SMC lines
  const drawingObjectsRef = useRef([]); // User drawings
  const previewObjectsRef = useRef([]); // Temporary drawing objects
  
  const [timeframe, setTimeframe] = useState('1D'); 
  const [chartData, setChartData] = useState([]);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeIndicators, setActiveIndicators] = useState([]);
  const [isLive, setIsLive] = useState(false);
  
  // Drawing State
  const [drawMode, setDrawMode] = useState('cursor'); 
  const [tempPoints, setTempPoints] = useState([]);
  const [userDrawings, setUserDrawings] = useState([]); 
  
  const [editingDrawing, setEditingDrawing] = useState(null);
  const [editValues, setEditValues] = useState({});

  const [selectedInd, setSelectedInd] = useState('SMC');
  const [param1, setParam1] = useState(20);
  const [param2, setParam2] = useState(26);
  const [param3, setParam3] = useState(9);

  // Sync state refs
  const drawModeRef = useRef(drawMode);
  const tempPointsRef = useRef(tempPoints);
  const userDrawingsRef = useRef(userDrawings);

  useEffect(() => { 
      drawModeRef.current = drawMode; 
      if(drawMode === 'cursor') {
          setTempPoints([]);
          clearPreview();
      }
  }, [drawMode]);
  
  useEffect(() => { tempPointsRef.current = tempPoints; }, [tempPoints]);
  useEffect(() => { userDrawingsRef.current = userDrawings; }, [userDrawings]);

  // --- 1. INITIALIZATION ---
  useEffect(() => {
    if (!chartContainerRef.current) return;
    chartContainerRef.current.innerHTML = '';
    
    priceLinesRef.current = [];
    drawingObjectsRef.current = [];
    previewObjectsRef.current = [];

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

    // --- CLICK HANDLER ---
    chart.subscribeClick((param) => {
      if (!param.point || !param.time || !candleSeries) return;
      const price = candleSeries.coordinateToPrice(param.point.y);
      const time = param.time;
      const mode = drawModeRef.current;
      const id = Date.now();

      if (mode === 'cursor') return;

      if (mode === 'horizontal') {
          setUserDrawings(prev => [...prev, { id, type: 'horizontal', price, title: 'H-Line' }]);
          setDrawMode('cursor');
          return;
      }
      if (mode === 'rect') {
           setUserDrawings(prev => [...prev, { id, type: 'rect', price, title: 'Zone' }]);
           return;
      }

      if (['fib', 'trend', 'longshort'].includes(mode)) {
          handleMultiClickTool(price, time, mode === 'longshort' ? 3 : 2, (points) => {
              setUserDrawings(prev => [...prev, { id, type: mode, points }]);
          });
      }
    });

    // --- MOUSE MOVE ---
    chart.subscribeCrosshairMove((param) => {
        const mode = drawModeRef.current;
        const currentPoints = tempPointsRef.current;
        if (mode === 'cursor' || currentPoints.length === 0 || !param.point || !param.time) return;
        
        const currentPrice = candleSeries.coordinateToPrice(param.point.y);
        const currentTime = param.time;
        const start = currentPoints[0];
        
        // CRITICAL FIX: Skip preview drawing if times are equal (prevents infinite loop/stack overflow)
        if (currentTime === start.time) return;

        // ONLY draw preview for Fib and LongShort. Skip Trend line preview to be safe.
        if (mode === 'trend') return; 

        drawPreviewShape(mode, start, { price: currentPrice, time: currentTime }, chart, candleSeries);
    });

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

  const handleMultiClickTool = (price, time, requiredClicks, callback) => {
      setTempPoints(prev => {
          const newPoints = [...prev, { price, time }];
          if (newPoints.length === requiredClicks) {
              clearPreview();
              callback(newPoints);
              setDrawMode('cursor');
              return [];
          }
          return newPoints;
      });
  };

  // --- DRAWING HELPERS ---
  const clearPreview = () => {
      previewObjectsRef.current.forEach(obj => {
          if (obj.type === 'line' && candleSeriesRef.current) try{ candleSeriesRef.current.removePriceLine(obj.ref); } catch(e){}
          if (obj.type === 'series' && chartRef.current) try{ chartRef.current.removeSeries(obj.ref); } catch(e){}
      });
      previewObjectsRef.current = [];
  };

  const drawPreviewShape = (type, p1, p2, chart, series) => {
      clearPreview(); 

      if (type === 'fib') {
          const low = Math.min(p1.price, p2.price); const high = Math.max(p1.price, p2.price); const diff = high - low;
          const levels = [0, 0.5, 1]; 
          levels.forEach(lvl => {
              const line = series.createPriceLine({ price: low + (diff * lvl), color: '#FFD700', lineWidth: 1, lineStyle: 2, axisLabelVisible: false });
              previewObjectsRef.current.push({ type: 'line', ref: line });
          });
      }
      else if (type === 'longshort') {
          const l1 = series.createPriceLine({ price: p1.price, color: '#888', title: 'ENTRY' });
          const l2 = series.createPriceLine({ price: p2.price, color: '#3FB950', title: 'TARGET' });
          previewObjectsRef.current.push({ type: 'line', ref: l1 }, { type: 'line', ref: l2 });
      }
  };

  // --- 2. RENDER DRAWINGS ---
  useEffect(() => {
      if (!candleSeriesRef.current || !chartRef.current) return;

      drawingObjectsRef.current.forEach(item => {
          if (item.type === 'line') try { candleSeriesRef.current.removePriceLine(item.ref); } catch(e){}
          if (item.type === 'series') try { chartRef.current.removeSeries(item.ref); } catch(e){}
      });
      drawingObjectsRef.current = [];

      userDrawings.forEach(d => {
          if (d.type === 'horizontal') {
              const line = candleSeriesRef.current.createPriceLine({ price: d.price, color: '#38bdf8', lineWidth: 2, lineStyle: 0, axisLabelVisible: true, title: d.title });
              drawingObjectsRef.current.push({ type: 'line', ref: line });
          }
          else if (d.type === 'rect') {
              const line = candleSeriesRef.current.createPriceLine({ price: d.price, color: '#FBBF24', lineWidth: 3, lineStyle: 2, axisLabelVisible: false, title: d.title });
              drawingObjectsRef.current.push({ type: 'line', ref: line });
          }
          else if (d.type === 'fib') {
              const p1 = d.points[0]; const p2 = d.points[1];
              const low = Math.min(p1.price, p2.price); const high = Math.max(p1.price, p2.price); const diff = high - low;
              const levels = [{l:0,c:'#fff',w:1},{l:0.382,c:'#FFD700',w:2},{l:0.5,c:'#3FB950',w:2},{l:0.618,c:'#FFD700',w:2},{l:1,c:'#fff',w:1}];
              levels.forEach(lvl => {
                  const line = candleSeriesRef.current.createPriceLine({ price: low + (diff * lvl.l), color: lvl.c, lineWidth: lvl.w, lineStyle: 0, axisLabelVisible: true, title: `Fib ${lvl.l}` });
                  drawingObjectsRef.current.push({ type: 'line', ref: line });
              });
          }
          else if (d.type === 'trend') {
              // Always sort by time to prevent crash
              const sorted = d.points[0].time > d.points[1].time ? [d.points[1], d.points[0]] : [d.points[0], d.points[1]];
              const data = [{ time: sorted[0].time, value: sorted[0].price }, { time: sorted[1].time, value: sorted[1].price }];
              const series = chartRef.current.addSeries(LineSeries, { color: '#ffffff', lineWidth: 2, lastValueVisible: false, priceLineVisible: false });
              series.setData(data);
              drawingObjectsRef.current.push({ type: 'series', ref: series });
          }
          else if (d.type === 'longshort') {
               const entry = d.points[0].price; const stop = d.points[1].price; const target = d.points[2].price;
               const rr = Math.abs((target - entry) / (entry - stop)).toFixed(2);
               const l1 = candleSeriesRef.current.createPriceLine({ price: entry, color: '#888', title: 'ENTRY' });
               const l2 = candleSeriesRef.current.createPriceLine({ price: stop, color: '#F85149', title: 'STOP' });
               const l3 = candleSeriesRef.current.createPriceLine({ price: target, color: '#3FB950', title: `TARGET R:R ${rr}` });
               drawingObjectsRef.current.push({ type: 'line', ref: l1 }, { type: 'line', ref: l2 }, { type: 'line', ref: l3 });
          }
      });
  }, [userDrawings]);
  
  // --- 3. EDIT LOGIC ---
  const handleEdit = (d) => {
      setEditingDrawing(d.id);
      if (d.points) {
          setEditValues({ p1: d.points[0]?.price, p2: d.points[1]?.price, p3: d.points[2]?.price });
      } else {
          setEditValues({ p1: d.price });
      }
  };
  
  const saveEdit = () => {
      setUserDrawings(prev => prev.map(d => {
          if (d.id !== editingDrawing) return d;
          if (d.points) {
              const newPoints = [...d.points];
              if (editValues.p1) newPoints[0].price = parseFloat(editValues.p1);
              if (editValues.p2) newPoints[1].price = parseFloat(editValues.p2);
              if (editValues.p3 && newPoints[2]) newPoints[2].price = parseFloat(editValues.p3);
              return { ...d, points: newPoints };
          } else {
              return { ...d, price: parseFloat(editValues.p1) };
          }
      }));
      setEditingDrawing(null);
  };
  
  const deleteDrawing = (id) => setUserDrawings(prev => prev.filter(d => d.id !== id));
  
  const clearDrawings = () => {
      setUserDrawings([]); 
  };
  
  const undoLastDrawing = () => {
      if (userDrawings.length > 0) setUserDrawings(prev => prev.slice(0, -1));
  };

  // --- 4. LAYOUT & DATA ---
  const updateLayout = () => {
      if (!chartRef.current || !volumeSeriesRef.current) return;
      const paneIndicators = activeIndicators.filter(i => ['RSI', 'MACD', 'StochRSI', 'ADX', 'ATR'].includes(i.type));
      const paneCount = paneIndicators.length;
      const PANE_HEIGHT = 0.2; 
      const mainChartHeight = 1.0 - (paneCount * PANE_HEIGHT);

      chartRef.current.priceScale('right').applyOptions({ scaleMargins: { top: 0.05, bottom: paneCount * PANE_HEIGHT } });
      volumeSeriesRef.current.priceScale().applyOptions({ scaleMargins: { top: mainChartHeight - 0.15, bottom: paneCount * PANE_HEIGHT } });

      paneIndicators.forEach((ind, index) => {
          const bottomPos = index * PANE_HEIGHT;
          const topPos = 1.0 - ((index + 1) * PANE_HEIGHT);
          if (ind.paneId) chartRef.current.priceScale(ind.paneId).applyOptions({ scaleMargins: { top: topPos, bottom: bottomPos } });
      });
  };

  useEffect(() => { updateLayout(); }, [activeIndicators]);

  const fetchData = useCallback(async () => {
    if (!symbol) return;
    try {
      const response = await axios.get(`/api/stocks/${symbol}/chart?range=${timeframe}`);
      const data = response.data;
      if (chartRef.current && candleSeriesRef.current && data.length > 0) {
        setChartData(data);
        const isSMC = activeIndicators.some(i => i.type === 'SMC');
        if (isSMC) applySMC(data); else candleSeriesRef.current.setData(data);
        if (volumeSeriesRef.current) {
             const volData = data.map(d => ({
              time: d.time, value: d.volume,
              color: d.close >= d.open ? 'rgba(63, 185, 80, 0.4)' : 'rgba(248, 81, 73, 0.4)'
            }));
            volumeSeriesRef.current.setData(volData);
        }
        setIsLive(true);
      }
    } catch (err) { console.error("Chart Error:", err); setIsLive(false); }
  }, [symbol, timeframe]);

  // --- 5. SMC & INDICATORS ---
  const applySMC = (data) => {
      if (!candleSeriesRef.current) return;
      const { markers, coloredCandles, priceLines } = calculateSMC(data);
      const coloredData = data.map(d => {
          const override = coloredCandles.find(c => c.time === d.time);
          return override ? { ...d, ...override } : d;
      });
      candleSeriesRef.current.setData(coloredData);
      if (candleSeriesRef.current.setMarkers) candleSeriesRef.current.setMarkers(markers);
      priceLinesRef.current.forEach(line => { try { candleSeriesRef.current.removePriceLine(line); } catch(e){} });
      priceLinesRef.current = [];
      priceLines.slice(-5).forEach(lineData => {
            if (candleSeriesRef.current.createPriceLine) {
                const lineObj = candleSeriesRef.current.createPriceLine({
                    price: lineData.price, color: lineData.color, lineWidth: 2, lineStyle: 0, axisLabelVisible: true, title: lineData.title,
                });
                priceLinesRef.current.push(lineObj);
            }
      });
  };

  useEffect(() => {
    if (!chartRef.current || chartData.length === 0) return;
    const isSMC = activeIndicators.some(i => i.type === 'SMC');
    if (isSMC) applySMC(chartData);
    else {
        candleSeriesRef.current.setData(chartData);
        if (candleSeriesRef.current.setMarkers) candleSeriesRef.current.setMarkers([]);
        priceLinesRef.current.forEach(line => { try { candleSeriesRef.current.removePriceLine(line); } catch(e){} });
        priceLinesRef.current = [];
    }
  }, [chartData, activeIndicators]);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, [fetchData]);

  const addIndicator = () => {
    if (!chartData.length || !chartRef.current) return;
    const closePrices = chartData.map(d => d.close);
    const highs = chartData.map(d => d.high);
    const lows = chartData.map(d => d.low);
    const volumes = chartData.map(d => d.volume);
    const id = Date.now();
    let newSeries = [];
    let paneId = ['RSI', 'MACD', 'StochRSI', 'ADX', 'ATR'].includes(selectedInd) ? `pane_${id}` : undefined;

    try {
      if (selectedInd === 'SMC') { }
      else if (selectedInd === 'SMA') {
        const period = parseInt(param1); const res = SMA.calculate({ period, values: closePrices });
        const series = chartRef.current.addSeries(LineSeries, { color: '#FF9800', lineWidth: 2, title: `SMA ${period}` });
        series.setData(mapData(res, chartData)); newSeries.push(series);
      }
      else if (selectedInd === 'EMA') {
        const period = parseInt(param1); const res = EMA.calculate({ period, values: closePrices });
        const series = chartRef.current.addSeries(LineSeries, { color: '#2962FF', lineWidth: 2, title: `EMA ${period}` });
        series.setData(mapData(res, chartData)); newSeries.push(series);
      }
      else if (selectedInd === 'SuperTrend') {
        const period = parseInt(param1); const mult = parseFloat(param3);
        const stData = calculateSuperTrend(chartData, period, mult);
        const series = chartRef.current.addSeries(LineSeries, { color: '#00E676', lineWidth: 2, title: `ST ${period}/${mult}` });
        series.setData(stData); newSeries.push(series);
      }
      else if (selectedInd === 'VWAP') {
        const res = VWAP.calculate({ high: highs, low: lows, close: closePrices, volume: volumes });
        const series = chartRef.current.addSeries(LineSeries, { color: '#FFD700', lineWidth: 2, title: `VWAP` });
        series.setData(mapData(res, chartData)); newSeries.push(series);
      }
      else if (selectedInd === 'RSI') {
        const res = RSI.calculate({ values: closePrices, period: parseInt(param1) });
        const series = chartRef.current.addSeries(LineSeries, { color: '#A855F7', lineWidth: 2, priceScaleId: paneId, title: `RSI (${param1})` });
        series.setData(mapData(res, chartData)); newSeries.push(series);
      }
      else if (selectedInd === 'MACD') {
        const macdInput = { values: closePrices, fastPeriod: parseInt(param1), slowPeriod: parseInt(param2), signalPeriod: parseInt(param3), SimpleMAOscillator: false, SimpleMASignal: false };
        const res = MACD.calculate(macdInput);
        const mLine = []; const sLine = []; const hLine = [];
        for(let i=0; i<res.length; i++){
            const dIndex = chartData.length - 1 - i; const rIndex = res.length - 1 - i;
            if (dIndex >= 0){
                const t = chartData[dIndex].time; const m = res[rIndex];
                mLine.unshift({ time: t, value: m.MACD }); sLine.unshift({ time: t, value: m.signal }); hLine.unshift({ time: t, value: m.histogram, color: m.histogram >= 0 ? '#26a69a' : '#ef5350' });
            }
        }
        const hSeries = chartRef.current.addSeries(HistogramSeries, { priceScaleId: paneId });
        const mSeries = chartRef.current.addSeries(LineSeries, { color: '#2962FF', lineWidth: 2, priceScaleId: paneId });
        const sSeries = chartRef.current.addSeries(LineSeries, { color: '#FF6D00', lineWidth: 2, priceScaleId: paneId });
        hSeries.setData(hLine); mSeries.setData(mLine); sSeries.setData(sLine);
        newSeries = [hSeries, mSeries, sSeries];
      }
      else if (selectedInd === 'StochRSI') {
          const stochInput = { values: closePrices, rsiPeriod: parseInt(param1), stochasticPeriod: parseInt(param2), kPeriod: 3, dPeriod: 3 };
          const res = StochasticRSI.calculate(stochInput);
          const kLine = []; const dLine = [];
          for(let i=0; i<res.length; i++){
              const dIndex = chartData.length - 1 - i; const sIndex = res.length - 1 - i;
              if (dIndex >= 0) { kLine.unshift({ time: chartData[dIndex].time, value: res[sIndex].k }); dLine.unshift({ time: chartData[dIndex].time, value: res[sIndex].d }); }
          }
          const kSeries = chartRef.current.addSeries(LineSeries, { color: '#2962FF', title: '%K', priceScaleId: paneId });
          const dSeries = chartRef.current.addSeries(LineSeries, { color: '#FF6D00', title: '%D', priceScaleId: paneId });
          kSeries.setData(kLine); dSeries.setData(dLine); newSeries = [kSeries, dSeries];
      }
      else if (selectedInd === 'ADX') {
          const res = ADX.calculate({ high: highs, low: lows, close: closePrices, period: parseInt(param1) });
          const series = chartRef.current.addSeries(LineSeries, { color: '#FF0055', lineWidth: 2, priceScaleId: paneId, title: `ADX (${param1})` });
          series.setData(mapData(res.map(r=>r.adx), chartData)); newSeries.push(series);
      }
      else if (selectedInd === 'ATR') {
          const res = ATR.calculate({ high: highs, low: lows, close: closePrices, period: parseInt(param1) });
          const series = chartRef.current.addSeries(LineSeries, { color: '#AB47BC', lineWidth: 2, priceScaleId: paneId, title: `ATR (${param1})` });
          series.setData(mapData(res, chartData)); newSeries.push(series);
      }

      const paramsLabel = selectedInd === 'SMC' || selectedInd === 'VWAP' ? '' : selectedInd === 'SuperTrend' ? `${param1}, ${param3}` : ['MACD', 'StochRSI'].includes(selectedInd) ? `${param1},${param2},${param3}` : `${param1}`;
      setActiveIndicators([...activeIndicators, { id, type: selectedInd, series: newSeries, paneId, params: paramsLabel }]);
      setIsMenuOpen(false);

    } catch (e) { console.error("Indicator Calc Error", e); }
  };

  const mapData = (values, chartData) => {
    const output = [];
    for (let i = 0; i < values.length; i++) {
        const dIndex = chartData.length - 1 - i; const vIndex = values.length - 1 - i;
        if (dIndex >= 0) output.unshift({ time: chartData[dIndex].time, value: values[vIndex] });
    }
    return output;
  };

  const removeIndicator = (id) => {
      const indToRemove = activeIndicators.find(i => i.id === id);
      if (!indToRemove) return;
      if (indToRemove.type !== 'SMC') {
          if (chartRef.current) indToRemove.series.forEach(s => chartRef.current.removeSeries(s));
      }
      setActiveIndicators(activeIndicators.filter(i => i.id !== id));
  };

  const timeframesList = ['5M', '15M', '1H', '4H', '1D', '1W', '1M'];
  let helpText = '';
  if (drawMode === 'fib') helpText = 'Click Low then High';
  if (drawMode === 'trend') helpText = 'Click Start then End';
  if (drawMode === 'longshort') helpText = 'Click Entry, Stop, Target';

  return (
    <ChartWrapper>
      <DrawingSidebar>
        <ToolBtn active={drawMode === 'cursor'} onClick={() => setDrawMode('cursor')} title="Cursor"><FaMousePointer /></ToolBtn>
        <ToolBtn active={drawMode === 'horizontal'} onClick={() => setDrawMode('horizontal')} title="Horizontal Line"><FaMinus /></ToolBtn>
        <ToolBtn active={drawMode === 'trend'} onClick={() => setDrawMode('trend')} title="Trend Line"><FaSlash /></ToolBtn>
        <ToolBtn active={drawMode === 'fib'} onClick={() => setDrawMode('fib')} title="Fibonacci Retracement"><FaListOl /></ToolBtn>
        <ToolBtn active={drawMode === 'rect'} onClick={() => setDrawMode('rect')} title="Zone (Box)"><FaVectorSquare /></ToolBtn>
        <ToolBtn active={drawMode === 'longshort'} onClick={() => setDrawMode('longshort')} title="Long/Short Tool"><FaBalanceScale /></ToolBtn>
        <ToolBtn onClick={undoLastDrawing} title="Undo Last"><FaUndo /></ToolBtn>
        <ToolBtn onClick={clearDrawings} title="Clear All" style={{color: '#F85149'}}><FaEraser /></ToolBtn>
      </DrawingSidebar>

      {/* LAYERS PANEL */}
      {userDrawings.length > 0 && (
          <LayersPanel>
              <LayerHeader><span>Drawing Layers</span></LayerHeader>
              {userDrawings.map((d, i) => (
                  <LayerItem key={d.id}>
                      <span>{d.type === 'horizontal' ? 'H-Line' : d.type === 'rect' ? 'Zone' : d.type === 'fib' ? 'Fibonacci' : d.type.toUpperCase()}</span>
                      <LayerActions>
                          <IconButton onClick={() => handleEdit(d)}><FaPencilAlt size={10} /></IconButton>
                          <IconButton className="delete" onClick={() => deleteDrawing(d.id)}><FaTrash size={10} /></IconButton>
                      </LayerActions>
                  </LayerItem>
              ))}
          </LayersPanel>
      )}

      {/* EDIT MODAL */}
      {editingDrawing && (
          <EditModal>
              <ModalTitle>Edit Drawing</ModalTitle>
              <ModalInput><label>Price / Level 1</label><input type="number" value={editValues.p1} onChange={e=>setEditValues({...editValues, p1: e.target.value})} /></ModalInput>
              {editValues.p2 !== undefined && <ModalInput><label>Price / Level 2</label><input type="number" value={editValues.p2} onChange={e=>setEditValues({...editValues, p2: e.target.value})} /></ModalInput>}
              {editValues.p3 !== undefined && <ModalInput><label>Price / Level 3</label><input type="number" value={editValues.p3} onChange={e=>setEditValues({...editValues, p3: e.target.value})} /></ModalInput>}
              <ModalActions>
                  <AddButton onClick={() => setEditingDrawing(null)} style={{background:'#30363D'}}>Cancel</AddButton>
                  <AddButton onClick={saveEdit}>Save Changes</AddButton>
              </ModalActions>
          </EditModal>
      )}

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
                            <option value="SMC">⚡ SMC</option><option value="SuperTrend">SuperTrend</option><option value="VWAP">VWAP</option>
                            <option value="SMA">SMA</option><option value="EMA">EMA</option><option value="RSI">RSI</option><option value="MACD">MACD</option><option value="StochRSI">Stoch RSI</option><option value="ADX">ADX</option><option value="ATR">ATR</option>
                        </select>
                        {selectedInd !== 'SMC' && selectedInd !== 'VWAP' && (
                            <>
                            <div style={{fontSize:'0.8rem', color:'#8b949e'}}>Settings:</div>
                            <InputGroup>
                                <StyledInput type="number" value={param1} onChange={e=>setParam1(e.target.value)} title="Period/Fast" />
                                {['MACD', 'StochRSI'].includes(selectedInd) && (
                                    <><StyledInput type="number" value={param2} onChange={e=>setParam2(e.target.value)} title="Slow" /><StyledInput type="number" value={param3} onChange={e=>setParam3(e.target.value)} title="Signal" /></>
                                )}
                                {selectedInd === 'SuperTrend' && ( <StyledInput type="number" value={param3} onChange={e=>setParam3(e.target.value)} title="Multiplier" /> )}
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
      
      {drawMode !== 'cursor' && <HelperText>{helpText}</HelperText>}
      <ChartContainer ref={chartContainerRef} crosshair={drawMode !== 'cursor'} />
    </ChartWrapper>
  );
};

export default CustomChart;