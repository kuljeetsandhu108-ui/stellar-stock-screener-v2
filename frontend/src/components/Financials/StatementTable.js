import React from 'react';
import styled from 'styled-components';

// --- Styled Components ---

const TableWrapper = styled.div`
  width: 100%;
  overflow-x: auto; /* The key to making the table horizontally scrollable */
`;

const StyledTable = styled.table`
  width: 100%;
  min-width: 800px; /* Ensures there's enough space for columns before scrolling */
  border-collapse: collapse;
  text-align: right;
`;

const TableHeader = styled.th`
  padding: 0.75rem 1rem;
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: 0.9rem;
  border-bottom: 1px solid var(--color-border);
  white-space: nowrap;

  &:first-child {
    text-align: left;
    position: sticky; /* Makes the first column "stick" to the left on scroll */
    left: 0;
    background-color: var(--color-secondary);
    z-index: 1;
  }
`;

const TableRow = styled.tr`
  &:nth-child(even) {
    background-color: rgba(0, 0, 0, 0.2);
  }
`;

const TableCell = styled.td`
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  font-family: 'Roboto Mono', monospace;
  white-space: nowrap;

  &:first-child {
    font-weight: 600;
    color: var(--color-text-primary);
    text-align: left;
    font-family: 'Inter', sans-serif;
    position: sticky;
    left: 0;
    background-color: var(--color-secondary);
    z-index: 1;
  }
`;

const Subtitle = styled.h4`
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--color-text-primary);
`;

// --- Helper Functions ---

const getCurrencySymbol = (currencyCode) => {
    switch (currencyCode) {
        case 'INR': return '₹';
        case 'USD': return '$';
        case 'JPY': return '¥';
        default: return ''; // No symbol if currency is unknown
    }
};

const formatNumber = (num, currencySymbol) => {
    if (num === null || num === undefined || isNaN(num)) return 'N/A';
    // Format large numbers into Millions for readability, prepended with currency
    const value = Math.abs(num);
    const sign = num < 0 ? '-' : '';
    if (value >= 1e6) {
        return `${sign}${currencySymbol}${(value / 1e6).toFixed(2)}M`;
    }
    // For smaller numbers, just add commas
    return `${sign}${currencySymbol}${num.toLocaleString()}`;
};

// --- The Reusable React Component ---

const StatementTable = ({ title, data, currency }) => {
  if (!data || !Array.isArray(data) || data.length === 0) {
    return null; // Don't render if there's no data
  }

  // --- Intelligent Data Key Discovery ---
  // This is the "brain". It finds all the numerical data points available
  // in the first record, excluding known non-financial keys.
  const headers = data.map(item => item.calendarYear || item.date.substring(0, 4));
  const ignoredKeys = new Set(['date', 'symbol', 'reportedCurrency', 'cik', 'fillingDate', 'acceptedDate', 'calendarYear', 'period', 'link', 'finalLink']);
  const dataKeys = Object.keys(data[0]).filter(key => 
      !ignoredKeys.has(key) && typeof data[0][key] === 'number'
  );

  const currencySymbol = getCurrencySymbol(currency);

  return (
    <div>
      <Subtitle>{title}</Subtitle>
      <TableWrapper>
        <StyledTable>
          <thead>
            <tr>
              <TableHeader>Line Item</TableHeader>
              {headers.map((header, index) => (
                <TableHeader key={index}>{header}</TableHeader>
              ))}
            </tr>
          </thead>
          <tbody>
            {dataKeys.map(key => (
              <TableRow key={key}>
                {/* Format the key name to be more readable (e.g., "netIncome" -> "Net Income") */}
                <TableCell>{key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}</TableCell>
                {data.map((row, index) => (
                  <TableCell key={index}>{formatNumber(row[key], currencySymbol)}</TableCell>
                ))}
              </TableRow>
            ))}
          </tbody>
        </StyledTable>
      </TableWrapper>
    </div>
  );
};

export default StatementTable;