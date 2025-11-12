import React from 'react';
import styled from 'styled-components';

// --- Styled Components (reusing our professional styles) ---

const SectionContainer = styled.div`
  /* Main container for this scan */
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-text-primary);
`;

const ScanGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  align-items: center;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const ScoreCard = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: var(--color-background);
  border-radius: 50%;
  width: 180px;
  height: 180px;
  border: 4px solid ${({ scoreColor }) => scoreColor};
  margin: 0 auto;
`;

const ScoreValue = styled.span`
  font-size: 4rem;
  font-weight: 800;
  color: ${({ scoreColor }) => scoreColor};
`;

const ScoreLabel = styled.span`
  font-size: 1rem;
  font-weight: 500;
  color: var(--color-text-secondary);
`;

const CriteriaList = styled.ul`
  list-style-type: none;
  padding-left: 0;
`;

const CriteriaListItem = styled.li`
  margin-bottom: 0.75rem;
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
  line-height: 1.6;

  &::before {
    content: '✓';
    color: var(--color-success);
    margin-right: 12px;
    font-size: 1.2rem;
    font-weight: bold;
  }
`;

// --- The React Component ---

const BenjaminGrahamScan = ({ scanData }) => {
  // If we don't have the data from the backend, show an informative message.
  if (!scanData || !scanData.criteria) {
    return (
      <SectionContainer>
        <SectionTitle>Benjamin Graham Scan</SectionTitle>
        <p>Graham scan data is not available or could not be calculated.</p>
      </SectionContainer>
    );
  }

  const { score, criteria } = scanData;

  // Determine the color based on the score (0-2 Red, 3-5 Yellow, 6-7 Green)
  const getScoreColor = () => {
    if (score >= 6) return 'var(--color-success)';
    if (score >= 3) return '#EDBB5A'; // Neutral Yellow
    return 'var(--color-danger)';
  };
  const scoreColor = getScoreColor();

  return (
    <SectionContainer>
      <SectionTitle>Benjamin Graham Scan</SectionTitle>
      <ScanGrid>
        <ScoreCard scoreColor={scoreColor}>
          <ScoreValue scoreColor={scoreColor}>{score}</ScoreValue>
          <ScoreLabel>/ 7 Tenets</ScoreLabel>
        </ScoreCard>
        <div>
          <p style={{ color: 'var(--color-text-secondary)', marginBottom: '1.5rem', lineHeight: 1.6 }}>
            A checklist for the "defensive investor" based on the principles of the father of value investing. A high score suggests a stable, reasonably priced company.
          </p>
          <CriteriaList>
            {criteria.map((item, index) => (
              <CriteriaListItem key={index}>{item}</CriteriaListItem>
            ))}
          </CriteriaList>
        </div>
      </ScanGrid>
    </SectionContainer>
  );
};

export default BenjaminGrahamScan;