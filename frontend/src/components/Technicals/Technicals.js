import React from 'react';
import styled from 'styled-components';
import Card from '../common/Card';
import RatingDial from './RatingDial';
import PivotLevels from './PivotLevels';
import MovingAverages from './MovingAverages';

// --- Styled Components ---

const TopSectionGrid = styled.div`
  display: grid;
  /* Two columns: the dial takes up more space than the table */
  grid-template-columns: 2fr 1fr; 
  gap: 2rem;
  align-items: center;
  padding-bottom: 2rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--color-border);

  /* On smaller screens, stack them */
  @media (max-width: 992px) {
    grid-template-columns: 1fr;
  }
`;

const BottomSection = styled.div`
  /* This section will hold the pivot levels table */
`;

// --- React Component ---

const Technicals = ({ analystRatings }) => {

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
        <PivotLevels />
      </BottomSection>

    </Card>
  );
};

export default Technicals;