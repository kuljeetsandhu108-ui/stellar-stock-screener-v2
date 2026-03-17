import React from 'react';
import styled from 'styled-components';

const StatsContainer = styled.div`
  padding-bottom: 2rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--color-border);
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-text-primary);
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem 1rem;

  @media (max-width: 992px) {
    grid-template-columns: repeat(2, 1fr);
  }
`;

const StatItem = styled.div`
  display: flex;
  flex-direction: column;
`;

const StatLabel = styled.span`
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  margin-bottom: 0.25rem;
`;

const StatValue = styled.span`
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-text-primary);
`;

const formatMarketCap = (num) => {
  if (num === null || num === undefined) return '--';
  if (num >= 1e12) return `$${(num / 1e12).toFixed(2)} T`;
  if (num >= 1e9) return `$${(num / 1e9).toFixed(2)} B`;
  if (num >= 1e6) return `$${(num / 1e6).toFixed(2)} M`;
  return `$${num}`;
};

const formatNumber = (num) => {
  if (num === null || num === undefined) return '--';
  return num.toFixed(2);
};

const KeyStats = ({ stats }) => {
  if (!stats) return null;

  return (
    <StatsContainer>
      <SectionTitle>Key Stats</SectionTitle>
      <StatsGrid>
        <StatItem>
          <StatLabel>Market Capitalization</StatLabel>
          <StatValue>{formatMarketCap(stats.marketCap)}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Dividend Yield (TTM)</StatLabel>
          <StatValue>{stats.dividendYield ? `${(stats.dividendYield * 100).toFixed(2)}%` : '--'}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Price to Earnings (TTM)</StatLabel>
          <StatValue>{formatNumber(stats.peRatio)}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Basic EPS (TTM)</StatLabel>
          <StatValue>{formatNumber(stats.basicEPS)}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Net Income / Share</StatLabel>
          <StatValue>{formatNumber(stats.netIncome)}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Revenue / Share</StatLabel>
          <StatValue>{formatNumber(stats.revenue)}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Shares Float</StatLabel>
          <StatValue>{formatMarketCap(stats.sharesFloat)}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Beta (1Y)</StatLabel>
          <StatValue>{formatNumber(stats.beta)}</StatValue>
        </StatItem>
      </StatsGrid>
    </StatsContainer>
  );
};

export default KeyStats;
