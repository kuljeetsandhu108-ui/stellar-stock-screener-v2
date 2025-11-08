import React from 'react';
import styled from 'styled-components';
import GaugeChart from 'react-gauge-chart';

// --- Styled Components ---

const DialContainer = styled.div`
  width: 100%;
  max-width: 400px; /* Control the max size of the dial */
  margin: 0 auto; /* Center the dial within its container */
`;

const RatingText = styled.div`
  font-size: 2rem;
  font-weight: 700;
  text-align: center;
  margin-top: -30px; /* Pull the text up to overlap with the gauge */
  color: ${({ ratingColor }) => ratingColor}; /* Dynamic color based on rating */
`;

// --- React Component ---

const RatingDial = ({ rating }) => {
  // We need to convert the text rating (e.g., "Bullish") into a percentage for the dial.
  // We also determine the color for the text.
  const getRatingDetails = () => {
    switch (rating.toLowerCase()) {
      case 'strong buy':
      case 'bullish':
      case 'very bullish':
        return { percent: 0.9, color: 'var(--color-success)' };
      case 'buy':
      case 'outperform':
        return { percent: 0.7, color: 'var(--color-success)' };
      case 'hold':
      case 'neutral':
        return { percent: 0.5, color: '#EDBB5A' }; // A neutral yellow/orange
      case 'sell':
      case 'underperform':
        return { percent: 0.3, color: 'var(--color-danger)' };
      case 'strong sell':
      case 'bearish':
        return { percent: 0.1, color: 'var(--color-danger)' };
      default:
        return { percent: 0.5, color: 'var(--color-text-secondary)' };
    }
  };

  const { percent, color } = getRatingDetails();
  const capitalizedRating = rating.charAt(0).toUpperCase() + rating.slice(1);

  return (
    <DialContainer>
      <GaugeChart
        id="technical-rating-gauge"
        nrOfLevels={30}
        colors={['#F85149', '#EDBB5A', '#3FB950']} // Red, Yellow, Green
        arcWidth={0.3}
        percent={percent}
        textColor={'transparent'} // Hide the default percentage text
        needleBaseColor={'#FFFFFF'}
        needleColor={'#C9D1D9'}
        animate={true}
        animDelay={500}
      />
      <RatingText ratingColor={color}>
        {capitalizedRating}
      </RatingText>
    </DialContainer>
  );
};

export default RatingDial;