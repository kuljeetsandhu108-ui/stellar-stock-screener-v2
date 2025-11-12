import React, { useMemo } from 'react';
import styled, { keyframes } from 'styled-components';
import Card from '../common/Card'; // We will now use our master Card component for each quadrant.

// --- Styled Components & Animations for the new design ---

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

// This grid will hold our four individual Card components, creating the quadrant effect.
const SwotCardGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  animation: ${fadeIn} 0.5s ease-in;

  /* On smaller screens, stack the cards vertically */
  @media (max-width: 992px) {
    grid-template-columns: 1fr;
  }
`;

// We no longer need the custom QuadrantTitle, as our Card component has its own title prop.
const SwotList = styled.ul`
  list-style-type: none;
  padding-left: 0;
  margin-top: 0; /* Adjusted for better spacing inside the card */
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

// --- The Final, Redesigned "Display Only" Component ---

const SwotAnalysis = ({ analysisText, isLoading }) => {

  // useMemo ensures this complex parsing only runs when the AI text changes.
  const swotData = useMemo(() => {
    if (!analysisText) {
      return null;
    }

    const sections = ['Strengths', 'Weaknesses', 'Opportunities', 'Threats'];
    const data = {
      Strengths: [],
      Weaknesses: [],
      Opportunities: [],
      Threats: []
    };
    
    // Split the entire text block into individual lines for robust processing.
    const lines = analysisText.split('\n');
    let currentSection = null;

    // We iterate through each line of the AI's response.
    lines.forEach(line => {
      const trimmedLine = line.trim();

      // Check if the current line is a new section header.
      const foundSection = sections.find(section => trimmedLine.includes(`**${section}**`));
      
      if (foundSection) {
        // If it's a header, we update our state to know which section we are in.
        currentSection = foundSection;
      } else if (currentSection && (trimmedLine.startsWith('*') || trimmedLine.startsWith('-'))) {
        // If we are inside a section and the line is a bullet point, we clean and add it.
        const point = trimmedLine
            .replace(/^[\*\-]\s?/, '') // Remove the leading '*' or '-'
            .replace(/\*\*.*?\*\*/g, '') // Remove any extra bolded text
            .trim();
        
        if (point) {
          data[currentSection].push(point);
        }
      }
    });

    return data;
  }, [analysisText]);

  // --- RENDER LOGIC ---

  if (isLoading) {
    return (
      <Card title="AI-Powered SWOT Analysis">
        <Loader>Generating AI analysis...</Loader>
      </Card>
    );
  }

  // If parsing failed or the AI returned no valid points, show the raw text as a safe fallback.
  if (!swotData || Object.values(swotData).every(arr => arr.length === 0)) {
    return (
      <Card title="AI-Powered SWOT Analysis">
        <p style={{ lineHeight: 1.7, color: 'var(--color-text-secondary)' }}>
          {analysisText || "Could not generate SWOT analysis for this stock."}
        </p>
      </Card>
    );
  }

  // If we have data, render the new, robust, and beautiful four-card layout.
  return (
    <div>
      <h2 style={{ fontSize: '1.8rem', fontWeight: 600, marginBottom: '1.5rem', color: 'var(--color-text-primary)' }}>
        AI-Powered SWOT Analysis
      </h2>
      <SwotCardGrid>
        <Card title="Strengths">
          <SwotList>
            {swotData.Strengths.map((item, index) => <SwotListItem key={`s-${index}`}>{item}</SwotListItem>)}
          </SwotList>
        </Card>
        
        <Card title="Weaknesses">
          <SwotList>
            {swotData.Weaknesses.map((item, index) => <SwotListItem key={`w-${index}`}>{item}</SwotListItem>)}
          </SwotList>
        </Card>
        
        <Card title="Opportunities">
          <SwotList>
            {swotData.Opportunities.map((item, index) => <SwotListItem key={`o-${index}`}>{item}</SwotListItem>)}
          </SwotList>
        </Card>
        
        <Card title="Threats">
          <SwotList>
            {swotData.Threats.map((item, index) => <SwotListItem key={`t-${index}`}>{item}</SwotListItem>)}
          </SwotList>
        </Card>
      </SwotCardGrid>
    </div>
  );
};

export default SwotAnalysis;