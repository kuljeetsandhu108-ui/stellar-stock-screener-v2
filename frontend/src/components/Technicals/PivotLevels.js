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
  white-space: nowrap; /* Prevents headers from wrapping */
`;

const TableCell = styled.td`
  padding: 12px;
  font-size: 0.95rem;
  font-family: 'Roboto Mono', monospace; /* Use a monospaced font for numbers */
  border-bottom: 1px solid var(--color-border);

  /* Style the 'Type' column differently */
  &:first-child {
    font-weight: 600;
    color: var(--color-text-primary);
    text-align: left;
    font-family: 'Inter', sans-serif;
  }
`;

const TableRow = styled.tr`
  /* A subtle hover effect for better user experience */
  &:hover {
    background-color: rgba(48, 54, 61, 0.5);
  }

  /* Remove bottom border for the very last row */
  &:last-child > td {
      border-bottom: none;
  }
`;

// --- The New, Dynamic React Component ---

// The component now accepts 'pivotData' as a prop from its parent.
const PivotLevels = ({ pivotData }) => {
  // If the data is missing or empty, we show an informative message.
  if (!pivotData || Object.keys(pivotData).length === 0) {
    return (
      <TableContainer>
        <p>Pivot point data is not available.</p>
      </TableContainer>
    );
  }

  // We dynamically create our rows from the keys in the 'pivotData' object
  // that our new backend provides (e.g., "classic", "fibonacci", "camarilla").
  const pivotRows = [
    { type: 'Classic', data: pivotData.classic },
    { type: 'Fibonacci', data: pivotData.fibonacci },
    { type: 'Camarilla', data: pivotData.camarilla },
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
            <TableHeader>Pivot Point (PP)</TableHeader>
            <TableHeader>S1</TableHeader>
            <TableHeader>S2</TableHeader>
            <TableHeader>S3</TableHeader>
          </tr>
        </thead>
        <tbody>
          {pivotRows.map(row => {
            const { type, data } = row;
            // A safety check: Don't render a row if its specific data is missing
            if (!data) return null;
            
            return (
              <TableRow key={type}>
                <TableCell>{type}</TableCell>
                {/* We use optional chaining (?.) and the nullish coalescing operator (??) 
                    for maximum safety. This prevents crashes if a value is null or undefined. */}
                <TableCell>{data.r3?.toFixed(2) ?? 'N/A'}</TableCell>
                <TableCell>{data.r2?.toFixed(2) ?? 'N/A'}</TableCell>
                <TableCell>{data.r1?.toFixed(2) ?? 'N/A'}</TableCell>
                <TableCell>{data.pp?.toFixed(2) ?? 'N/A'}</TableCell>
                <TableCell>{data.s1?.toFixed(2) ?? 'N/A'}</TableCell>
                <TableCell>{data.s2?.toFixed(2) ?? 'N/A'}</TableCell>
                <TableCell>{data.s3?.toFixed(2) ?? 'N/A'}</TableCell>
              </TableRow>
            );
          })}
        </tbody>
      </StyledTable>
    </TableContainer>
  );
};

export default PivotLevels;