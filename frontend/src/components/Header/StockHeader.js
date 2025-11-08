import React from 'react';
import styled from 'styled-components';

// --- Styled Components ---

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
  gap: 1.5rem; /* Space between logo and text */
`;

const CompanyLogo = styled.img`
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #fff; /* White background for logos that are transparent */
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

// This component's color will change based on the 'isPositive' prop
const PriceChange = styled.div`
  font-size: 1.2rem;
  font-weight: 500;
  color: ${({ isPositive }) => (isPositive ? 'var(--color-success)' : 'var(--color-danger)')};
`;


// --- React Component ---

const StockHeader = ({ profile, quote }) => {
  // Defensive check to prevent errors if data is missing
  if (!profile || !quote) {
    return null;
  }

  // Determine if the stock price change is positive or negative
  const isPositive = quote.change >= 0;

  // Format the numbers for a clean display
  const formattedPrice = (quote.price || 0).toFixed(2);
  const formattedChange = (quote.change || 0).toFixed(2);
  const formattedChangePercent = (quote.changesPercentage || 0).toFixed(2);
  
  // Construct the price change string, e.g., "+1.50 (0.75%)"
  const changeText = `${isPositive ? '+' : ''}${formattedChange} (${formattedChangePercent}%)`;

  return (
    <HeaderContainer>
      <CompanyInfo>
        {/* Display company logo if available in the profile data */}
        {profile.image && <CompanyLogo src={profile.image} alt={`${profile.companyName} logo`} />}
        <div>
          <CompanyName>
            {profile.companyName}
            <CompanySymbol>{profile.symbol}</CompanySymbol>
          </CompanyName>
        </div>
      </CompanyInfo>
      <PriceInfo>
        <CurrentPrice>${formattedPrice}</CurrentPrice>
        <PriceChange isPositive={isPositive}>
            {changeText}
        </PriceChange>
      </PriceInfo>
    </HeaderContainer>
  );
};

export default StockHeader;