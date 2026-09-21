import React, { useState, useEffect, useRef } from 'react';
import styled, { keyframes, css } from 'styled-components';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa';

const fadeIn = keyframes`from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); }`;
const flashGreen = keyframes`0% { color: var(--color-text-primary); } 10% { color: #3FB950; text-shadow: 0 0 15px rgba(63, 185, 80, 0.6); } 100% { color: var(--color-text-primary); }`;
const flashRed = keyframes`0% { color: var(--color-text-primary); } 10% { color: #F85149; text-shadow: 0 0 15px rgba(248, 81, 73, 0.6); } 100% { color: var(--color-text-primary); }`;

const BannerContainer = styled.div`width: 100%; padding: 1rem 0; margin-bottom: 2rem; overflow: hidden; position: relative;`;
const CardScroller = styled.div`display: flex; gap: 1rem; overflow-x: auto; padding: 0.5rem; scroll-behavior: smooth; &::-webkit-scrollbar { display: none; }`;
const ScrollArrow = styled.button`position: absolute; top: 50%; transform: translateY(-50%); width: 36px; height: 36px; border-radius: 50%; background: rgba(22, 27, 34, 0.9); border: 1px solid var(--color-border); color: var(--color-text-primary); display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 10; &:hover { background: var(--color-primary); color: #fff; } &.left { left: 10px; } &.right { right: 10px; }`;
const IndexCard = styled.div`flex-shrink: 0; width: 220px; padding: 1.2rem; background-color: var(--color-secondary); border: 1px solid var(--color-border); border-radius: 16px; cursor: pointer; transition: transform 0.2s ease, border-color 0.2s ease; animation: ${fadeIn} 0.5s ease-out; position: relative; display: flex; flex-direction: column; justify-content: space-between; &:hover { transform: translateY(-5px); border-color: var(--color-primary); }`;
const IndexHeader = styled.div`display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;`;
const IndexName = styled.h3`font-size: 0.95rem; font-weight: 600; color: var(--color-text-secondary); white-space: nowrap; margin: 0;`;
const CurrencyBadge = styled.span`font-size: 0.65rem; background: rgba(255, 255, 255, 0.08); padding: 2px 6px; border-radius: 4px; color: var(--color-text-secondary); font-weight: 700;`;
const IndexPrice = styled.div`font-size: 1.4rem; font-weight: 700; color: var(--color-text-primary); margin-bottom: 0.4rem; font-family: 'Roboto Mono', monospace; ${({ flash }) => flash === 'up' && css`animation: ${flashGreen} 0.5s ease-out;`} ${({ flash }) => flash === 'down' && css`animation: ${flashRed} 0.5s ease-out;`}`;
const IndexChange = styled.div`font-size: 0.85rem; font-weight: 600; display: flex; align-items: center; gap: 6px; color: ${({ isPositive }) => (isPositive ? 'var(--color-success)' : 'var(--color-danger)')};`;
const ConnectionDot = styled.div`position: absolute; top: 10px; right: 10px; width: 6px; height: 6px; border-radius: 50%; background-color: ${({ active }) => active ? '#3FB950' : 'transparent'}; box-shadow: ${({ active }) => active ? '0 0 5px #3FB950' : 'none'};`;

const getCurrencySymbol = (code) => {
    switch (code) { case 'INR': return '\u20B9'; case 'USD': return '$'; case 'JPY': return '\u00A5'; case 'EUR': return '\u20AC'; default: return '$'; }
};

const IndicesBanner = () => {
  const [indices, setIndices] = useState([]);
  const [flashStates, setFlashStates] = useState({});
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef(null);
  const scrollRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    let isMounted = true;
    axios.get('/api/indices/summary')
      .then(res => { if (res.data && Array.isArray(res.data) && isMounted) setIndices(res.data); })
      .catch(() => {});
    return () => { isMounted = false; };
  }, []);

  useEffect(() => {
    const getWsUrl = () => {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        return `${protocol}//${host}/ws/live/MARKET_OVERVIEW`;
    };

    let pingInterval = null;
    const connect = () => {
        if (wsRef.current?.readyState === WebSocket.OPEN) return;
        const ws = new WebSocket(getWsUrl());
        wsRef.current = ws;

        ws.onopen = () => {
            setIsConnected(true);
            pingInterval = setInterval(() => { if (ws.readyState === WebSocket.OPEN) ws.send("ping"); }, 10000);
        };

        ws.onmessage = (event) => {
            try {
                const update = JSON.parse(event.data);
                const symbol = update.symbol;
                if (!symbol) return;

                setIndices(prev => prev.map(idx => {
                    if (idx.symbol === symbol) {
                        const newPrice = Number(update.price) || idx.price;
                        if (newPrice !== idx.price) {
                            const dir = newPrice > idx.price ? 'up' : 'down';
                            setFlashStates(f => ({ ...f, [symbol]: dir }));
                            setTimeout(() => setFlashStates(f => { const next = { ...f }; delete next[symbol]; return next; }), 600);
                        }
                        return { ...idx, price: newPrice, change: update.change, percent_change: update.percent_change };
                    }
                    return idx;
                }));
            } catch(e) {}
        };

        ws.onclose = () => {
            setIsConnected(false);
            if (pingInterval) clearInterval(pingInterval);
            setTimeout(connect, 3000);
        };
    };

    connect();
    return () => { if (pingInterval) clearInterval(pingInterval); if (wsRef.current) wsRef.current.close(); };
  }, []);

  const handleCardClick = (symbol) => {
    navigate(`/index/${encodeURIComponent(symbol)}`);
  };

  const scroll = (dir) => {
    if (scrollRef.current) {
        const amount = window.innerWidth > 768 ? 500 : 250;
        scrollRef.current.scrollBy({ left: dir === 'left' ? -amount : amount, behavior: 'smooth' });
    }
  };

  if (indices.length === 0) return null;

  return (
    <BannerContainer>
      <ScrollArrow className="left" onClick={() => scroll('left')}><FaChevronLeft size={12} /></ScrollArrow>
      <CardScroller ref={scrollRef}>
        {indices.map(index => {
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
              <IndexPrice flash={flash}>{symbol}{safePrice.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</IndexPrice>
              <IndexChange isPositive={isPositive}>{isPositive ? '▲' : '▼'} {Math.abs(safeChange).toFixed(2)} ({safePct.toFixed(2)}%)</IndexChange>
            </IndexCard>
          );
        })}
      </CardScroller>
      <ScrollArrow className="right" onClick={() => scroll('right')}><FaChevronRight size={12} /></ScrollArrow>
    </BannerContainer>
  );
};

export default IndicesBanner;
