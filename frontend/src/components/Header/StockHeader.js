import React, { useState, useEffect, useRef } from 'react';
import styled, { keyframes, css } from 'styled-components';

const flashGreen = keyframes`0% { color: var(--color-text-primary); } 10% { color: #3FB950; text-shadow: 0 0 15px rgba(63, 185, 80, 0.8); } 100% { color: var(--color-text-primary); }`;
const flashRed = keyframes`0% { color: var(--color-text-primary); } 10% { color: #F85149; text-shadow: 0 0 15px rgba(248, 81, 73, 0.8); } 100% { color: var(--color-text-primary); }`;
const pulse = keyframes`0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; }`;

const HeaderContainer = styled.div`display: flex; flex-direction: column; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; padding: 1.5rem; background: linear-gradient(145deg, #161B22, #0D1117); border: 1px solid var(--color-border); border-radius: 16px; gap: 1rem; width: 100%; box-sizing: border-box; box-shadow: 0 8px 32px rgba(0,0,0,0.3); @media (min-width: 768px) { flex-direction: row; align-items: center; gap: 0; }`;
const CompanyInfo = styled.div`display: flex; align-items: center; gap: 1.2rem;`;
const TextContainer = styled.div`display: flex; flex-direction: column;`;
const CompanyName = styled.h1`font-size: 1.4rem; font-weight: 800; margin: 0; line-height: 1.2; color: var(--color-text-primary); @media (min-width: 768px) { font-size: 2.2rem; }`;
const CompanySymbol = styled.span`font-size: 0.85rem; color: var(--color-text-secondary); font-weight: 600; background: rgba(255,255,255,0.05); padding: 2px 8px; border-radius: 6px; font-family: 'Roboto Mono', monospace; border: 1px solid rgba(255,255,255,0.05);`;
const PriceInfo = styled.div`text-align: left; display: flex; flex-direction: column; align-items: flex-start; @media (min-width: 768px) { text-align: right; align-items: flex-end; }`;
const CurrentPrice = styled.div`font-size: 2rem; font-weight: 800; margin-bottom: 0.25rem; font-family: 'Roboto Mono', monospace; color: var(--color-text-primary); ${({ flash }) => flash === 'up' && css`animation: ${flashGreen} 0.6s both;`} ${({ flash }) => flash === 'down' && css`animation: ${flashRed} 0.6s both;`} @media (min-width: 768px) { font-size: 2.8rem; }`;
const PriceChange = styled.div`font-size: 1.1rem; font-weight: 600; color: ${({ isPositive }) => (isPositive ? '#3FB950' : '#F85149')}; display: flex; align-items: center; gap: 8px; background: ${({ isPositive }) => (isPositive ? 'rgba(63, 185, 80, 0.1)' : 'rgba(248, 81, 73, 0.1)')}; padding: 4px 12px; border-radius: 20px; border: 1px solid ${({ isPositive }) => (isPositive ? 'rgba(63, 185, 80, 0.2)' : 'rgba(248, 81, 73, 0.2)')};`;
const LiveDot = styled.div`width: 8px; height: 8px; background-color: #3FB950; border-radius: 50%; animation: ${pulse} 2s infinite;`;
const ConnectionStatus = styled.div`font-size: 0.65rem; color: var(--color-text-secondary); margin-top: 5px; display: flex; align-items: center; gap: 4px;`;

const getCurrencySymbol = (currencyCode, symbol) => {
    if (symbol && (symbol.includes('.NS') || symbol.includes('.BO') || symbol.includes('NIFTY') || symbol.includes('SENSEX') || symbol.includes('^NSE'))) {
        return '\u20B9';
    }
    return currencyCode === 'INR' ? '\u20B9' : '$';
};

const StockHeader = ({ profile, quote: initialQuote }) => {
  const [liveData, setLiveData] = useState({ price: 0, change: 0, pct: 0 });
  const [flash, setFlash] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const prevPriceRef = useRef(0);

  useEffect(() => {
    if (initialQuote) {
        const p = Number(initialQuote.price) || 0;
        setLiveData({ price: p, change: Number(initialQuote.change) || 0, pct: Number(initialQuote.changesPercentage) || 0 });
        prevPriceRef.current = p;
    }
  }, [initialQuote]);

  useEffect(() => {
    const symbol = profile?.symbol;
    if (!symbol) return;

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const wsUrl = `${protocol}//${host}/ws/live/${encodeURIComponent(symbol)}`;

    let ws = null;
    let pingInterval = null;

    const connect = () => {
        try {
            ws = new WebSocket(wsUrl);
            ws.onopen = () => {
                setIsConnected(true);
                pingInterval = setInterval(() => { if (ws.readyState === WebSocket.OPEN) ws.send("ping"); }, 10000);
            };
            ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    const newPrice = Number(data.price);
                    if (newPrice && newPrice !== prevPriceRef.current) {
                        setFlash(newPrice > prevPriceRef.current ? 'up' : 'down');
                        setTimeout(() => setFlash(null), 800);
                        setLiveData({ price: newPrice, change: Number(data.change) || 0, pct: Number(data.percent_change) || 0 });
                        prevPriceRef.current = newPrice;
                    }
                } catch(e) {}
            };
            ws.onclose = () => {
                setIsConnected(false);
                if (pingInterval) clearInterval(pingInterval);
                setTimeout(connect, 3000);
            };
        } catch(e) {}
    };

    connect();
    return () => { if (pingInterval) clearInterval(pingInterval); if (ws) ws.close(); };
  }, [profile?.symbol]);

  if (!profile) return null;

  const symbol = profile.symbol || "";
  const currencySymbol = getCurrencySymbol(profile.currency, symbol);
  const safePrice = Number(liveData.price) || 0;
  const safeChange = Number(liveData.change) || 0;
  const safePct = Number(liveData.pct) || 0;
  const isPositive = safeChange >= 0;

  return (
    <HeaderContainer>
      <CompanyInfo>
        <TextContainer>
          <CompanyName>{profile.companyName}</CompanyName>
          <div style={{display:'flex', alignItems:'center', gap:'10px', marginTop:'6px'}}>
             <CompanySymbol>{symbol}</CompanySymbol>
             {isConnected && <ConnectionStatus><LiveDot /> Live Broadcast Feed</ConnectionStatus>}
          </div>
        </TextContainer>
      </CompanyInfo>
      
      <PriceInfo>
        <CurrentPrice flash={flash}>
          {currencySymbol}{safePrice.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
        </CurrentPrice>
        <PriceChange isPositive={isPositive}>
            {isPositive ? '▲' : '▼'} {Math.abs(safeChange).toFixed(2)} ({isPositive ? '+' : ''}{safePct.toFixed(2)}%)
        </PriceChange>
      </PriceInfo>
    </HeaderContainer>
  );
};

export default StockHeader;
