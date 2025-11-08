import React from 'react';
import styled from 'styled-components';

// --- Styled Components ---

const TableContainer = styled.div`
  width: 100%;
  max-width: 300px; /* Constrain width for a compact look */
  margin-left: auto; /* Push the table to the right */
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

  /* Style the value cell */
  &:last-child {
    font-weight: 600;
    color: var(--color-text-primary);
    text-align: right;
  }
`;

const TableRow = styled.tr`
  border-bottom: 1px solid var(--color-border);

  &:last-child {
    border-bottom: none; /* Remove the border for the last row */
  }
`;

// --- React Component ---

const MovingAverages = () => {
  // Placeholder data to match the snapshot
  const maData = [
    { period: '5 Days', value: 59.10 },
    { period: '10 Days', value: 57.60 },
    { period: '20 Days', value: 55.69 },
    { period: '50 Days', value: 56.48 },
    { period: '100 Days', value: 60.19 },
    { period: '200 Days', value: 58.72 },
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
          {maData.map((row) => (
            <TableRow key={row.period}>
              <TableCell>{row.period}</TableCell>
              <TableCell>{row.value.toFixed(2)}</TableCell>
            </TableRow>
          ))}
        </tbody>
      </StyledTable>
    </TableContainer>
  );
};

export default MovingAverages;