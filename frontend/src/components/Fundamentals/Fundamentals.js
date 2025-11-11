import React, { useState, useEffect, useMemo } from 'react';
import styled, { keyframes } from 'styled-components';
import Card from '../common/Card';
import axios from 'axios';

// --- (Styled Components are unchanged) ---
const fadeIn = keyframes`from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); }`;
const SectionContainer = styled.div`margin-bottom: 3rem; animation: ${fadeIn} 0.5s ease-out;`;
const SectionTitle = styled.h3`font-size: 1.5rem; font-weight: 600; margin-bottom: 1.5rem; color: var(--color-text-primary);`;
const PiotroskiGrid = styled.div`display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; align-items: center; @media (max-width: 768px) { grid-template-columns: 1fr; }`;
const ScoreCard = styled.div`display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2rem; background-color: var(--color-background); border-radius: 50%; width: 180px; height: 180px; border: 4px solid ${({ scoreColor }) => scoreColor}; margin: 0 auto;`;
const ScoreValue = styled.span`font-size: 4rem; font-weight: 800; color: ${({ scoreColor }) => scoreColor};`;
const ScoreLabel = styled.span`font-size: 1rem; font-weight: 500; color: var(--color-text-secondary);`;
const CriteriaList = styled.ul`list-style-type: none; padding-left: 0;`;
const CriteriaListItem = styled.li`margin-bottom: 0.75rem; color: var(--color-text-primary); display: flex; align-items: center; &::before { content: '✓'; color: var(--color-success); margin-right: 12px; font-size: 1.2rem; font-weight: bold; }`;
const AssessmentTable = styled.div`display: grid; grid-template-columns: 1fr 1fr 2fr; gap: 1px; background-color: var(--color-border); border: 1px solid var(--color-border); border-radius: 8px; overflow: hidden; & > div { background-color: var(--color-secondary); padding: 1rem; } & > .header { font-weight: 600; color: var(--color-text-secondary); background-color: var(--color-background); }`;
const Loader = styled.div`color: var(--color-primary); animation: ${fadeIn} 0.5s ease-in;`;


// --- The Updated React Component ---

// The component now accepts the 'delay' prop
const Fundamentals = ({ symbol, profile, keyMetrics, piotroskiData, delay }) => {
  const [assessment, setAssessment] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAiAssessment = async () => {
      if (!symbol || !profile || !keyMetrics) {
        setIsLoading(false);
        return;
      }
      
      setIsLoading(true);
      try {
        const payload = {
            companyName: profile.companyName,
            keyMetrics: keyMetrics,
        };
        const response = await axios.post(`/api/stocks/${symbol}/fundamental-analysis`, payload);
        setAssessment(response.data.assessment);
      } catch (error) {
        console.error("Failed to fetch AI fundamental assessment:", error);
        setAssessment("Could not generate AI-powered assessment at this time.");
      } finally {
        setIsLoading(false);
      }
    };

    // --- NEW DELAY LOGIC ---
    // We wrap the API call in a setTimeout to stagger the request.
    const timer = setTimeout(() => {
        fetchAiAssessment();
    }, delay || 0);

    return () => clearTimeout(timer);

  }, [symbol, profile, keyMetrics, delay]); // Added 'delay' to the dependency array


  // --- (The rest of the component logic is unchanged) ---
  const { score, criteria } = piotroskiData || {};
  const getScoreColor = () => {
    if (score >= 7) return 'var(--color-success)';
    if (score >= 4) return '#EDBB5A';
    return 'var(--color-danger)';
  };
  const scoreColor = getScoreColor();
  
  const parsedAssessment = useMemo(() => {
    if (!assessment || typeof assessment !== 'string') return [];
    return assessment
        .split('\n')
        .map(row => row.split('|').map(cell => cell.trim()))
        .filter(row => row.length > 3 && !row[1].includes('---'));
  }, [assessment]);

  return (
    <Card>
      <SectionContainer>
        <SectionTitle>Piotroski F-Score Analysis</SectionTitle>
        {piotroskiData && piotroskiData.score > 0 ? (
          <PiotroskiGrid>
            <ScoreCard scoreColor={scoreColor}>
              <ScoreValue scoreColor={scoreColor}>{score}</ScoreValue>
              <ScoreLabel>/ 9</ScoreLabel>
            </ScoreCard>
            <div>
              <p style={{ color: 'var(--color-text-secondary)', marginBottom: '1rem' }}>
                The F-Score reflects financial strength. High scores (7-9) are considered strong.
              </p>
              <CriteriaList>
                {criteria && criteria.map((item, index) => (
                  <CriteriaListItem key={index}>{item}</CriteriaListItem>
                ))}
              </CriteriaList>
            </div>
          </PiotroskiGrid>
        ) : <p>Piotroski F-Score data not available for this stock.</p>}
      </SectionContainer>

      <SectionContainer>
        <SectionTitle>Investment Philosophy Assessment</SectionTitle>
        {isLoading ? (
          <Loader>Generating AI analysis...</Loader>
        ) : (
          parsedAssessment.length > 0 ? (
            <AssessmentTable>
                <div className="header">Formula</div>
                <div className="header">Key Criteria</div>
                <div className="header">Assessment</div>
                {parsedAssessment.map((row, rowIndex) => (
                    <React.Fragment key={rowIndex}>
                        <div>{row[1]}</div>
                        <div>{row[2]}</div>
                        <div>{row[3]}</div>
                    </React.Fragment>
                ))}
            </AssessmentTable>
          ) : <p>Could not generate AI assessment for this stock.</p>
        )}
      </SectionContainer>
      
    </Card>
  );
};

export default Fundamentals;