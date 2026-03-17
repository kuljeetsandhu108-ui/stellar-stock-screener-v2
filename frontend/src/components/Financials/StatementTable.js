import React from 'react';
import styled from 'styled-components';

// --- Styled Components ---
const TableWrapper = styled.div`
  width: 100%;
  overflow-x: auto;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background);
  
  /* Scrollbar styling for smooth UX */
  &::-webkit-scrollbar { height: 6px; }
  &::-webkit-scrollbar-thumb { background: #30363D; border-radius: 3px; }
`;

const StyledTable = styled.table`
  width: 100%;
  min-width: 800px;
  border-collapse: collapse;
  text-align: right;
`;

const TableHeader = styled.th`
  padding: 1rem;
  color: var(--color-text-secondary);
  font-weight: 600;
  font-size: 0.85rem;
  border-bottom: 1px solid var(--color-border);
  white-space: nowrap;
  background-color: rgba(255, 255, 255, 0.02);

  &:first-child {
    text-align: left;
    position: sticky;
    left: 0;
    background-color: #161B22; 
    z-index: 1;
    border-right: 1px solid var(--color-border);
  }
`;

const TableRow = styled.tr`
  &:nth-child(even) { background-color: rgba(255, 255, 255, 0.02); }
  &:hover { background-color: rgba(88, 166, 255, 0.05); }
`;

const TableCell = styled.td`
  padding: 1rem;
  font-size: 0.95rem;
  font-family: 'Roboto Mono', monospace;
  white-space: nowrap;
  color: #C9D1D9;
  border-bottom: 1px solid rgba(255,255,255,0.05);

  &:first-child {
    font-weight: 600;
    color: var(--color-primary);
    text-align: left;
    font-family: 'Inter', sans-serif;
    position: sticky;
    left: 0;
    background-color: #161B22;
    z-index: 1;
    border-right: 1px solid var(--color-border);
  }
`;

const Subtitle = styled.h4`
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--color-text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
    
    &::before {
        content: '';
        display: inline-block;
        width: 4px;
        height: 16px;
        background-color: var(--color-primary);
        border-radius: 2px;
    }
`;

// --- Helper Functions ---
const getCurrencySymbol = (currencyCode) => {
    switch (currencyCode) {
        case 'INR': return '\u20B9';
        case 'USD': return '$';
        case 'JPY': return '\u00A5';
        case 'EUR': return '\u20AC';
        case 'GBP': return '\u00A3';
        default: return ''; 
    }
};

const formatNumber = (num, currencySymbol) => {
    if (num === null || num === undefined || isNaN(num)) return '--';
    
    const value = Math.abs(num);
    const sign = num < 0 ? '-' : '';
    if (value >= 1e6) {
        return `${sign}${currencySymbol}${(value / 1e6).toFixed(2)}M`;
    }
    return `${sign}${currencySymbol}${num.toLocaleString()}`;
};

// --- The Component ---
const StatementTable = ({ title, data, currency }) => {
  if (!data || !Array.isArray(data) || data.length === 0) return null;

  const headers = data.map(item => item.calendarYear || item.date.substring(0, 4));
  const ignoredKeys = new Set(['date', 'symbol', 'reportedCurrency', 'cik', 'fillingDate', 'acceptedDate', 'calendarYear', 'period', 'link', 'finalLink']);
  
  // 1. DYNAMIC KEY DETECTION: Only grab keys that actually have numbers (ignoring missing data)
  const dataKeysSet = new Set();
  data.forEach(row => {
      Object.keys(row).forEach(key => {
          if (!ignoredKeys.has(key) && typeof row[key] === 'number') {
              dataKeysSet.add(key);
          }
      });
  });

  // 2. PRIORITY SORTING: Keep the table extremely clean and logical
  const priority =[
      // Income Statement Priority
      'revenue', 'costOfRevenue', 'grossProfit', 'ebitda', 'operatingIncome', 'interestExpense', 'netIncome',
      // Balance Sheet Priority
      'totalAssets', 'totalCurrentAssets', 'cashAndEquivalents', 'totalLiabilities', 'totalCurrentLiabilities', 'longTermDebt', 'netDebt', 'totalStockholdersEquity', 'sharesOutstanding',
      // Cash Flow Priority
      'operatingCashFlow', 'investingCashFlow', 'financingCashFlow', 'capitalExpenditure', 'freeCashFlow', 'dividendsPaid'
  ];

  const dataKeys = Array.from(dataKeysSet).sort((a, b) => {
      let idxA = priority.indexOf(a);
      let idxB = priority.indexOf(b);
      if (idxA === -1) idxA = 999;
      if (idxB === -1) idxB = 999;
      return idxA - idxB;
  });

  const currencySymbol = getCurrencySymbol(currency);

  return (
    <div style={{ marginBottom: '3rem' }}>
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
                <TableCell>{key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}</TableCell>
                {data.map((row, index) => (
                  <TableCell key={`${key}-${index}`}>{formatNumber(row[key], currencySymbol)}</TableCell>
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

