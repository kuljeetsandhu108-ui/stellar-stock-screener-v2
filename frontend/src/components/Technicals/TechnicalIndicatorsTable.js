import React from 'react';
import styled, { keyframes } from 'styled-components';

// --- Styled Components & Animations ---

const fadeInRow = keyframes`
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const TableContainer = styled.div`
  width: 100%;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-border);
`;

const StyledTable = styled.table`
  width: 100%;
  border-collapse: collapse;
`;

const TableHeader = styled.th`
  padding: 12px;
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: 0.9rem;
  text-align: left;
  
  &:nth-child(2) {
    text-align: right;
  }
  &:last-child {
    text-align: right;
  }
`;

const TableRow = styled.tr`
  opacity: 0; /* Start hidden for animation */
  animation: ${fadeInRow} 0.5s ease-out forwards;
  /* Stagger the animation for each row for a beautiful effect */
  animation-delay: ${({ delay }) => delay * 0.05}s;
  
  &:not(:last-child) {
    border-bottom: 1px solid var(--color-border);
  }
`;

const TableCell = styled.td`
  padding: 14px 12px;
  font-size: 0.95rem;
  font-weight: 500;
  white-space: pre-wrap; /* Allows the multiline content for Bollinger Bands */

  &:first-child {
    font-weight: 600;
    color: var(--color-text-primary);
  }
  
  &:nth-child(2) {
    text-align: right;
    font-family: 'Roboto Mono', monospace;
  }

  &:last-child {
    text-align: right;
    font-weight: 700;
  }
`;

const Indication = styled.span`
  color: ${({ type }) => {
    switch (type) {
      case 'Bullish':
      case 'Oversold':
        return 'var(--color-success)';
      case 'Bearish':
      case 'Overbought':
        return 'var(--color-danger)';
      default:
        return 'var(--color-text-secondary)';
    }
  }};
`;

// --- The Corrected React Component ---

const TechnicalIndicatorsTable = ({ indicators }) => {
  if (!indicators || Object.keys(indicators).length === 0) {
    return (
      <TableContainer>
        <p>Technical indicator data is not available.</p>
      </TableContainer>
    );
  }

  // --- THIS IS THE CRITICAL FIX FOR BOLLINGER BANDS ---
  // We now safely access the nested 'bollingerBands' object, providing an empty object as a fallback.
  const bb = indicators.bollingerBands || {};

  const indicatorList = [
    { name: 'RSI(14)', level: indicators.rsi, indication: indicators.rsi < 30 ? 'Oversold' : indicators.rsi > 70 ? 'Overbought' : (indicators.rsi < 50 ? 'Bearish' : 'Bullish') },
    { name: 'MACD(12,26,9)', level: indicators.macd, indication: indicators.macd > indicators.macdsignal ? 'Bullish' : 'Bearish' },
    { name: 'Stochastic(14,3)', level: indicators.stochasticsk, indication: indicators.stochasticsk < 20 ? 'Oversold' : indicators.stochasticsk > 80 ? 'Overbought' : 'Neutral' },
    { name: 'ADX(14)', level: indicators.adx, indication: indicators.adx > 25 ? 'Strong Trend' : 'Weak Trend' },
    { name: 'Williams %R(14)', level: indicators.williamsr, indication: indicators.williamsr < -80 ? 'Oversold' : indicators.williamsr > -20 ? 'Overbought' : 'Neutral' },
    { name: 'ATR(14)', level: indicators.atr, indication: 'Volatility' },
    // We now correctly and safely access the properties from our 'bb' object.
    { name: 'Bollinger Band(20,2)', level: `UB: ${bb.upperBand?.toFixed(2) ?? 'N/A'}\nLB: ${bb.lowerBand?.toFixed(2) ?? 'N/A'}\nSMA: ${bb.middleBand?.toFixed(2) ?? 'N/A'}`, indication: '--' },
  ];
  
  return (
    <TableContainer>
      <StyledTable>
        <thead>
          <tr>
            <TableHeader>Indicator</TableHeader>
            <TableHeader>Level</TableHeader>
            <TableHeader>Indication</TableHeader>
          </tr>
        </thead>
        <tbody>
          {indicatorList.map((item, index) => (
            <TableRow key={item.name} delay={index}>
              <TableCell>{item.name}</TableCell>
              <TableCell>{typeof item.level === 'number' ? item.level.toFixed(2) : item.level}</TableCell>
              <TableCell>
                <Indication type={item.indication}>
                  {item.indication}
                </Indication>
              </TableCell>
            </TableRow>
          ))}
        </tbody>
      </StyledTable>
    </TableContainer>
  );
};

export default TechnicalIndicatorsTable;