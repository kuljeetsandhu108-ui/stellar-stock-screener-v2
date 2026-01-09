import React, { useState, useEffect, useRef } from 'react';
import styled, { keyframes, css } from 'styled-components';
import axios from 'axios';

// --- ANIMATIONS ---
const flashGreen = keyframes`
  0% { color: var(--color-text-primary); }
  50% { color: #3FB950; text-shadow: 0 0 10px #3FB950; }
  100% { color: var(--color-text-primary); }
`;

const flashRed = keyframes`
  0% { color: var(--color-text-primary); }
  50% { color: #F85149; text-shadow: 0 0 10px #F85149; }
  100% { color: var(--color-text-primary); }
`;

const pulse = keyframes`
  0% { opacity: 1; box-shadow: 0 0 0 0 rgba(63, 185, 80, 0.7); }
  70% { opacity: 1; box-shadow: 0 0 0 6px rgba(63, 185, 80, 0); }
  100% { opacity: 1; box-shadow: 0 0 0 0 rgba(63, 185, 80, 0); }
`;

// --- STYLED COMPONENTS ---

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
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);

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

  @media (min-width: 768px) {
    font-size: 2.2rem;
    white-space: nowrap;
  }
`;

const CompanySymbol = styled.span`
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  font-weight: 600;
  background: rgba(255,255,255,0.05);
  padding: 2px 8px;
  border-radius: 4px;
  margin-top: 6px;
  display: inline-block;
  font-family: 'Roboto Mono', monospace;
  
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
  
  /* Blinking Logic */
  ${({ flash }) => flash === 'up' && css`animation: ${flashGreen} 1s ease;`}
  ${({ flash }) => flash === 'down' && css`animation: ${flashRed} 1s ease;`}

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

// --- Helper ---
const getCurrencySymbol = (currencyCode) => {
    switch (currencyCode) {
        case 'INR': return '₹';
        case 'USD': return '$';
        case 'JPY': return '¥';
        case 'EUR': return '€';
        case 'GBP': return '£';
        default: return '$';
    }
};

const StockHeader = ({ profile, quote: initialQuote }) => {
  const [liveData, setLiveData] = useState({
    price: initialQuote?.price || 0,
    change: initialQuote?.change || 0,
    pct: initialQuote?.changesPercentage || 0
  });
  
  const [flash, setFlash] = useState(null); // 'up' or 'down' or null
  const prevPriceRef = useRef(initialQuote?.price || 0);
  const intervalRef = useRef(null);

  // --- REAL-TIME POLLING ENGINE ---
  useEffect(() => {
    // Reset state on symbol change
    if (initialQuote) {
        setLiveData({
            price: initialQuote.price,
            change: initialQuote.change,
            pct: initialQuote.changesPercentage
        });
        prevPriceRef.current = initialQuote.price;
    }

    const fetchLivePrice = async () => {
      try {
        const symbol = profile.symbol;
        if (!symbol) return;

        // Determine correct endpoint based on asset type
        // Index -> use indices router. Stock -> use chart as proxy (fastest).
        let url = '';
        const isIndex = profile.sector === 'Market Index' || profile.exchange === 'INDEX' || symbol.includes('.INDX');
        
        if (isIndex) {
            // Encode symbol to handle ^NSEI etc safely
            url = `/api/indices/${encodeURIComponent(symbol)}/live-price`;
        } else {
            // Fetch only 1 day of chart data (lightweight) to get the latest close
            url = `/api/stocks/${symbol}/chart?range=1D`;
        }

        const res = await axios.get(url);
        
        let newPrice = 0;
        let newChange = 0;
        let newPct = 0;

        if (isIndex) {
            // Index response: { price, change, changesPercentage ... }
            newPrice = res.data.price;
            newChange = res.data.change;
            newPct = res.data.changesPercentage;
        } else {
            // Stock response (Chart array): [{close: ...}, ...]
            const candles = res.data;
            if (candles && candles.length > 0) {
                const last = candles[candles.length - 1];
                newPrice = last.close;
                
                // Keep the change relative to the initial Previous Close to be consistent
                const prevClose = initialQuote.previousClose || candles[0].open;
                newChange = newPrice - prevClose;
                newPct = (newChange / prevClose) * 100;
            }
        }

        // Only update if we have a valid price
        if (newPrice > 0) {
            // Trigger Flash Animation
            if (newPrice > prevPriceRef.current) setFlash('up');
            else if (newPrice < prevPriceRef.current) setFlash('down');
            
            // Remove flash class after animation
            setTimeout(() => setFlash(null), 1000);

            setLiveData({ price: newPrice, change: newChange, pct: newPct });
            prevPriceRef.current = newPrice;
        }

      } catch (err) {
        // Silent fail on polling error to keep UI stable
        // console.error("Poll skip");
      }
    };

    // 2-Second Polling for "Live" Feel
    intervalRef.current = setInterval(fetchLivePrice, 2000);

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [profile.symbol, profile.sector, profile.exchange, initialQuote]);

  if (!profile) return null;
  
  const currencySymbol = getCurrencySymbol(profile.currency);
  const isPositive = liveData.change >= 0;

  return (
    <HeaderContainer>
      <CompanyInfo>
        {profile.image ? (
            <CompanyLogo src={profile.image} alt={`${profile.companyName} logo`} onError={(e) => e.target.style.display='none'} />
        ) : null}
        <TextContainer>
          <CompanyName>
            {profile.companyName}
            <span style={{ display: 'inline-block' }}>
               <CompanySymbol>{profile.symbol}</CompanySymbol>
            </span>
          </CompanyName>
        </TextContainer>
      </CompanyInfo>
      
      <PriceInfo>
        <CurrentPrice flash={flash}>
          {currencySymbol}{(liveData.price || 0).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
        </CurrentPrice>
        <PriceChange isPositive={isPositive}>
            <LiveDot />
            {isPositive ? '+' : ''}{(liveData.change || 0).toFixed(2)} ({isPositive ? '+' : ''}{(liveData.pct || 0).toFixed(2)}%)
        </PriceChange>
      </PriceInfo>
    </HeaderContainer>
  );
};

export default StockHeader;