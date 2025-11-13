import React from 'react';
import styled from 'styled-components';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Label
} from 'recharts';

// --- Styled Components ---

const PriceTargetContainer = styled.div`
  width: 100%;
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--color-text-primary);
`;

const PriceDisplay = styled.div`
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
`;

const PriceChange = styled.div`
  font-size: 1rem;
  font-weight: 500;
  color: ${({ isPositive }) => (isPositive ? 'var(--color-success)' : 'var(--color-danger)')};
  margin-bottom: 1rem;
`;

const SummaryText = styled.p`
  color: var(--color-text-secondary);
  line-height: 1.6;
  max-width: 400px;
  margin-bottom: 2rem;
`;

const ChartWrapper = styled.div`
  height: 400px;
  width: 100%;
`;

// --- NEW: The same intelligent currency helper function from our StockHeader ---
const getCurrencySymbol = (currencyCode) => {
    switch (currencyCode) {
        case 'INR':
            return '₹';
        case 'USD':
            return '$';
        case 'JPY':
            return '¥';
        // We can add more currencies like EUR, GBP etc. as needed in the future
        default:
            return '$'; // Default to dollar if the currency code is unknown or missing
    }
};

// --- The Upgraded, Currency-Aware React Component ---

// The component now accepts the 'currency' prop from its parent.
const PriceTarget = ({ consensus, quote, currency }) => {

  // Defensive check: If essential data is missing, we show an informative message.
  if (!consensus || !quote || !consensus.targetConsensus) {
    return (
      <PriceTargetContainer>
        <SectionTitle>Price Target</SectionTitle>
        <p>Price target data is not available for this stock.</p>
      </PriceTargetContainer>
    );
  }
  
  // --- Get the correct currency symbol based on the data received ---
  const currencySymbol = getCurrencySymbol(currency);

  const { targetHigh, targetLow, targetConsensus } = consensus;
  const currentPrice = quote.price;

  const change = targetConsensus - currentPrice;
  const changePercent = (change / currentPrice) * 100;
  const isPositive = change >= 0;

  // Data for the simple line chart visualization
  const chartData = [
    { name: 'Current', value: currentPrice },
    { name: '1Y Forecast', value: targetConsensus },
  ];
  
  // A custom tooltip for better styling that also includes the currency symbol
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div style={{
          backgroundColor: 'var(--color-secondary)',
          border: '1px solid var(--color-border)',
          padding: '1rem',
          borderRadius: '8px'
        }}>
          <p>{`${label}: ${currencySymbol}${payload[0].value.toFixed(2)}`}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <PriceTargetContainer>
      <SectionTitle>Price Target</SectionTitle>
      
      {/* --- All displayed values now use the dynamic currency symbol --- */}
      <PriceDisplay>{currencySymbol}{targetConsensus?.toFixed(2)}</PriceDisplay>
      <PriceChange isPositive={isPositive}>
          {isPositive ? '+' : ''}{currencySymbol}{change.toFixed(2)} ({isPositive ? '+' : ''}{changePercent.toFixed(2)}%)
      </PriceChange>
      <SummaryText>
        The analysts offering 1-year price forecasts have a max estimate of {currencySymbol}{targetHigh?.toFixed(2)} and a min estimate of {currencySymbol}{targetLow?.toFixed(2)}.
      </SummaryText>

      <ChartWrapper>
        <ResponsiveContainer>
          <LineChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
            <XAxis dataKey="name" stroke="var(--color-text-secondary)" tick={{ fill: 'var(--color-text-secondary)' }} />
            <YAxis 
                stroke="var(--color-text-secondary)" 
                domain={['dataMin - 20', 'dataMax + 20']}
                tick={{ fill: 'var(--color-text-secondary)' }}
                tickFormatter={(tick) => `${currencySymbol}${tick}`} // Add currency to the axis
            />
            <Tooltip content={<CustomTooltip />} />
            
            <Line type="monotone" dataKey="value" stroke="var(--color-primary)" strokeWidth={2} dot={{ r: 4 }} />

            {/* Reference lines now also include the dynamic currency symbol */}
            <ReferenceLine y={targetHigh} stroke="var(--color-success)" strokeDasharray="3 3">
                <Label value={`Max: ${currencySymbol}${targetHigh.toFixed(2)}`} position="right" fill="var(--color-success)" />
            </ReferenceLine>
            <ReferenceLine y={targetLow} stroke="var(--color-danger)" strokeDasharray="3 3">
                <Label value={`Min: ${currencySymbol}${targetLow.toFixed(2)}`} position="right" fill="var(--color-danger)" />
            </ReferenceLine>
            <ReferenceLine y={targetConsensus} stroke="var(--color-primary)" strokeDasharray="3 3">
                <Label value={`Avg: ${currencySymbol}${targetConsensus.toFixed(2)}`} position="right" fill="var(--color-primary)" />
            </ReferenceLine>
            <ReferenceLine y={currentPrice} stroke="#fff" strokeDasharray="1 1">
                <Label value={`Current: ${currencySymbol}${currentPrice.toFixed(2)}`} position="left" fill="#fff" />
            </ReferenceLine>
            
          </LineChart>
        </ResponsiveContainer>
      </ChartWrapper>
    </PriceTargetContainer>
  );
};

export default PriceTarget;