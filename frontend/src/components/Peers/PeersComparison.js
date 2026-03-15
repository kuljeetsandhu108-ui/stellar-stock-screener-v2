import React, { useState, useEffect, useMemo } from 'react';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';
import Card from '../common/Card';
import { FaCrown, FaBalanceScale, FaChartLine, FaGlobe } from 'react-icons/fa';

// --- ANIMATIONS & STYLES ---
const fadeIn = keyframes`from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); }`;

const Loader = styled.div`display: flex; align-items: center; justify-content: center; height: 150px; color: var(--color-primary); font-weight: 500; letter-spacing: 1px;`;

// --- WINNER CARD UI ---
const WinnerCard = styled.div`
  background: linear-gradient(135deg, rgba(235, 203, 139, 0.1) 0%, rgba(13, 17, 23, 0.9) 100%);
  border: 1px solid #EBCB8B; border-radius: 12px; padding: 2rem; margin-bottom: 2rem;
  box-shadow: 0 10px 30px rgba(235, 203, 139, 0.05); animation: ${fadeIn} 0.5s ease-out;
  position: relative; overflow: hidden;
`;

const WinnerHeader = styled.div`
  display: flex; align-items: center; gap: 10px; color: #EBCB8B; font-weight: 800; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1rem;
`;

const WinnerSymbol = styled.h2`
  font-size: 2.5rem; font-weight: 900; color: #fff; margin: 0 0 0.5rem 0; font-family: 'Roboto Mono', monospace;
  text-shadow: 0 0 20px rgba(255,255,255,0.2);
`;

const WinnerScore = styled.div`
  position: absolute; top: 2rem; right: 2rem; background: rgba(63, 185, 80, 0.15); border: 1px solid #3FB950;
  color: #3FB950; padding: 10px 20px; border-radius: 50px; font-weight: 800; font-size: 1.2rem;
  box-shadow: 0 0 20px rgba(63, 185, 80, 0.2);
  @media (max-width: 768px) { position: relative; top: 0; right: 0; width: fit-content; margin-bottom: 1rem; }
`;

const RationaleText = styled.p`font-size: 1.05rem; color: #C9D1D9; line-height: 1.6; max-width: 800px; margin: 0;`;

const Highlight = styled.span`color: ${({ color }) => color}; font-weight: 700;`;

// --- TABLE UI ---
const TableContainer = styled.div`width: 100%; overflow-x: auto; border-radius: 12px; border: 1px solid var(--color-border); background: var(--color-secondary); animation: ${fadeIn} 0.7s ease-out;`;
const StyledTable = styled.table`width: 100%; border-collapse: collapse; min-width: 800px;`;
const Th = styled.th`text-align: left; padding: 16px; background: rgba(255, 255, 255, 0.03); color: var(--color-text-secondary); font-weight: 700; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 1px; border-bottom: 1px solid var(--color-border); cursor: pointer; transition: color 0.2s; &:hover{color: #fff;} &:last-child{text-align: right;}`;
const Tr = styled.tr`border-bottom: 1px solid rgba(255, 255, 255, 0.05); transition: background 0.2s; background-color: ${({ $isMain }) => $isMain ? 'rgba(88, 166, 255, 0.1)' : 'transparent'}; &:last-child { border-bottom: none; } &:hover { background: rgba(255, 255, 255, 0.03); }`;
const Td = styled.td`padding: 16px; font-size: 0.95rem; color: #C9D1D9; vertical-align: middle; font-family: 'Roboto Mono', monospace; &:first-child{font-weight: 700; color: var(--color-primary); font-family: 'Inter', sans-serif;} &:last-child{text-align: right;}`;

const ScoreBarContainer = styled.div`width: 100px; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden; margin-left: auto; display: inline-block; vertical-align: middle; margin-right: 10px;`;
const ScoreBarFill = styled.div`height: 100%; width: ${({ pct }) => pct}%; background: ${({ color }) => color}; border-radius: 3px;`;

// --- FORMATTERS ---
const formatMarketCap = (num) => {
  if (!num || isNaN(num)) return '--';
  if (Math.abs(num) >= 1e12) return `${(num / 1e12).toFixed(2)}T`;
  if (Math.abs(num) >= 1e9) return `${(num / 1e9).toFixed(2)}B`;
  if (Math.abs(num) >= 1e6) return `${(num / 1e6).toFixed(2)}M`;
  return num.toLocaleString();
};
const formatPercent = (num) => (!num || isNaN(num)) ? '--' : `${(num > 0 ? '+' : '')}${num.toFixed(2)}%`;
const formatNumber = (num) => (!num || isNaN(num) || num === 0) ? '--' : num.toFixed(2);

// --- MAIN COMPONENT ---
const PeersComparison = ({ symbol }) => {
  const [peersData, setPeersData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [sortConfig, setSortConfig] = useState({ key: 'smartScore', direction: 'descending' });

  useEffect(() => {
    let isMounted = true;
    if (!symbol) { setIsLoading(false); return; }
    
    axios.get(`/api/stocks/${symbol}/peers`)
      .then(res => { if(isMounted) setPeersData(res.data); })
      .catch(() => { if(isMounted) setPeersData([]); })
      .finally(() => { if(isMounted) setIsLoading(false); });
      
    return () => { isMounted = false; };
  }, [symbol]);

  // 💥 THE QUANTITATIVE SCORING ENGINE 💥
  const scoredPeers = useMemo(() => {
    if (!peersData || peersData.length === 0) return[];

    return peersData.map(peer => {
        let valueScore = 0;
        const pe = peer.peRatioTTM || 0;
        
        // 1. Value Math (Max 50 pts)
        if (pe > 0 && pe <= 15) valueScore = 50;
        else if (pe > 15 && pe <= 35) valueScore = 50 - ((pe - 15) * 2);
        else if (pe > 35) valueScore = Math.max(0, 10 - (pe - 35));

        // 2. Momentum Math (Max 50 pts)
        let momScore = 25; 
        const mom = peer.revenueGrowth || 0; 
        momScore += (mom * 2); 
        momScore = Math.min(Math.max(momScore, 0), 50);

        // 3. Mega-Cap Stability Bonus (Max 5 pts)
        let capBonus = 0;
        if (peer.marketCap > 1e11) capBonus = 2; 
        if (peer.marketCap > 1e12) capBonus = 5; 

        // 4. Total Calculation
        let totalScore = Math.min(valueScore + momScore + capBonus, 100);

        return { ...peer, smartScore: totalScore, valueScore, momScore };
    });
  },[peersData]);

  // Handle Sorting
  const sortedAndScored = useMemo(() => {
    let sortable = [...scoredPeers];
    sortable.sort((a, b) => {
        const aVal = a[sortConfig.key] || 0;
        const bVal = b[sortConfig.key] || 0;
        if (aVal < bVal) return sortConfig.direction === 'ascending' ? -1 : 1;
        if (aVal > bVal) return sortConfig.direction === 'ascending' ? 1 : -1;
        return 0;
    });
    return sortable;
  }, [scoredPeers, sortConfig]);

  const requestSort = (key) => {
    let dir = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') dir = 'descending';
    setSortConfig({ key, direction: dir });
  };

  const getScoreColor = (score) => {
      if (score >= 70) return '#3FB950';
      if (score >= 40) return '#EBCB8B';
      return '#F85149';
  };

  if (isLoading) return <Card title="Sector & Peers"><Loader>Compiling Sector Data...</Loader></Card>;
  if (!scoredPeers || scoredPeers.length <= 1) return <Card title="Sector & Peers"><p style={{color:'#8B949E'}}>Quantitative peer comparison unavailable.</p></Card>;

  // Find the absolute best stock in the sector
  const winner = [...scoredPeers].sort((a, b) => b.smartScore - a.smartScore)[0];
  
  // Mathematically generate the explanation
  let winReason = "";
  if (winner.valueScore >= 40 && winner.momScore >= 35) {
      winReason = `an exceptional balance of deep value (P/E: ${formatNumber(winner.peRatioTTM)}) and powerful upward momentum (${formatPercent(winner.revenueGrowth)}).`;
  } else if (winner.valueScore >= 40) {
      winReason = `a highly attractive valuation discount (P/E: ${formatNumber(winner.peRatioTTM)}) compared to its peers, limiting downside risk.`;
  } else if (winner.momScore >= 40) {
      winReason = `market-leading price momentum (${formatPercent(winner.revenueGrowth)}), indicating aggressive institutional accumulation.`;
  } else {
      winReason = `the most stable composite metrics in a currently weak sector environment.`;
  }

  return (
    <Card title="Sector & Peers">
      
      {/* 💥 THE QUANTITATIVE CONCLUSION WINNER CARD 💥 */}
      <WinnerCard>
          <WinnerHeader><FaCrown size={16} /> Quantitative Sector Leader</WinnerHeader>
          <WinnerScore>Score: {winner.smartScore.toFixed(0)}/100</WinnerScore>
          <WinnerSymbol>{winner.symbol}</WinnerSymbol>
          <RationaleText>
              Based on algorithmic ranking, <Highlight color="#fff">{winner.symbol}</Highlight> is currently the top-performing asset in this peer group. 
              The quantitative model selected this stock because it offers <Highlight color="#3FB950">{winReason}</Highlight>
          </RationaleText>
      </WinnerCard>

      <TableContainer>
        <StyledTable>
          <thead>
            <tr>
              <Th onClick={() => requestSort('symbol')}>Symbol</Th>
              <Th onClick={() => requestSort('marketCap')}>Market Cap</Th>
              <Th onClick={() => requestSort('peRatioTTM')}>P/E Ratio</Th>
              <Th onClick={() => requestSort('revenueGrowth')}>Momentum</Th>
              <Th onClick={() => requestSort('smartScore')}>Smart Score</Th>
            </tr>
          </thead>
          <tbody>
            {sortedAndScored.map(peer => (
              <Tr key={peer.symbol} $isMain={peer.symbol === symbol}>
                <Td>{peer.symbol}</Td>
                <Td>{formatMarketCap(peer.marketCap)}</Td>
                <Td>{formatNumber(peer.peRatioTTM)}</Td>
                <Td style={{color: peer.revenueGrowth > 0 ? '#3FB950' : peer.revenueGrowth < 0 ? '#F85149' : '#C9D1D9'}}>
                    {formatPercent(peer.revenueGrowth)}
                </Td>
                <Td>
                    <ScoreBarContainer>
                        <ScoreBarFill pct={peer.smartScore} color={getScoreColor(peer.smartScore)} />
                    </ScoreBarContainer>
                    <span style={{color: getScoreColor(peer.smartScore), fontWeight: '700'}}>
                        {peer.smartScore.toFixed(0)}
                    </span>
                </Td>
              </Tr>
            ))}
          </tbody>
        </StyledTable>
      </TableContainer>

    </Card>
  );
};

export default PeersComparison;
