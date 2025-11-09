import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';
import Card from '../common/Card';
// --- THESE ARE THE CORRECTED IMPORT PATHS ---
// The PriceTarget and AnalystRating components are in the same folder, so './' is correct.
import PriceTarget from './PriceTarget';
import AnalystRating from './AnalystRating';

// --- Styled Components ---

const fadeIn = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

const ForecastGrid = styled.div`
  display: grid;
  grid-template-columns: 1.5fr 1fr; /* Make the left column wider */
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

// --- The Main Forecasts Component ---

const Forecasts = ({ symbol, quote, analystRatings, priceTarget, keyStats, news }) => {
  const [aiAnalysis, setAiAnalysis] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAiAnalysis = async () => {
      // Guard clause: Don't run if essential data is missing
      if (!symbol || !analystRatings || !priceTarget || !keyStats || !news || !quote) {
        setIsLoading(false);
        return;
      }
      
      setIsLoading(true);
      try {
        const payload = {
          companyName: quote.name || symbol, // Use symbol as a fallback for name
          analystRatings: analystRatings,
          priceTarget: priceTarget,
          keyStats: keyStats,
          newsHeadlines: news.map(n => n.title).slice(0, 10),
        };
        // Make the dedicated API call to our new AI endpoint
        const response = await axios.post(`/api/stocks/${symbol}/forecast-analysis`, payload);
        setAiAnalysis(response.data.analysis);
      } catch (error) {
        console.error("Failed to fetch AI forecast analysis:", error);
        setAiAnalysis("Could not generate AI-powered forecast analysis at this time.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchAiAnalysis();
  }, [symbol, quote, analystRatings, priceTarget, keyStats, news]); // Re-fetch if any data changes


  // Main render check
  if (!priceTarget || !analystRatings) {
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
          <PriceTarget consensus={priceTarget} quote={quote} />
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