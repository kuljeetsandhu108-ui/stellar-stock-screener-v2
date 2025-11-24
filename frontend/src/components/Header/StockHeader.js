import React from 'react';
import styled from 'styled-components';

// --- (Styled Components are unchanged) ---
const HeaderContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: var(--color-secondary);
  border: 1px solid var(--color-border);
  border-radius: 12px;
`;
const CompanyInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 1.5rem;
`;
const CompanyLogo = styled.img`
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #fff;
`;
const CompanyName = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
`;
const CompanySymbol = styled.span`
  font-size: 1.2rem;
  color: var(--color-text-secondary);
  margin-left: 0.75rem;
  font-weight: 500;
`;
const PriceInfo = styled.div`
  text-align: right;
`;
const CurrentPrice = styled.div`
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
`;
const PriceChange = styled.div`
  font-size: 1.2rem;
  font-weight: 500;
  color: ${({ $isPositive }) => ($isPositive ? 'var(--color-success)' : 'var(--color-danger)')};
`;

// --- NEW HELPER FUNCTION TO GET CURRENCY SYMBOL ---
const getCurrencySymbol = (currencyCode) => {
    switch (currencyCode) {
        case 'INR':
            return '₹';
        case 'USD':
            return '$';
        case 'JPY':
            return '¥';
        // Add more currencies as needed
        default:
            return '$'; // Default to dollar
    }
};


// --- The Updated React Component ---
const StockHeader = ({ profile, quote }) => {
  if (!profile || !quote) {
    return null;
  }

  // --- NEW: Get the currency symbol from the profile data ---
  const currencySymbol = getCurrencySymbol(profile.currency);

  const isPositive = (quote.change || 0) >= 0;
  const formattedPrice = (quote.price || 0).toFixed(2);
  const formattedChange = (quote.change || 0).toFixed(2);
  const formattedChangePercent = (quote.changesPercentage || 0).toFixed(2);
  const changeText = `${isPositive ? '+' : ''}${formattedChange} (${formattedChangePercent}%)`;

  return (
    <HeaderContainer>
      <CompanyInfo>
        {profile.image && <CompanyLogo src={profile.image} alt={`${profile.companyName} logo`} />}
        <div>
          <CompanyName>
            {profile.companyName}
            <CompanySymbol>{profile.symbol}</CompanySymbol>
          </CompanyName>
        </div>
      </CompanyInfo>
      <PriceInfo>
        {/* --- NEW: Use the dynamic currency symbol --- */}
        <CurrentPrice>{currencySymbol}{formattedPrice}</CurrentPrice>
        <PriceChange $isPositive={isPositive}>
            {changeText}
        </PriceChange>
      </PriceInfo>
    </HeaderContainer>
  );
};

export default StockHeader;