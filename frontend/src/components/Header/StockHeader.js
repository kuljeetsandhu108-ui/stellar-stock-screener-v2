import React, { useState, useEffect, useRef } from 'react';
import styled, { keyframes, css } from 'styled-components';
import ConnectBroker from './ConnectBroker';

// ==========================================
// 1. HIGH-END ANIMATIONS
// ==========================================

const flashGreen = keyframes`
  0% { color: var(--color-text-primary); text-shadow: none; }
  10% { color: #3FB950; text-shadow: 0 0 15px rgba(63, 185, 80, 0.8); transform: scale(1.05); }
  100% { color: var(--color-text-primary); text-shadow: none; transform: scale(1); }
`;

const flashRed = keyframes`
  0% { color: var(--color-text-primary); text-shadow: none; }
  10% { color: #F85149; text-shadow: 0 0 15px rgba(248, 81, 73, 0.8); transform: scale(1.05); }
  100% { color: var(--color-text-primary); text-shadow: none; transform: scale(1); }
`;

const pulse = keyframes`
  0% { opacity: 1; box-shadow: 0 0 0 0 rgba(63, 185, 80, 0.7); }
  70% { opacity: 1; box-shadow: 0 0 0 6px rgba(63, 185, 80, 0); }
  100% { opacity: 1; box-shadow: 0 0 0 0 rgba(63, 185, 80, 0); }
`;

// ==========================================
// 2. STYLED COMPONENTS (Glassmorphism)
// ==========================================

const HeaderContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background: linear-gradient(145deg, #161B22, #0D1117);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  gap: 1rem;
  width: 100%;
  box-sizing: border-box;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3); 
  backdrop-filter: blur(10px);
  
  @media (min-width: 768px) {
    flex-direction: row;
    align-items: center;
    gap: 0;
  }
`;

const CompanyInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 1.2rem;
  max-width: 100%;
  min-width: 0; 
`;

const CompanyLogo = styled.img`
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background-color: #fff;
  padding: 4px;
  object-fit: contain;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  flex-shrink: 0;
  border: 1px solid rgba(255,255,255,0.1);
  
  @media (min-width: 768px) {
      width: 64px;
      height: 64px;
  }
`;

const TextContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-width: 0; 
`;

const TopRow = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
`;

const CompanyName = styled.h1`
  font-size: 1.4rem;
  font-weight: 800;
  margin: 0;
  line-height: 1.2;
  color: var(--color-text-primary);
  white-space: normal; 
  word-wrap: break-word;
  letter-spacing: -0.5px;

  @media (min-width: 768px) {
    font-size: 2.2rem;
    white-space: nowrap;
  }
`;

const CompanySymbol = styled.span`
  font-size: 0.85rem;
  color: var(--color-text-secondary);
  font-weight: 600;
  background: rgba(255,255,255,0.05);
  padding: 2px 8px;
  border-radius: 6px;
  display: inline-block;
  font-family: 'Roboto Mono', monospace;
  border: 1px solid rgba(255,255,255,0.05);
  
  @media (min-width: 768px) {
      font-size: 1rem;
  }
`;

const PriceInfo = styled.div`
  text-align: left;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  
  @media (min-width: 768px) {
    text-align: right;
    align-items: flex-end;
  }
`;

const CurrentPrice = styled.div`
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 0.25rem;
  font-family: 'Roboto Mono', monospace;
  color: var(--color-text-primary);
  
  ${({ flash }) => flash === 'up' && css`animation: ${flashGreen} 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;`}
  ${({ flash }) => flash === 'down' && css`animation: ${flashRed} 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;`}

  @media (min-width: 768px) {
      font-size: 2.8rem;
  }
`;

const PriceChange = styled.div`
  font-size: 1.1rem;
  font-weight: 600;
  color: ${({ isPositive }) => (isPositive ? '#3FB950' : '#F85149')};
  display: flex;
  align-items: center;
  gap: 8px;
  background: ${({ isPositive }) => (isPositive ? 'rgba(63, 185, 80, 0.1)' : 'rgba(248, 81, 73, 0.1)')};
  padding: 4px 12px;
  border-radius: 20px;
  border: 1px solid ${({ isPositive }) => (isPositive ? 'rgba(63, 185, 80, 0.2)' : 'rgba(248, 81, 73, 0.2)')};
  
  @media (min-width: 768px) {
      font-size: 1.2rem;
  }
`;

const LiveDot = styled.div`
  width: 8px;
  height: 8px;
  background-color: #3FB950;
  border-radius: 50%;
  animation: ${pulse} 2s infinite;
`;

const ConnectionStatus = styled.div`
    font-size: 0.65rem;
    color: var(--color-text-secondary);
    margin-top: 5px;
    display: flex;
    align-items: center;
    gap: 4px;
    opacity: 0.7;
`;

// ==========================================
// 3. INTELLIGENT HELPER FUNCTIONS
// ==========================================

const getCurrencySymbol = (currencyCode, symbol) => {
    // 1. Priority: Explicit Symbol Check for India
    if (symbol) {
        const s = symbol.toUpperCase();
        if (s.includes('.NS') || s.includes('.BO') || s.includes('NIFTY') || s.includes('SENSEX') || s.includes('BANKNIFTY')) {
            return '₹';
        }
    }
    
    // 2. Fallback: Currency Code
    switch (currencyCode) {
        case 'INR': return '₹';
        case 'USD': return '$';
        case 'JPY': return '¥';
        case 'EUR': return '€';
        case 'GBP': return '£';
        default: return '$';
    }
};

// ==========================================
// 4. MAIN COMPONENT LOGIC
// ==========================================

const StockHeader = ({ profile, quote: initialQuote }) => {
  // State for Real-Time Data
  const [liveData, setLiveData] = useState({
    price: 0,
    change: 0,
    pct: 0
  });
  
  const [flash, setFlash] = useState(null); // 'up', 'down', or null
  const [isConnected, setIsConnected] = useState(false);
  const prevPriceRef = useRef(0);
  const wsRef = useRef(null);

  // --- SAFE INITIALIZATION ---
  useEffect(() => {
    if (initialQuote) {
        setLiveData({ 
            price: Number(initialQuote.price) || 0, 
            change: Number(initialQuote.change) || 0, 
            pct: Number(initialQuote.changesPercentage) || 0 
        });
        prevPriceRef.current = Number(initialQuote.price) || 0;
    }
  }, [initialQuote]);
  
  // --- REAL WEBSOCKET ENGINE WITH HEARTBEAT ---
  useEffect(() => {
    // Crash Guard: Don't run if symbol is missing
    const symbol = profile?.symbol;
    if (!symbol) return;

    // 1. Construct WebSocket URL Dynamically (Local vs Production)
    const apiUrl = process.env.REACT_APP_API_URL;
    let wsUrl = "";
    
    if (apiUrl) {
         // Production (Vercel -> Railway)
         const host = apiUrl.replace(/^https?:\/\//, '');
         const proto = apiUrl.includes('https') ? 'wss://' : 'ws://';
         wsUrl = `${proto}${host}/ws/live/${symbol}`;
    } else {
         // Default Localhost
         const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
         const wsHost = isLocal ? '127.0.0.1:8000' : window.location.host;
         const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
         wsUrl = `${protocol}//${wsHost}/ws/live/${symbol}`;
    }

    let pingInterval = null;

    const connect = () => {
        try {
            // Close existing connection if any
            if (wsRef.current) wsRef.current.close();
            
            const ws = new WebSocket(wsUrl);
            wsRef.current = ws;

            ws.onopen = () => {
                setIsConnected(true);
                // --- HEARTBEAT ENGINE ---
                // Send "ping" every 10s to keep connection alive on Railway
                pingInterval = setInterval(() => {
                    if (ws.readyState === WebSocket.OPEN) {
                        ws.send("ping");
                    }
                }, 10000); 
            };

            ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    const newPrice = Number(data.price); // Force Number
                    
                    if (newPrice && newPrice !== prevPriceRef.current) {
                        // Flash Logic
                        if (newPrice > prevPriceRef.current) setFlash('up');
                        else if (newPrice < prevPriceRef.current) setFlash('down');
                        
                        setTimeout(() => setFlash(null), 800);

                        setLiveData({
                            price: newPrice,
                            change: Number(data.change) || 0,
                            pct: Number(data.percent_change) || 0
                        });
                        prevPriceRef.current = newPrice;
                    }
                } catch (e) {
                    // Ignore parsing errors
                }
            };

            ws.onclose = () => {
                setIsConnected(false);
                if (pingInterval) clearInterval(pingInterval);
                // Auto Reconnect if connection drops
                setTimeout(connect, 3000);
            };
        } catch(e) {
            console.error("WS Connect Error", e);
        }
    };

    connect();

    // Cleanup on unmount
    return () => {
        if (pingInterval) clearInterval(pingInterval);
        if (wsRef.current) wsRef.current.close();
    };
  }, [profile?.symbol]);

  // --- RENDER SAFEGUARDS ---
  if (!profile) return null; // Don't render until data exists
  
  const symbol = profile.symbol || "";
  const currencySymbol = getCurrencySymbol(profile.currency, symbol);
  
  // Safe Formatting (Prevents .toFixed crash)
  const safePrice = Number(liveData.price) || 0;
  const safeChange = Number(liveData.change) || 0;
  const safePct = Number(liveData.pct) || 0;

  const isPositive = safeChange >= 0;
  const formattedPrice = safePrice.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const formattedChange = safeChange.toFixed(2);
  const formattedPct = safePct.toFixed(2);

  // Check if Indian stock (to show button)
  const isIndian = symbol.includes('.NS') || symbol.includes('.BO') || symbol.includes('NIFTY') || symbol.includes('SENSEX');

  return (
    <HeaderContainer>
      <CompanyInfo>
        {profile.image ? (
            <CompanyLogo 
                src={profile.image} 
                alt={`${profile.companyName} logo`} 
                onError={(e) => e.target.style.display='none'} 
            />
        ) : null}
        <TextContainer>
          <TopRow>
            <CompanyName>
                {profile.companyName}
            </CompanyName>
            {/* --- CONNECT BROKER BUTTON --- */}
            {isIndian && <ConnectBroker />} 
          </TopRow>
          
          <div style={{display:'flex', alignItems:'center', gap:'10px'}}>
             <CompanySymbol>{symbol}</CompanySymbol>
             {isConnected && (
                  <ConnectionStatus>
                      <LiveDot style={{width:'6px', height:'6px'}}/> Live
                  </ConnectionStatus>
             )}
          </div>
        </TextContainer>
      </CompanyInfo>
      
      <PriceInfo>
        <CurrentPrice flash={flash}>
          {currencySymbol}{formattedPrice}
        </CurrentPrice>
        <PriceChange isPositive={isPositive}>
            {isPositive ? '▲' : '▼'}
            {formattedChange} ({isPositive ? '+' : ''}{formattedPct}%)
        </PriceChange>
      </PriceInfo>
    </HeaderContainer>
  );
};

export default StockHeader;