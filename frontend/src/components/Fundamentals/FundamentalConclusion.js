import React, { useMemo } from 'react';
import styled, { keyframes } from 'styled-components';

// --- Styled Components & Animations for our "Extreme Graphics" UI ---

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const SectionContainer = styled.div`
  animation: ${fadeIn} 0.5s ease-out;
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-text-primary);
`;

const ConclusionGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  align-items: center;

  @media (max-width: 992px) {
    grid-template-columns: 1fr;
  }
`;

const GradeCircle = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  // A beautiful gradient background for the inner circle
  background: radial-gradient(circle, var(--color-secondary) 60%, transparent 61%);
  // A thick, vibrant border whose color is determined by the grade
  border: 8px solid ${({ color }) => color};
  // A subtle glow effect that matches the border color
  box-shadow: 0 0 25px ${({ color }) => color}33;
  margin: 0 auto;
  transition: all 0.5s ease-in-out;
`;

const GradeText = styled.span`
  font-size: 5rem;
  font-weight: 800;
  line-height: 1;
  color: ${({ color }) => color};
`;

const ThesisText = styled.p`
  font-size: 1.5rem;
  font-weight: 500;
  color: var(--color-text-primary);
  line-height: 1.6;
  margin-bottom: 2rem;
  text-align: center;
  border-left: 3px solid var(--color-primary);
  padding-left: 1.5rem;
`;

const TakeawaysList = styled.ul`
  list-style-type: none;
  padding-left: 0;
`;

const TakeawayItem = styled.li`
  margin-bottom: 1rem;
  color: var(--color-text-secondary);
  display: flex;
  align-items: flex-start;
  line-height: 1.6;

  &::before {
    content: '▪';
    color: var(--color-primary);
    margin-right: 12px;
    font-size: 1.5rem;
    line-height: 1.6;
  }
`;

// --- The New "Display-Only" React Component ---

const FundamentalConclusion = ({ conclusionData }) => {

  // The parser and color logic is now the only "brain" in this component.
  const parsedConclusion = useMemo(() => {
    if (!conclusionData) {
      return { grade: 'N/A', thesis: 'Synthesizing data...', takeaways: [] };
    }
    
    const lines = conclusionData.split('\n');
    const grade = lines.find(l => l.startsWith('GRADE:'))?.replace('GRADE:', '').trim() || 'N/A';
    const thesis = lines.find(l => l.startsWith('THESIS:'))?.replace('THESIS:', '').trim() || 'No thesis available.';
    const takeaways = lines.filter(l => l.startsWith('- ')).map(l => l.replace('- ', '').trim());

    return { grade, thesis, takeaways };
  }, [conclusionData]);

  const getGradeColor = (grade) => {
    if (grade.startsWith('A')) return 'var(--color-success)';
    if (grade.startsWith('B')) return '#34D399';
    if (grade.startsWith('C')) return '#EDBB5A';
    if (grade.startsWith('D')) return '#F88149';
    if (grade.startsWith('F')) return 'var(--color-danger)';
    return 'var(--color-text-secondary)';
  };
  const gradeColor = getGradeColor(parsedConclusion.grade);

  // --- All useEffect and isLoading logic has been REMOVED ---

  return (
    <SectionContainer>
      <SectionTitle>Analyst's Conclusion</SectionTitle>
      
      <ThesisText>"{parsedConclusion.thesis}"</ThesisText>
      
      <ConclusionGrid>
        <GradeCircle color={gradeColor}>
          <GradeText color={gradeColor}>{parsedConclusion.grade}</GradeText>
        </GradeCircle>
        <div>
          <h4 style={{ fontWeight: 600, color: 'var(--color-text-primary)', marginBottom: '1rem' }}>Key Takeaways:</h4>
          <TakeawaysList>
            {parsedConclusion.takeaways.map((item, index) => (
              <TakeawayItem key={index}>{item}</TakeawayItem>
            ))}
          </TakeawaysList>
        </div>
      </ConclusionGrid>
    </SectionContainer>
  );
};

export default FundamentalConclusion;