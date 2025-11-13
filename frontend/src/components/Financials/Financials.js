import React from 'react';
import styled from 'styled-components';

// --- Import all our components ---
import Card from '../common/Card';
import RevenueChart from './RevenueChart';
import KeyStats from './KeyStats';
import AboutCompany from './AboutCompany';
import BalanceSheet from './BalanceSheet';
// --- NEW: Import our new Financial Statements viewer ---
import FinancialStatements from './FinancialStatements';

// --- Styled Components ---

const FinancialsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem; /* Adds space between each section */
`;

// --- The Final, Upgraded React Component ---

const Financials = ({
  profile,
  keyStats,
  financialData,
  balanceSheetData,
  // --- NEW: Accepting all the new data props ---
  annualCashFlow,
  quarterlyIncome,
  quarterlyBalance,
  quarterlyCashFlow
}) => {
  // Defensive check: If we don't have the core profile data, show a generic message.
  if (!profile) {
    return (
      <Card>
        <p>Financial data is not available for this stock.</p>
      </Card>
    );
  }

  return (
    <Card>
      <FinancialsContainer>

        {/* --- Section 1: Key Stats (Unchanged) --- */}
        <KeyStats stats={keyStats} />
        
        {/* --- Section 2: Balance Sheet Charts (Unchanged) --- */}
        <BalanceSheet balanceSheetData={balanceSheetData} />

        {/* --- Section 3: Income Statement Chart (Unchanged) --- */}
        <div>
            <h3 style={{ fontSize: '1.5rem', fontWeight: 600, marginBottom: '1.5rem' }}>Income Statement (5-Year Trend)</h3>
            <RevenueChart data={financialData} />
        </div>

        {/* --- Section 4: Detailed Financial Statements Viewer (NEW!) --- */}
        {/* We add our new component here, passing all the necessary annual and quarterly data down to it. */}
        <FinancialStatements
          currency={profile.currency}
          annualIncome={financialData}
          annualBalance={balanceSheetData}
          annualCashFlow={annualCashFlow}
          quarterlyIncome={quarterlyIncome}
          quarterlyBalance={quarterlyBalance}
          quarterlyCashFlow={quarterlyCashFlow}
        />

        {/* --- Section 5: About the Company (Unchanged) --- */}
        <AboutCompany profile={profile} />

      </FinancialsContainer>
    </Card>
  );
};

export default Financials;