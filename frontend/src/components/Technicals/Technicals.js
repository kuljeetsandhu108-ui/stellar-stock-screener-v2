import React from 'react';
import styled from 'styled-components';
import Card from '../common/Card';
import RatingDial from './RatingDial';
import PivotLevels from './PivotLevels';
import MovingAverages from './MovingAverages';
// --- NEW IMPORT ---
import TechnicalIndicatorsTable from './TechnicalIndicatorsTable';

// --- Styled Components ---

const TopSectionGrid = styled.div`
  display: grid;
  /* Two columns: the dial takes up more space than the table */
  grid-template-columns: 2fr 1fr; 
  gap: 2rem;
  align-items: center;
  padding-bottom: 2rem;
  
  /* On smaller screens, stack them */
  @media (max-width: 992px) {
    grid-template-columns: 1fr;
  }
`;

const BottomSection = styled.div`
  /* This section will hold the pivot levels table and the new indicators table */
`;

// --- React Component ---

// The component now accepts the new 'technicalIndicators' data prop
const Technicals = ({ analystRatings, technicalIndicators }) => {

  // We need to get the latest analyst rating to feed into our dial.
  // The FMP API provides an array of ratings, with the most recent first.
  let latestRating = "Neutral"; // Default value

  if (analystRatings && Array.isArray(analystRatings) && analystRatings.length > 0) {
    // We'll use the 'rating' field, e.g., "Buy", "Hold", "Strong Sell"
    latestRating = analystRatings[0].rating;
  }

  return (
    <Card title="Technical Summary">
      
      {/* --- Top Section --- */}
      <TopSectionGrid>
        {/* Left column */}
        <RatingDial rating={latestRating} />
        {/* Right column */}
        <MovingAverages />
      </TopSectionGrid>

      {/* --- Bottom Section --- */}
      <BottomSection>
        {/* The new indicators table is added here, passing the data down */}
        <TechnicalIndicatorsTable indicators={technicalIndicators} />
        
        {/* The PivotLevels table is now below the new table */}
        <div style={{ marginTop: '2rem' }}>
          <PivotLevels />
        </div>
      </BottomSection>

    </Card>
  );
};

export default Technicals;