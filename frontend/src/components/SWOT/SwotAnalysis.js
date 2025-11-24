import React, { useMemo } from 'react';
import styled, { keyframes } from 'styled-components';
import Card from '../common/Card';

// --- Styled Components & Animations ---

const fadeIn = keyframes`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`;

const Loader = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: var(--color-primary);
  animation: ${fadeIn} 0.5s ease-in;
`;

// The 4-quadrant grid layout
const SwotGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px; /* Creates the thin border lines */
  background-color: var(--color-border);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;
  animation: ${fadeIn} 0.5s ease-in;

  /* Stack vertically on mobile */
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const SwotQuadrant = styled.div`
  background-color: var(--color-secondary);
  padding: 1.5rem;
  min-height: 200px;
`;

const QuadrantTitle = styled.h4`
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: ${({ color }) => color};
  border-bottom: 2px solid ${({ color }) => color};
  padding-bottom: 0.5rem;
  display: inline-block;
`;

const SwotList = styled.ul`
  list-style-type: none;
  padding-left: 0;
  margin-top: 0;
`;

const SwotListItem = styled.li`
  margin-bottom: 0.75rem;
  color: var(--color-text-secondary);
  line-height: 1.6;
  padding-left: 1.5rem;
  position: relative;

  &::before {
    content: '•';
    color: var(--color-primary);
    position: absolute;
    left: 0;
    top: 0;
    font-size: 1.2rem;
    line-height: 1.6;
  }

  &:last-child {
    margin-bottom: 0;
  }
`;

// --- The Component ---

const SwotAnalysis = ({ analysisText, isLoading }) => {

  // --- ROBUST PARSING LOGIC ---
  // This logic is designed to be "fuzzy" and forgiving. 
  // It catches section headers even if the AI changes capitalization or formatting.
  const swotData = useMemo(() => {
    if (!analysisText) return null;

    const data = { Strengths: [], Weaknesses: [], Opportunities: [], Threats: [] };
    const lines = analysisText.split('\n');
    let currentSection = null;

    lines.forEach(line => {
      const cleanLine = line.trim();
      const lowerLine = cleanLine.toLowerCase();

      // Fuzzy matching for headers
      if (lowerLine.includes('strength')) currentSection = 'Strengths';
      else if (lowerLine.includes('weakness')) currentSection = 'Weaknesses';
      else if (lowerLine.includes('opportunit')) currentSection = 'Opportunities';
      else if (lowerLine.includes('threat')) currentSection = 'Threats';
      
      // Check for bullet points
      else if (currentSection && (cleanLine.startsWith('-') || cleanLine.startsWith('*') || cleanLine.startsWith('•'))) {
        // Clean up the content: remove the bullet char and any bold markdown
        const content = cleanLine
            .replace(/^[\-\*\•]\s?/, '') 
            .replace(/\*\*.*?\*\*/g, '') 
            .trim();
        
        // Only add if it's not an empty string
        if (content.length > 2) {
            data[currentSection].push(content);
        }
      }
    });
    return data;
  }, [analysisText]);

  // --- Render Logic ---

  if (isLoading) {
    return (
        <Card title="AI-Powered SWOT Analysis">
            <Loader>Generating AI analysis...</Loader>
        </Card>
    );
  }

  // Fallback: If parsing produced no data (or analysisText was empty), show raw text or message
  if (!swotData || Object.values(swotData).every(arr => arr.length === 0)) {
    return (
      <Card title="AI-Powered SWOT Analysis">
        <p style={{ lineHeight: 1.7, color: 'var(--color-text-secondary)', whiteSpace: 'pre-wrap' }}>
          {analysisText || "Could not generate SWOT analysis for this stock."}
        </p>
      </Card>
    );
  }

  return (
    <Card title="AI-Powered SWOT Analysis">
      <SwotGrid>
        <SwotQuadrant>
          <QuadrantTitle color="var(--color-success)">Strengths</QuadrantTitle>
          <SwotList>
            {swotData.Strengths.map((item, i) => <SwotListItem key={`s-${i}`}>{item}</SwotListItem>)}
          </SwotList>
        </SwotQuadrant>
        
        <SwotQuadrant>
          <QuadrantTitle color="var(--color-danger)">Weaknesses</QuadrantTitle>
          <SwotList>
            {swotData.Weaknesses.map((item, i) => <SwotListItem key={`w-${i}`}>{item}</SwotListItem>)}
          </SwotList>
        </SwotQuadrant>
        
        <SwotQuadrant>
          <QuadrantTitle color="var(--color-primary)">Opportunities</QuadrantTitle>
          <SwotList>
            {swotData.Opportunities.map((item, i) => <SwotListItem key={`o-${i}`}>{item}</SwotListItem>)}
          </SwotList>
        </SwotQuadrant>
        
        <SwotQuadrant>
          <QuadrantTitle color="#EDBB5A">Threats</QuadrantTitle>
          <SwotList>
            {swotData.Threats.map((item, i) => <SwotListItem key={`t-${i}`}>{item}</SwotListItem>)}
          </SwotList>
        </SwotQuadrant>
      </SwotGrid>
    </Card>
  );
};

export default SwotAnalysis;