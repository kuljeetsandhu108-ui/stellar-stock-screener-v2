import React, { useMemo } from 'react';
import styled from 'styled-components';
import GaugeChart from 'react-gauge-chart';

//...(Styled components are unchanged)...
const RatingContainer = styled.div`
  width: 100%;
`;
const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 2rem;
  color: var(--color-text-primary);
`;
const GaugeWrapper = styled.div`
  max-width: 450px;
  margin: 0 auto;
`;
const RatingText = styled.div`
  font-size: 1.8rem;
  font-weight: 700;
  text-align: center;
  margin-top: -40px;
  color: ${({ color }) => color};
`;
const BreakdownList = styled.div`
  margin-top: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;
const BreakdownItem = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
`;
const BreakdownLabel = styled.span`
  font-size: 1rem;
  color: var(--color-text-secondary);
  width: 100px;
`;
const BreakdownBarContainer = styled.div`
  flex-grow: 1;
  height: 8px;
  background-color: var(--color-border);
  border-radius: 4px;
  margin: 0 1rem;
`;
const BreakdownBar = styled.div`
  height: 100%;
  width: ${({ percent }) => percent}%;
  background-color: ${({ color }) => color};
  border-radius: 4px;
  transition: width 0.5s ease-out;
`;
const BreakdownValue = styled.span`
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-primary);
  width: 30px;
  text-align: right;
`;


const AnalystRating = ({ ratingsData }) => {
  const processedRatings = useMemo(() => {
    // MORE ROBUST CHECK: Ensure the array exists and has content.
    if (!ratingsData || !Array.isArray(ratingsData) || ratingsData.length === 0) {
      return null;
    }

    const ratingMap = {
      'strongSell': { count: 0, text: 'Strong Sell', color: '#F85149' },
      'sell': { count: 0, text: 'Sell', color: '#F88149' },
      'hold': { count: 0, text: 'Hold', color: '#EDBB5A' },
      'buy': { count: 0, text: 'Buy', color: '#3FB950' },
      'strongBuy': { count: 0, text: 'Strong Buy', color: '#17C3B2' },
    };

    let totalAnalysts = 0;

    // The FMP API gives the breakdown directly in the first object of the array
    const latestRatingData = ratingsData[0];
    
    ratingMap.strongSell.count = latestRatingData.ratingStrongSell || 0;
    ratingMap.sell.count = latestRatingData.ratingSell || 0;
    ratingMap.hold.count = latestRatingData.ratingHold || 0;
    ratingMap.buy.count = latestRatingData.ratingBuy || 0;
    ratingMap.strongBuy.count = latestRatingData.ratingStrongBuy || 0;

    totalAnalysts = Object.values(ratingMap).reduce((sum, item) => sum + item.count, 0);
    
    // FINAL GUARD: If after all that, we have no analysts, return null.
    if (totalAnalysts === 0) return null;

    let totalScore = 0;
    totalScore += ratingMap.strongSell.count * 1;
    totalScore += ratingMap.sell.count * 2;
    totalScore += ratingMap.hold.count * 3;
    totalScore += ratingMap.buy.count * 4;
    totalScore += ratingMap.strongBuy.count * 5;

    const averageScore = totalScore / totalAnalysts;
    const gaugePercent = (averageScore - 1) / 4;

    let consensusText = 'Hold';
    let consensusColor = ratingMap.hold.color;
    if (averageScore > 4.5) { consensusText = 'Strong Buy'; consensusColor = ratingMap.strongBuy.color; }
    else if (averageScore > 3.5) { consensusText = 'Buy'; consensusColor = ratingMap.buy.color; }
    else if (averageScore < 2.5) { consensusText = 'Sell'; consensusColor = ratingMap.sell.color; }
    else if (averageScore < 1.5) { consensusText = 'Strong Sell'; consensusColor = ratingMap.strongSell.color; }

    return {
      totalAnalysts,
      gaugePercent,
      consensusText,
      consensusColor,
      breakdown: Object.values(ratingMap).reverse(),
    };
  }, [ratingsData]);

  if (!processedRatings) {
    return (
      <RatingContainer>
        <SectionTitle>Analyst Rating</SectionTitle>
        <p>Analyst rating data is not available for this stock.</p>
      </RatingContainer>
    );
  }

  const { totalAnalysts, gaugePercent, consensusText, consensusColor, breakdown } = processedRatings;

  return (
    <RatingContainer>
      <SectionTitle>Analyst Rating</SectionTitle>
      <p style={{ color: 'var(--color-text-secondary)', marginTop: '-1.5rem', marginBottom: '2rem' }}>
          Based on {totalAnalysts} analysts giving stock ratings in the past 3 months.
      </p>

      <GaugeWrapper>
        <GaugeChart id="analyst-rating-gauge" nrOfLevels={5} arcsLength={[0.2, 0.15, 0.3, 0.15, 0.2]} colors={['#F85149', '#F88149', '#EDBB5A', '#3FB950', '#17C3B2']} percent={gaugePercent} arcPadding={0.02} cornerRadius={3} textColor={'transparent'} needleBaseColor={'#FFFFFF'} needleColor={'#C9D1D9'} />
        <RatingText color={consensusColor}>{consensusText}</RatingText>
      </GaugeWrapper>

      <BreakdownList>
        {breakdown.map(item => (
          <BreakdownItem key={item.text}>
            <BreakdownLabel>{item.text}</BreakdownLabel>
            <BreakdownBarContainer>
              <BreakdownBar percent={(item.count / totalAnalysts) * 100} color={item.color} />
            </BreakdownBarContainer>
            <BreakdownValue>{item.count}</BreakdownValue>
          </BreakdownItem>
        ))}
      </BreakdownList>
    </RatingContainer>
  );
};

export default AnalystRating;