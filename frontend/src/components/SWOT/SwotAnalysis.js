import React, { useState, useEffect, useMemo } from 'react';
import styled, { keyframes } from 'styled-components';
import Card from '../common/Card';
import axios from 'axios';

// --- (Styled Components are unchanged) ---
const fadeIn = keyframes`from { opacity: 0; } to { opacity: 1; }`;
const Loader = styled.div`display: flex; align-items: center; justify-content: center; height: 200px; color: var(--color-primary); animation: ${fadeIn} 0.5s ease-in;`;
const TabContainer = styled.div`display: flex; margin-bottom: 1.5rem; border-bottom: 1px solid var(--color-border);`;
const TabButton = styled.button`padding: 10px 20px; border: none; background-color: transparent; color: ${({ active }) => (active ? 'var(--color-primary)' : 'var(--color-text-secondary)')}; font-size: 1rem; font-weight: 600; cursor: pointer; position: relative; transition: color 0.3s ease; &::after { content: ''; position: absolute; bottom: -1px; left: 0; width: 100%; height: 2px; background-color: var(--color-primary); transform: ${({ active }) => (active ? 'scaleX(1)' : 'scaleX(0)')}; transition: transform 0.3s ease; }`;
const ContentContainer = styled.div`min-height: 200px; animation: ${fadeIn} 0.5s ease-in;`;
const SwotList = styled.ul`list-style-type: none; padding-left: 0;`;
const SwotListItem = styled.li`margin-bottom: 0.75rem; color: var(--color-text-primary); line-height: 1.6; &::before { content: '✓'; color: var(--color-success); margin-right: 10px; font-weight: bold; }`;


// --- The Updated React Component ---

// The component now accepts the 'delay' prop
const SwotAnalysis = ({ symbol, profile, delay }) => {
  const [analysisText, setAnalysisText] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('Strengths');

  useEffect(() => {
    const fetchSwotData = async () => {
      if (!symbol || !profile || !profile.companyName || !profile.description) {
        setIsLoading(false);
        return;
      }
      
      setIsLoading(true);
      try {
        const payload = {
            companyName: profile.companyName,
            description: profile.description,
        };
        const response = await axios.post(`/api/stocks/${symbol}/swot`, payload);
        setAnalysisText(response.data.swot_analysis);
      } catch (error) {
        console.error("Failed to fetch SWOT analysis:", error);
        setAnalysisText('');
      } finally {
        setIsLoading(false);
      }
    };

    // --- NEW DELAY LOGIC ---
    // We wrap the API call in a setTimeout to stagger the request.
    const timer = setTimeout(() => {
        fetchSwotData();
    }, delay || 0); // Use the delay prop, or default to 0ms.

    // This is a cleanup function to prevent errors if the component unmounts.
    return () => clearTimeout(timer);

  }, [symbol, profile, delay]); // Added 'delay' to the dependency array

  // --- (The rest of the component logic is unchanged) ---
  const swotData = useMemo(() => {
    if (!analysisText) return {};
    const sections = ['Strengths', 'Weaknesses', 'Opportunities', 'Threats'];
    const data = {};
    const parts = analysisText.split(/\n(?=Strengths|Weaknesses|Opportunities|Threats)/);
    parts.forEach(part => {
      const trimmedPart = part.trim();
      for (const section of sections) {
        if (trimmedPart.startsWith(section)) {
          data[section] = trimmedPart.replace(new RegExp(`^${section}:?`, 'i'), '').trim().split(/-\s|\*\s|\n/).map(item => item.trim()).filter(Boolean);
        }
      }
    });
    return data;
  }, [analysisText]);

  const tabs = Object.keys(swotData);

  if (isLoading) {
    return (
        <Card title="AI-Powered SWOT Analysis">
            <Loader>Generating AI analysis...</Loader>
        </Card>
    );
  }

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
          <TabButton key={tab} active={activeTab === tab} onClick={() => setActiveTab(tab)}>
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