import React, { useState, useEffect, useRef } from 'react';
import styled, { keyframes, css } from 'styled-components';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

// ==========================================
// 1. HIGH-END ANIMATIONS
// ==========================================

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
`;

const flashGreen = keyframes`
  0% { color: var(--color-text-primary); transform: scale(1); }
  10% { color: #3FB950; text-shadow: 0 0 15px rgba(63, 185, 80, 0.6); transform: scale(1.05); }
  100% { color: var(--color-text-primary); transform: scale(1); }
`;

const flashRed = keyframes`
  0% { color: var(--color-text-primary); transform: scale(1); }
  10% { color: #F85149; text-shadow: 0 0 15px rgba(248, 81, 73, 0.6); transform: scale(1.05); }
  100% { color: var(--color-text-primary); transform: scale(1); }
`;

// ==========================================
// 2. STYLED COMPONENTS
// ==========================================

const BannerContainer = styled.div`
  width: 100%;
  padding: 1rem 0;
  margin-bottom: 2rem;
  overflow: hidden;
`;

const CardScroller = styled.div`
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding: 0.5rem;
  
  /* Hide scrollbar for sleek look */
  &::-webkit-scrollbar { display: none; }
  -ms-overflow-style: none;
  scrollbar-width: none;
`;

const IndexCard = styled.div`
  flex-shrink: 0;
  width: 220px;
  padding: 1.2rem;
  background-color: var(--color-secondary);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  animation: ${fadeIn} 0.5s ease-out;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    border-color: var(--color-primary);
  }
`;

const IndexHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
`;

const IndexName = styled.h3`
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--color-text-secondary);
  white-space: nowrap;
  margin: 0;
  letter-spacing: 0.5px;
`;

const CurrencyBadge = styled.span`
  font-size: 0.65rem;
  background: rgba(255, 255, 255, 0.08);
  padding: 2px 6px;
  border-radius: 4px;
  color: var(--color-text-secondary);
  font-weight: 700;
`;

const IndexPrice = styled.div`
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 0.4rem;
  font-family: 'Roboto Mono', monospace;
  
  /* Dynamic Flashing Logic */
  ${({ flash }) => flash === 'up' && css`animation: ${flashGreen} 0.5s ease-out;`}
  ${({ flash }) => flash === 'down' && css`animation: ${flashRed} 0.5s ease-out;`}
`;

const IndexChange = styled.div`
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  color: ${({ isPositive }) => (isPositive ? 'var(--color-success)' : 'var(--color-danger)')};
`;

const ConnectionDot = styled.div`
  position: absolute;
  top: 10px;
  right: 10px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: ${({ active }) => active ? '#3FB950' : 'transparent'};
  box-shadow: ${({ active }) => active ? '0 0 5px #3FB950' : 'none'};
  transition: background-color 0.3s ease;
`;

// ==========================================
// 3. LOGIC & COMPONENT
// ==========================================

const getCurrencySymbol = (code) => {
    switch (code) { 
        case 'INR': return '₹'; 
        case 'USD': return '$'; 
        case 'JPY': return '¥'; 
        case 'EUR': return '€'; 
        default: return '$'; 
    }
};

const IndicesBanner = () => {
  const [indices, setIndices] = useState([]);
  const [flashStates, setFlashStates] = useState({});
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef(null);
  const navigate = useNavigate();
  const isMounted = useRef(true);

  // --- 1. INITIAL LOAD (REST API) ---
  useEffect(() => {
    isMounted.current = true;
    const loadInitial = async () => {
        try {
            // Use Environment Variable for Flexibility (Vercel vs Local)
            const baseUrl = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
            const res = await axios.get(`${baseUrl}/api/indices/summary`);
            
            if (res.data && Array.isArray(res.data) && isMounted.current) {
                setIndices(res.data);
            }
        } catch(e) {
            console.error("Initial load failed", e);
        }
    };
    loadInitial();
    
    return () => { isMounted.current = false; };
  }, []);

  // --- 2. LIVE WEBSOCKET ENGINE ---
  useEffect(() => {
    // Dynamic URL Construction (Works on Vercel & Localhost)
    const getWsUrl = () => {
        const apiUrl = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
        const wsProtocol = apiUrl.includes('https') ? 'wss://' : 'ws://';
        const host = apiUrl.replace(/^https?:\/\//, '');
        // Connect to the specific channel for homepage ticker
        return `${wsProtocol}${host}/ws/live/MARKET_OVERVIEW`;
    };

    const wsUrl = getWsUrl();
    let pingInterval = null;

    const connect = () => {
        if (wsRef.current?.readyState === WebSocket.OPEN) return;

        const ws = new WebSocket(wsUrl);
        wsRef.current = ws;

        ws.onopen = () => {
            if (!isMounted.current) return;
            setIsConnected(true);
            
            // Heartbeat: Keep connection alive on Railway
            pingInterval = setInterval(() => {
                if (ws.readyState === WebSocket.OPEN) {
                    ws.send("ping");
                }
            }, 10000); 
        };

        ws.onmessage = (event) => {
            if (!isMounted.current) return;
            try {
                const update = JSON.parse(event.data);
                const symbol = update.symbol; 
                
                if (!symbol) return;

                setIndices(prevIndices => {
                    return prevIndices.map(idx => {
                        // Match incoming update to existing card
                        if (idx.symbol === symbol) {
                            
                            // Visual Flash Logic
                            if (update.price !== idx.price) {
                                const dir = update.price > idx.price ? 'up' : 'down';
                                
                                setFlashStates(prev => ({ ...prev, [symbol]: dir }));
                                
                                // Clear flash after animation
                                setTimeout(() => {
                                    if (isMounted.current) {
                                        setFlashStates(prev => {
                                            const next = { ...prev };
                                            delete next[symbol];
                                            return next;
                                        });
                                    }
                                }, 600);
                            }
                            
                            // Return Updated Card Data
                            return {
                                ...idx,
                                price: update.price,
                                change: update.change,
                                percent_change: update.percent_change
                            };
                        }
                        return idx; // No change for this card
                    });
                });
            } catch(e) {
                // Silent fail for keep-alive packets
            }
        };
        
        ws.onclose = () => {
            if (isMounted.current) setIsConnected(false);
            if (pingInterval) clearInterval(pingInterval);
            // Auto-Reconnect after 3 seconds if connection drops
            if (isMounted.current) setTimeout(connect, 3000);
        };
    };

    connect();

    // Cleanup on Unmount
    return () => { 
        if (pingInterval) clearInterval(pingInterval);
        if(wsRef.current) wsRef.current.close(); 
    };
  }, []);

  const handleCardClick = (symbol) => {
    navigate(`/index/${encodeURIComponent(symbol)}`);
  };

  // Render nothing until data loads (prevents empty flashes)
  if (indices.length === 0) return null;

  return (
    <BannerContainer>
      <CardScroller>
        {indices.map(index => {
          // Safe Number Conversion (Fixes .toFixed crash)
          const safePrice = Number(index.price) || 0;
          const safeChange = Number(index.change) || 0;
          const safePct = Number(index.percent_change) || 0;
          
          const isPositive = safeChange >= 0;
          const symbol = getCurrencySymbol(index.currency);
          const flash = flashStates[index.symbol];
          
          return (
            <IndexCard key={index.symbol} onClick={() => handleCardClick(index.symbol)}>
              <ConnectionDot active={isConnected} />
              <IndexHeader>
                <IndexName>{index.name}</IndexName>
                <CurrencyBadge>{index.currency}</CurrencyBadge>
              </IndexHeader>
              
              <IndexPrice flash={flash}>
                {symbol}{safePrice.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </IndexPrice>
              
              <IndexChange isPositive={isPositive}>
                {isPositive ? '▲' : '▼'} 
                {Math.abs(safeChange).toFixed(2)} ({safePct.toFixed(2)}%)
              </IndexChange>
            </IndexCard>
          );
        })}
      </CardScroller>
    </BannerContainer>
  );
};

export default IndicesBanner;