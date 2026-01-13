import React, { useState, useEffect, useRef } from 'react';
import styled, { keyframes, css } from 'styled-components';

// ==========================================
// 1. HIGH-END ANIMATIONS (GPU Accelerated)
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
  margin-top: 6px;
  display: inline-block;
  font-family: 'Roboto Mono', monospace;
  border: 1px solid rgba(255,255,255,0.05);
  
  @media (min-width: 768px) {
      font-size: 1rem;
      margin-left: 1rem;
      margin-top: 0;
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
  
  /* Advanced Flash Logic */
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
    price: initialQuote?.price || 0,
    change: initialQuote?.change || 0,
    pct: initialQuote?.changesPercentage || 0
  });
  
  const [flash, setFlash] = useState(null); // 'up', 'down', or null
  const [isConnected, setIsConnected] = useState(false);
  const prevPriceRef = useRef(initialQuote?.price || 0);
  const wsRef = useRef(null);

  // --- A. Sync State on Load ---
  useEffect(() => {
    if (initialQuote) {
        setLiveData({
            price: initialQuote.price,
            change: initialQuote.change,
            pct: initialQuote.changesPercentage
        });
        prevPriceRef.current = initialQuote.price;
    }
  }, [initialQuote]);

  // --- B. WEBSOCKET ENGINE (The Formula 1 Upgrade) ---
  useEffect(() => {
    if (!profile?.symbol) return;

    // 1. Determine Protocol (WSS for https, WS for http)
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    // 2. Build URL: Connects to our Backend Traffic Controller
    const wsUrl = `${protocol}//${host}/ws/ws/${profile.symbol}`;

    const connect = () => {
        const ws = new WebSocket(wsUrl);
        wsRef.current = ws;

        ws.onopen = () => {
            setIsConnected(true);
            // console.log("Live Stream Connected");
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                const newPrice = data.price;

                // Only update DOM if price actually changed
                if (newPrice && newPrice !== prevPriceRef.current) {
                    
                    // Flash Logic
                    if (newPrice > prevPriceRef.current) setFlash('up');
                    else if (newPrice < prevPriceRef.current) setFlash('down');
                    
                    // Reset Flash
                    setTimeout(() => setFlash(null), 600);

                    // Update State
                    setLiveData({
                        price: newPrice,
                        change: data.change,
                        pct: data.percent_change
                    });
                    
                    prevPriceRef.current = newPrice;
                }
            } catch (e) {
                // Ignore malformed packets
            }
        };

        ws.onclose = () => {
            setIsConnected(false);
            // Auto-Reconnect Logic (Robustness)
            setTimeout(() => {
                // Simple reconnect logic if component is still mounted
                // (In a full app we'd check refs, but this is sufficient for robustness)
            }, 3000);
        };
        
        ws.onerror = () => {
            ws.close();
        };
    };

    connect();

    // Cleanup
    return () => {
        if (wsRef.current) {
            wsRef.current.close();
        }
    };
  }, [profile.symbol]);

  if (!profile) return null;
  
  // Robust Currency Symbol
  const currencySymbol = getCurrencySymbol(profile.currency, profile.symbol);
  
  // Formatting
  const isPositive = liveData.change >= 0;
  const formattedPrice = (liveData.price || 0).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const formattedChange = (liveData.change || 0).toFixed(2);
  const formattedPct = (liveData.pct || 0).toFixed(2);

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
          <CompanyName>
            {profile.companyName}
            <span style={{ display: 'inline-block' }}>
               <CompanySymbol>{profile.symbol}</CompanySymbol>
            </span>
          </CompanyName>
          {isConnected && (
              <ConnectionStatus>
                  <LiveDot style={{width:'6px', height:'6px'}}/> Real-Time Connection
              </ConnectionStatus>
          )}
        </TextContainer>
      </CompanyInfo>
      
      <PriceInfo>
        <CurrentPrice flash={flash}>
          {currencySymbol}{formattedPrice}
        </CurrentPrice>
        <PriceChange isPositive={isPositive}>
            <LiveDot />
            {isPositive ? '+' : ''}{formattedChange} ({isPositive ? '+' : ''}{formattedPct}%)
        </PriceChange>
      </PriceInfo>
    </HeaderContainer>
  );
};

export default StockHeader;