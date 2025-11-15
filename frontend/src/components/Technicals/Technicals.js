import React from 'react';
import styled from 'styled-components';
import Card from '../common/Card';
import RatingDial from './RatingDial';
import PivotLevels from './PivotLevels';
import MovingAverages from './MovingAverages';
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
  /* This section will hold our tables */
`;

// --- The Final, Upgraded React Component ---

// The component now accepts all the new data props from its parent, StockDetailPage.
const Technicals = ({ analystRatings, technicalIndicators, movingAverages, pivotPoints }) => {

  // This logic intelligently determines the overall analyst consensus for the dial.
  let latestRating = "Neutral"; // Default value

  if (analystRatings && Array.isArray(analystRatings) && analystRatings.length > 0) {
    // We use the reliable yfinance data structure.
    const ratingData = analystRatings[0];
    const strongBuy = ratingData.ratingStrongBuy || 0;
    const buy = ratingData.ratingBuy || 0;
    const hold = ratingData.ratingHold || 0;
    const sell = ratingData.ratingSell || 0;
    const strongSell = ratingData.ratingStrongSell || 0;

    // A simple but effective algorithm to find the dominant rating.
    if (strongBuy > (sell + strongSell) && strongBuy > hold) {
        latestRating = "Strong Buy";
    } else if ((strongBuy + buy) > (strongSell + sell)) {
        latestRating = "Buy";
    } else if (strongSell > (buy + strongBuy) && strongSell > hold) {
        latestRating = "Strong Sell";
    } else if ((strongSell + sell) > (strongBuy + buy)) {
        latestRating = "Sell";
    } else {
        latestRating = "Hold";
    }
  }

  return (
    <Card title="Technical Summary">
      
      {/* --- Top Section --- */}
      <TopSectionGrid>
        {/* The dial now receives a dynamically calculated rating */}
        <RatingDial rating={latestRating} />
        {/* This component now receives real, dynamic moving average data */}
        <MovingAverages maData={movingAverages} />
      </TopSectionGrid>

      {/* --- Bottom Section --- */}
      <BottomSection>
        {/* This component receives real, dynamic indicator data */}
        <TechnicalIndicatorsTable indicators={technicalIndicators} />
        
        {/* This component now receives real, dynamic pivot point data */}
        <div style={{ marginTop: '2rem' }}>
          <PivotLevels pivotData={pivotPoints} />
        </div>
      </BottomSection>

    </Card>
  );
};

export default Technicals;