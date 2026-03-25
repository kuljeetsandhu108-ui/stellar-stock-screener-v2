import React from 'react';
import styled from 'styled-components';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from 'recharts';
import { FaUsers } from 'react-icons/fa';

// --- Styled Components ---
const ChartWrapper = styled.div`
  width: 100%;
  height: 350px;
`;

const ChartTitle = styled.h3`
  text-align: center;
  color: var(--color-text-secondary);
  font-weight: 500;
  margin-bottom: 2rem;
`;

const PlaceholderContainer = styled.div`
  width: 100%;
  height: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  border: 1px dashed var(--color-border);
  padding: 2rem;
  text-align: center;
`;

// --- React Component ---
const TrendChart = ({ data }) => {
  // Safety check: Filter out empty or aggregated responses
  const hasData = data && Array.isArray(data) && data.length > 0 && data[0].holder !== "Data Aggregated";

  if (!hasData) {
     return (
        <PlaceholderContainer>
            <FaUsers size={40} style={{ color: 'var(--color-text-secondary)', opacity: 0.5, marginBottom: '1rem' }} />
            <h4 style={{ color: 'var(--color-text-primary)', marginBottom: '0.5rem' }}>Holders Data Unavailable</h4>
            <p style={{ color: 'var(--color-text-secondary)', fontSize: '0.9rem', fontStyle: 'italic' }}>
                Detailed institutional holder breakdowns are currently unavailable for this specific asset.
            </p>
        </PlaceholderContainer>
     );
  }

  // We only want the top 5 holders for a clean UI
  const chartData = data.slice(0, 5).map(item => ({
      name: item.holder.length > 18 ? item.holder.substring(0, 18) + '...' : item.holder,
      fullName: item.holder,
      Shares: item.shares
  }));

  // Determine if the backend passed us Percentages (synthetic) or raw Share counts
  const isPercentage = chartData.length > 0 && chartData[0].Shares <= 100;

  const formatXAxis = (tick) => {
      if (isPercentage) return `${tick.toFixed(0)}%`;
      if (tick >= 1e9) return `${(tick / 1e9).toFixed(1)}B`;
      if (tick >= 1e6) return `${(tick / 1e6).toFixed(1)}M`;
      return tick.toLocaleString();
  };

  const CustomTooltip = ({ active, payload }) => {
      if (active && payload && payload.length) {
          const val = payload[0].value;
          const displayVal = isPercentage ? `${val.toFixed(2)}%` : val.toLocaleString();
          return (
              <div style={{ backgroundColor: '#1C2128', border: '1px solid var(--color-border)', padding: '10px', borderRadius: '8px', zIndex: 100 }}>
                  <p style={{ color: '#C9D1D9', fontWeight: 600, marginBottom: '5px' }}>{payload[0].payload.fullName}</p>
                  <p style={{ color: '#58A6FF' }}>Holding: {displayVal}</p>
              </div>
          );
      }
      return null;
  };

  return (
    <ChartWrapper>
      <ChartTitle>Major Shareholders</ChartTitle>
      <ResponsiveContainer width="100%" height="100%">
        {/* Horizontal Bar Chart is better for long names */}
        <BarChart 
            layout="vertical" 
            data={chartData} 
            margin={{ top: 5, right: 20, left: 60, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" horizontal={true} vertical={false} />
          <XAxis type="number" stroke="var(--color-text-secondary)" tickFormatter={formatXAxis} tick={{ fontSize: 11 }} />
          <YAxis type="category" dataKey="name" stroke="var(--color-text-secondary)" tick={{ fontSize: 10 }} width={80} />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(136, 132, 216, 0.05)' }} />
          
          <Bar dataKey="Shares" fill="#58A6FF" radius={[0, 4, 4, 0]} barSize={25}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={index === 0 ? '#58A6FF' : '#30363D'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </ChartWrapper>
  );
};

export default TrendChart;
