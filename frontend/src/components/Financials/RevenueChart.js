import React from 'react';
import styled from 'styled-components';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  CartesianGrid
} from 'recharts';

// --- Styled Components ---

const ChartContainer = styled.div`
  width: 100%;
  height: 400px; /* Give the chart a fixed height */
`;

// Custom Tooltip for a better look and feel
const CustomTooltipContainer = styled.div`
  background-color: #2a3441;
  border: 1px solid var(--color-border);
  padding: 1rem;
  border-radius: 8px;
  color: var(--color-text-primary);
`;

const TooltipLabel = styled.p`
  margin-bottom: 0.5rem;
  font-weight: bold;
`;

// --- Helper Functions ---

// Formats large numbers into Billions (B) or Millions (M) for the Y-axis
const formatYAxis = (tick) => {
  if (Math.abs(tick) >= 1e9) {
    return `${(tick / 1e9).toFixed(1)}B`;
  }
  if (Math.abs(tick) >= 1e6) {
    return `${(tick / 1e6).toFixed(1)}M`;
  }
  return tick;
};

// Formats large numbers with commas and adds a currency symbol
const formatCurrency = (value) => {
    return `$${new Intl.NumberFormat('en-US').format(value)}`;
};


// --- React Component ---

const RevenueChart = ({ data }) => {
  // The API sends data from newest to oldest, so we reverse it for the chart
  // and process it into a more usable format.
  const chartData = data.slice().reverse().map(item => ({
    year: new Date(item.date).getFullYear(),
    Revenue: item.revenue,
    'Net Profit': item.netIncome,
  }));

  // Custom Tooltip Component
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <CustomTooltipContainer>
          <TooltipLabel>{`Year: ${label}`}</TooltipLabel>
          <p style={{ color: '#8884d8' }}>{`Revenue: ${formatCurrency(payload[0].value)}`}</p>
          <p style={{ color: '#82ca9d' }}>{`Net Profit: ${formatCurrency(payload[1].value)}`}</p>
        </CustomTooltipContainer>
      );
    }
    return null;
  };

  return (
    <ChartContainer>
      {/* ResponsiveContainer makes the chart adapt to its parent's size */}
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={chartData}
          margin={{ top: 5, right: 20, left: 30, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke={ "var(--color-border)" } />
          <XAxis 
            dataKey="year" 
            stroke={ "var(--color-text-secondary)" }
            tick={{ fill: 'var(--color-text-secondary)', fontSize: 12 }} 
          />
          <YAxis 
            stroke={ "var(--color-text-secondary)" }
            tickFormatter={formatYAxis}
            tick={{ fill: 'var(--color-text-secondary)', fontSize: 12 }}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(136, 132, 216, 0.1)' }}/>
          <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '20px' }} />
          <Bar dataKey="Revenue" fill="#8884d8" />
          <Bar dataKey="Net Profit" fill="#82ca9d" />
        </BarChart>
      </ResponsiveContainer>
    </ChartContainer>
  );
};

export default RevenueChart;