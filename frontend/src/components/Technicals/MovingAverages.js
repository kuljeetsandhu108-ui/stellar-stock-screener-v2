import React from 'react';
import styled from 'styled-components';

// --- Styled Components ---

const TableContainer = styled.div`
  width: 100%;
  max-width: 300px; /* Constrain width for a compact, clean look */
  margin-left: auto; /* Push the table to the right within its grid container */
`;

const StyledTable = styled.table`
  width: 100%;
  border-collapse: collapse;
`;

const TableHeader = styled.th`
  padding: 10px;
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: 0.9rem;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
`;

const TableCell = styled.td`
  padding: 10px;
  font-size: 0.95rem;

  /* Style the period (e.g., "5 Days") cell */
  &:first-child {
    color: var(--color-text-secondary);
  }

  /* Style the calculated value cell */
  &:last-child {
    font-weight: 600;
    color: var(--color-text-primary);
    text-align: right;
    font-family: 'Roboto Mono', monospace; /* Use a monospaced font for numbers */
  }
`;

const TableRow = styled.tr`
  border-bottom: 1px solid var(--color-border);

  &:last-child {
    border-bottom: none; /* Remove the border for the last row */
  }
`;

// --- The New, Dynamic React Component ---

// The component now accepts 'maData' as a prop from its parent.
const MovingAverages = ({ maData }) => {
  // If the data is missing or empty, we show an informative message.
  if (!maData || Object.keys(maData).length === 0) {
    return (
      <TableContainer>
        <p>Moving average data is not available.</p>
      </TableContainer>
    );
  }

  // We create a structured array to ensure the rows are always in the correct order.
  const ma_periods = [
    { period: '5 Days', key: '5' },
    { period: '10 Days', key: '10' },
    { period: '20 Days', key: '20' },
    { period: '50 Days', key: '50' },
    { period: '100 Days', key: '100' },
    { period: '200 Days', key: '200' },
  ];

  return (
    <TableContainer>
      <StyledTable>
        <thead>
          <tr>
            <TableHeader>Period (SMA)</TableHeader>
            <TableHeader style={{ textAlign: 'right' }}>Value</TableHeader>
          </tr>
        </thead>
        <tbody>
          {ma_periods.map(item => {
            const value = maData[item.key];
            return (
              <TableRow key={item.period}>
                <TableCell>{item.period}</TableCell>
                {/* We check if the value is a valid number before displaying */}
                <TableCell>{typeof value === 'number' ? value.toFixed(2) : 'N/A'}</TableCell>
              </TableRow>
            );
          })}
        </tbody>
      </StyledTable>
    </TableContainer>
  );
};

export default MovingAverages;