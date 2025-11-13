import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';
import Card from '../common/Card';
import PriceTarget from './PriceTarget';
import AnalystRating from './AnalystRating';

// --- Styled Components ---

const fadeIn = keyframes`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`;

const ForecastGrid = styled.div`
  display: grid;
  grid-template-columns: 1.5fr 1fr; /* Make the left column (Price Target) wider */
  gap: 3rem;

  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
  }
`;

const LeftColumn = styled.div``;
const RightColumn = styled.div``;

const AiAnalysisContainer = styled.div`
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid var(--color-border);
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--color-text-primary);
`;

const AiSummaryText = styled.p`
  font-size: 1rem;
  color: var(--color-text-secondary);
  line-height: 1.8;
  white-space: pre-wrap; /* Respects newlines from the AI's response */
  animation: ${fadeIn} 0.5s ease-in;
`;

const Loader = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 150px;
  color: var(--color-primary);
`;

// --- The Upgraded React Component ---

// The component now accepts the 'currency' prop to pass down to its children.
const Forecasts = ({ symbol, quote, analystRatings, priceTarget, keyStats, news, currency, delay }) => {
  const [aiAnalysis, setAiAnalysis] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAiAnalysis = async () => {
      // Guard clause to ensure all necessary data is present before making the API call.
      if (!symbol || !analystRatings || !priceTarget || !keyStats || !news || !quote) {
        setIsLoading(false);
        return;
      }
      
      setIsLoading(true);
      try {
        const payload = {
          companyName: quote.name || symbol,
          analystRatings: analystRatings,
          priceTarget: priceTarget,
          keyStats: keyStats,
          newsHeadlines: news.map(n => n.title).slice(0, 10),
        };
        const response = await axios.post(`/api/stocks/${symbol}/forecast-analysis`, payload);
        setAiAnalysis(response.data.analysis);
      } catch (error) {
        console.error("Failed to fetch AI forecast analysis:", error);
        setAiAnalysis("Could not generate AI-powered forecast analysis at this time.");
      } finally {
        setIsLoading(false);
      }
    };

    // Use a setTimeout to stagger this lazy-loaded API call.
    const timer = setTimeout(() => {
        fetchAiAnalysis();
    }, delay || 0);

    // Cleanup function to prevent memory leaks.
    return () => clearTimeout(timer);
  }, [symbol, quote, analystRatings, priceTarget, keyStats, news, delay]); // Dependency array


  // Main render check: if there's no analyst or price target data, show a clear message.
  if (!priceTarget || !analystRatings || Object.keys(priceTarget).length === 0) {
    return (
      <Card>
        <p>Forecast data is not available for this stock.</p>
      </Card>
    );
  }

  return (
    <Card>
      <ForecastGrid>
        <LeftColumn>
          {/* We now pass the 'currency' prop down to the PriceTarget component */}
          <PriceTarget consensus={priceTarget} quote={quote} currency={currency} />
        </LeftColumn>
        <RightColumn>
          <AnalystRating ratingsData={analystRatings} />
        </RightColumn>
      </ForecastGrid>

      <AiAnalysisContainer>
        <SectionTitle>AI-Powered Analysis</SectionTitle>
        {isLoading ? (
          <Loader>Generating AI summary...</Loader>
        ) : (
          <AiSummaryText>{aiAnalysis}</AiSummaryText>
        )}
      </AiAnalysisContainer>
    </Card>
  );
};

export default Forecasts;