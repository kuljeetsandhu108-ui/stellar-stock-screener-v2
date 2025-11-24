import React from 'react';
import styled from 'styled-components';
import GaugeChart from 'react-gauge-chart';

// --- Styled Components (No changes here) ---

const DialContainer = styled.div`
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
`;

const RatingText = styled.div`
  font-size: 2rem;
  font-weight: 700;
  text-align: center;
  margin-top: -30px;
  color: ${({ $ratingColor }) => $ratingColor};
`;

// --- The React Component (Logic is now more robust) ---

const RatingDial = ({ rating }) => {
  const getRatingDetails = () => {
    // --- THIS IS THE CRITICAL FIX ---
    // We add a "guard clause". If the rating prop is missing or not a string,
    // we default to a Neutral state immediately. This prevents the .toLowerCase() error.
    if (!rating || typeof rating !== 'string') {
      return { percent: 0.5, color: 'var(--color-text-secondary)', text: 'Neutral' };
    }

    // The rest of the logic remains the same
    switch (rating.toLowerCase()) {
      case 'strong buy':
      case 'bullish':
      case 'very bullish':
        return { percent: 0.9, color: 'var(--color-success)', text: 'Strong Buy' };
      case 'buy':
      case 'outperform':
        return { percent: 0.7, color: 'var(--color-success)', text: 'Buy' };
      case 'hold':
      case 'neutral':
        return { percent: 0.5, color: '#EDBB5A', text: 'Hold' };
      case 'sell':
      case 'underperform':
        return { percent: 0.3, color: 'var(--color-danger)', text: 'Sell' };
      case 'strong sell':
      case 'bearish':
        return { percent: 0.1, color: 'var(--color-danger)', text: 'Strong Sell' };
      default:
        return { percent: 0.5, color: 'var(--color-text-secondary)', text: 'Neutral' };
    }
  };

  const { percent, color, text } = getRatingDetails();

  return (
    <DialContainer>
      <GaugeChart
        id="technical-rating-gauge"
        nrOfLevels={30}
        colors={['#F85149', '#EDBB5A', '#3FB950']}
        arcWidth={0.3}
        percent={percent}
        textColor={'transparent'}
        needleBaseColor={'#FFFFFF'}
        needleColor={'#C9D1D9'}
        animate={true}
        animDelay={500}
      />
        <RatingText $ratingColor={color}>
        {text}
      </RatingText>
    </DialContainer>
  );
};

export default RatingDial;