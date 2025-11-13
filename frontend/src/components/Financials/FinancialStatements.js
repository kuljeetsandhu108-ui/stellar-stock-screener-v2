import React, { useState } from 'react';
import styled from 'styled-components';
import StatementTable from './StatementTable'; // We will create this next

// --- Styled Components ---

const SectionContainer = styled.div`
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid var(--color-border);
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-text-primary);
`;

const ToggleContainer = styled.div`
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1.5rem;
`;

const ToggleButton = styled.button`
  padding: 0.5rem 1rem;
  border: 1px solid var(--color-border);
  background-color: ${({ active }) => (active ? 'var(--color-primary)' : 'var(--color-secondary)')};
  color: ${({ active }) => (active ? 'var(--color-background)' : 'var(--color-text-primary)')};
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;

  &:first-child {
    border-radius: 6px 0 0 6px;
  }
  &:last-child {
    border-radius: 0 6px 6px 0;
  }
  &:hover {
    background-color: var(--color-primary);
    color: var(--color-background);
  }
`;

const StatementsGrid = styled.div`
  display: flex;
  flex-direction: column;
  gap: 3rem;
`;

// --- The Main React Component ---

const FinancialStatements = ({
  currency,
  annualIncome, annualBalance, annualCashFlow,
  quarterlyIncome, quarterlyBalance, quarterlyCashFlow
}) => {
  const [period, setPeriod] = useState('annual'); // Default to 'annual'

  const isAnnual = period === 'annual';

  return (
    <SectionContainer>
      <SectionTitle>Financial Statements</SectionTitle>
      
      <ToggleContainer>
        <ToggleButton active={isAnnual} onClick={() => setPeriod('annual')}>
          Annual
        </ToggleButton>
        <ToggleButton active={!isAnnual} onClick={() => setPeriod('quarterly')}>
          Quarterly
        </ToggleButton>
      </ToggleContainer>

      <StatementsGrid>
        {/* We pass the correctly selected data and currency to our table component */}
        <StatementTable
          title="Income Statement"
          data={isAnnual ? annualIncome : quarterlyIncome}
          currency={currency}
        />
        <StatementTable
          title="Balance Sheet"
          data={isAnnual ? annualBalance : quarterlyBalance}
          currency={currency}
        />
        <StatementTable
          title="Cash Flow Statement"
          data={isAnnual ? annualCashFlow : quarterlyCashFlow}
          currency={currency}
        />
      </StatementsGrid>
    </SectionContainer>
  );
};

export default FinancialStatements;