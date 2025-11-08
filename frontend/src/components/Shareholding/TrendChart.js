import React from 'react';
import styled from 'styled-components';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Cell
} from 'recharts';

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

// --- React Component ---

const TrendChart = () => {
  // --- Placeholder Data ---
  // The free API does not provide this historical data,
  // so we are using a realistic placeholder structure to build the UI.
  const placeholderData = [
    { name: 'Jun 2024', Holding: 13.27, Pledges: 0 },
    { name: 'Sep 2024', Holding: 13.25, Pledges: 0 },
    { name: 'Dec 2024', Holding: 13.25, Pledges: 0 },
    { name: 'Jun 2025', Holding: 11.74, Pledges: 0 },
    { name: 'Sep 2025', Holding: 11.73, Pledges: 0 },
  ];

  // Custom Tooltip for better styling
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div style={{
            backgroundColor: 'var(--color-secondary)',
            border: '1px solid var(--color-border)',
            padding: '10px',
            borderRadius: '5px'
        }}>
          <p>{label}</p>
          <p style={{ color: '#8884d8' }}>{`Holding: ${payload[0].value}%`}</p>
          <p style={{ color: '#82ca9d' }}>{`Pledged: ${payload[1] ? payload[1].value : '0'}%`}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <ChartWrapper>
      <ChartTitle>Promoter Holding Trend (%)</ChartTitle>
      <ResponsiveContainer>
        <BarChart
          data={placeholderData}
          margin={{ top: 5, right: 20, left: 0, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" vertical={false} />
          <XAxis 
            dataKey="name" 
            stroke="var(--color-text-secondary)" 
            tick={{ fill: 'var(--color-text-secondary)', fontSize: 12 }} 
          />
          <YAxis 
            stroke="var(--color-text-secondary)" 
            domain={[0, 15]} // Set a fixed domain for better visual consistency
            tick={{ fill: 'var(--color-text-secondary)', fontSize: 12 }} 
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(136, 132, 216, 0.1)' }} />
          
          {/* Bar for Promoter Holding */}
          <Bar dataKey="Holding" fill="#586994" barSize={30}>
            {placeholderData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.Holding < 12 ? '#FE6D73' : '#586994'} />
            ))}
          </Bar>
          
          {/* Bar for Pledged shares. It will stack on top of the Holding bar.
              Since our pledges are 0, it won't be visible, which is correct. */}
          <Bar dataKey="Pledges" stackId="a" fill="#3FB950" />
        </BarChart>
      </ResponsiveContainer>
    </ChartWrapper>
  );
};

export default TrendChart;