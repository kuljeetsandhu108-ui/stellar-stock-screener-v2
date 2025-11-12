import React from 'react';
import styled from 'styled-components';
import GaugeChart from 'react-gauge-chart';
import Card from '../common/Card';

// --- Styled Components for an "Extreme Graphics" Dial ---

const SentimentContainer = styled.div`
  width: 100%;
  padding: 1rem;
`;

const GaugeWrapper = styled.div`
  width: 100%;
  max-width: 350px;
  margin: 0 auto;
`;

const VerdictText = styled.div`
  font-size: 2.2rem;
  font-weight: 800;
  text-align: center;
  margin-top: -50px; /* Pull the text up into the gauge */
  color: ${({ color }) => color};
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
`;

const ScoreText = styled.div`
  font-size: 1rem;
  font-weight: 500;
  text-align: center;
  color: var(--color-text-secondary);
  margin-top: 5px;
`;

// --- The React Component ---

const OverallSentiment = ({ sentimentData }) => {
  if (!sentimentData) {
    return (
      <Card title="Overall Sentiment">
        <p>Sentiment data could not be calculated.</p>
      </Card>
    );
  }

  const { score, verdict } = sentimentData;

  // Convert the 0-100 score to a 0-1 percentage for the gauge
  const gaugePercent = score / 100;

  // Determine the color for the verdict text based on the score
  const getVerdictColor = () => {
    if (score > 75) return 'var(--color-success)';
    if (score > 60) return '#34D399'; // A lighter green
    if (score < 25) return 'var(--color-danger)';
    if (score < 40) return '#F87171'; // A lighter red
    return '#EDBB5A'; // Neutral Yellow
  };
  const verdictColor = getVerdictColor();

  return (
    <Card title="Overall Sentiment">
      <SentimentContainer>
        <GaugeWrapper>
          <GaugeChart
            id="sentiment-gauge"
            nrOfLevels={40}
            arcsLength={[0.2, 0.2, 0.2, 0.2, 0.2]} // 5 equal sections
            colors={['#F85149', '#F88149', '#EDBB5A', '#3FB950', '#17C3B2']}
            percent={gaugePercent}
            arcPadding={0.02}
            cornerRadius={3}
            textColor={'transparent'} // Hide the default percentage
            needleBaseColor={'#FFFFFF'}
            needleColor={'#C9D1D9'}
            animate={true}
            animDelay={500}
          />
          <VerdictText color={verdictColor}>{verdict}</VerdictText>
          <ScoreText>Score: {score.toFixed(0)} / 100</ScoreText>
        </GaugeWrapper>
      </SentimentContainer>
    </Card>
  );
};

export default OverallSentiment;