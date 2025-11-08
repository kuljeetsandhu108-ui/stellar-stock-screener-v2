import React from 'react';
import styled from 'styled-components';

// --- Styled Components ---

const TableContainer = styled.div`
  width: 100%;
  overflow-x: auto; /* Allows horizontal scrolling on small screens if needed */
`;

const StyledTable = styled.table`
  width: 100%;
  border-collapse: collapse;
  text-align: center;
`;

const TableHeader = styled.th`
  padding: 12px;
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: 0.9rem;
  border-bottom: 1px solid var(--color-border);
`;

const TableCell = styled.td`
  padding: 12px;
  font-size: 0.95rem;
  border-bottom: 1px solid var(--color-border);

  /* Style the 'Type' column differently */
  &:first-child {
    font-weight: 600;
    color: var(--color-text-primary);
    text-align: left;
  }
`;

const TableRow = styled.tr`
  /* A subtle hover effect for better user experience */
  &:hover {
    background-color: rgba(48, 54, 61, 0.5);
  }
`;

// --- React Component ---

const PivotLevels = () => {
  // Placeholder data to match the structure from the snapshot
  const pivotData = [
    { type: 'Classic', r1: 60.92, r2: 62.23, r3: 62.96, pp: 60.19, s1: 58.88, s2: 58.15, s3: 56.84 },
    { type: 'Fibonacci', r1: 60.97, r2: 61.45, r3: 62.23, pp: 60.19, s1: 59.41, s2: 58.93, s3: 58.15 },
    { type: 'Camarilla', r1: 59.80, r2: 59.98, r3: 60.17, pp: 60.19, s1: 59.42, s2: 59.24, s3: 59.05 },
  ];

  return (
    <TableContainer>
      <StyledTable>
        <thead>
          <tr>
            <TableHeader>Type</TableHeader>
            <TableHeader>R3</TableHeader>
            <TableHeader>R2</TableHeader>
            <TableHeader>R1</TableHeader>
            <TableHeader>PP</TableHeader>
            <TableHeader>S1</TableHeader>
            <TableHeader>S2</TableHeader>
            <TableHeader>S3</TableHeader>
          </tr>
        </thead>
        <tbody>
          {pivotData.map((row) => (
            <TableRow key={row.type}>
              <TableCell>{row.type}</TableCell>
              <TableCell>{row.r3.toFixed(2)}</TableCell>
              <TableCell>{row.r2.toFixed(2)}</TableCell>
              <TableCell>{row.r1.toFixed(2)}</TableCell>
              <TableCell>{row.pp.toFixed(2)}</TableCell>
              <TableCell>{row.s1.toFixed(2)}</TableCell>
              <TableCell>{row.s2.toFixed(2)}</TableCell>
              <TableCell>{row.s3.toFixed(2)}</TableCell>
            </TableRow>
          ))}
        </tbody>
      </StyledTable>
    </TableContainer>
  );
};

export default PivotLevels;