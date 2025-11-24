import React from 'react';
import styled from 'styled-components';

// --- Styled Components ---

const HeaderContainer = styled.div`
  display: flex;
  flex-direction: column; /* Default to column for mobile */
  justify-content: space-between;
  align-items: flex-start; /* Align left on mobile */
  margin-bottom: 1.5rem;
  padding: 1.25rem;
  background-color: var(--color-secondary);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  gap: 1rem;
  width: 100%; /* Ensure it takes full width but respects padding */
  box-sizing: border-box;

  @media (min-width: 768px) {
    flex-direction: row; /* Row for desktop */
    align-items: center;
    gap: 0;
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
`;

const CompanyInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  max-width: 100%; /* Prevent overflow */
`;

const CompanyLogo = styled.img`
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: #fff;
  flex-shrink: 0; /* Prevent logo from getting squished */
  
  @media (min-width: 768px) {
      width: 60px;
      height: 60px;
  }
`;

const TextContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-width: 0; /* Critical for text truncation to work in flex items */
`;

const CompanyName = styled.h1`
  font-size: 1.25rem; /* Smaller, safer size for mobile */
  font-weight: 700;
  margin: 0;
  line-height: 1.3;
  
  /* Text Wrapping Logic */
  white-space: normal; 
  word-wrap: break-word;

  @media (min-width: 768px) {
    font-size: 2.5rem;
    white-space: nowrap; /* On desktop, we can keep it on one line */
  }
`;

const CompanySymbol = styled.span`
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  font-weight: 500;
  margin-top: 0.25rem;
  
  @media (min-width: 768px) {
      font-size: 1.2rem;
      margin-top: 0;
      margin-left: 0.75rem;
      display: inline-block; /* Sit next to name on desktop */
  }
`;

const PriceInfo = styled.div`
  text-align: left;
  width: 100%;
  
  @media (min-width: 768px) {
    text-align: right;
    width: auto;
  }
`;

const CurrentPrice = styled.div`
  font-size: 1.75rem; /* Readable but compact for mobile */
  font-weight: 700;
  margin-bottom: 0.25rem;

  @media (min-width: 768px) {
      font-size: 2.5rem;
  }
`;

const PriceChange = styled.div`
  font-size: 1rem;
  font-weight: 500;
  color: ${({ isPositive }) => (isPositive ? 'var(--color-success)' : 'var(--color-danger)')};
  
  @media (min-width: 768px) {
      font-size: 1.2rem;
  }
`;

// --- Helper Function ---
const getCurrencySymbol = (currencyCode) => {
    switch (currencyCode) {
        case 'INR': return '₹';
        case 'USD': return '$';
        case 'JPY': return '¥';
        case 'EUR': return '€';
        case 'GBP': return '£';
        default: return '$';
    }
};

// --- The React Component ---

const StockHeader = ({ profile, quote }) => {
  if (!profile || !quote) return null;
  const currencySymbol = getCurrencySymbol(profile.currency);
  const isPositive = (quote.change || 0) >= 0;

  return (
    <HeaderContainer>
      <CompanyInfo>
        {profile.image && <CompanyLogo src={profile.image} alt={`${profile.companyName} logo`} />}
        <TextContainer>
          <CompanyName>
            {profile.companyName}
            {/* On Desktop, symbol is next to name. On Mobile, we put it below via flex direction logic above */}
            <span style={{ display: 'inline-block' }}>
               <CompanySymbol>{profile.symbol}</CompanySymbol>
            </span>
          </CompanyName>
        </TextContainer>
      </CompanyInfo>
      
      <PriceInfo>
        <CurrentPrice>{currencySymbol}{(quote.price || 0).toFixed(2)}</CurrentPrice>
        <PriceChange isPositive={isPositive}>
            {isPositive ? '+' : ''}{(quote.change || 0).toFixed(2)} ({(quote.changesPercentage || 0).toFixed(2)}%)
        </PriceChange>
      </PriceInfo>
    </HeaderContainer>
  );
};

export default StockHeader;