import React, { useState, useMemo } from 'react';
import styled from 'styled-components';
import Card from '../common/Card';

// --- Styled Components ---

const TabContainer = styled.div`
  display: flex;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid var(--color-border);
`;

const TabButton = styled.button`
  padding: 10px 20px;
  border: none;
  background-color: transparent;
  color: ${({ active }) => (active ? 'var(--color-primary)' : 'var(--color-text-secondary)')};
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  position: relative;
  transition: color 0.3s ease;

  /* The active tab indicator line */
  &::after {
    content: '';
    position: absolute;
    bottom: -1px; /* Align with the container's border */
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--color-primary);
    transform: ${({ active }) => (active ? 'scaleX(1)' : 'scaleX(0)')};
    transition: transform 0.3s ease;
  }
`;

const ContentContainer = styled.div`
  min-height: 200px; /* Ensures consistent card height */
`;

const SwotList = styled.ul`
  list-style-type: none;
  padding-left: 0;
`;

const SwotListItem = styled.li`
  margin-bottom: 0.75rem;
  color: var(--color-text-primary);
  line-height: 1.6;
  
  &::before {
    content: '✓'; /* Simple bullet point */
    color: var(--color-success);
    margin-right: 10px;
    font-weight: bold;
  }
`;


// --- React Component ---

const SwotAnalysis = ({ analysisText }) => {
  const [activeTab, setActiveTab] = useState('Strengths');

  // useMemo will parse the text only once, improving performance
  const swotData = useMemo(() => {
    if (!analysisText) return {};

    const sections = ['Strengths', 'Weaknesses', 'Opportunities', 'Threats'];
    const data = {};

    // Split the text into sections based on the titles
    const parts = analysisText.split(/\n(?=Strengths|Weaknesses|Opportunities|Threats)/);

    parts.forEach(part => {
      const trimmedPart = part.trim();
      for (const section of sections) {
        if (trimmedPart.startsWith(section)) {
          // Get the content, remove the title, and split into bullet points
          data[section] = trimmedPart
            .replace(new RegExp(`^${section}:?`, 'i'), '')
            .trim()
            .split(/-\s|\*\s|\n/) // Split by bullets or newlines
            .map(item => item.trim())
            .filter(item => item); // Filter out any empty lines
        }
      }
    });
    return data;
  }, [analysisText]);

  const tabs = Object.keys(swotData);

  if (tabs.length === 0) {
    return (
        <Card title="AI-Powered SWOT Analysis">
            <p>Could not generate SWOT analysis for this stock.</p>
        </Card>
    );
  }

  return (
    <Card title="AI-Powered SWOT Analysis">
      <TabContainer>
        {tabs.map(tab => (
          <TabButton
            key={tab}
            active={activeTab === tab}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </TabButton>
        ))}
      </TabContainer>
      <ContentContainer>
        <SwotList>
          {swotData[activeTab] && swotData[activeTab].map((item, index) => (
            <SwotListItem key={index}>{item}</SwotListItem>
          ))}
        </SwotList>
      </ContentContainer>
    </Card>
  );
};

export default SwotAnalysis;