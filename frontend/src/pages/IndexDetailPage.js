import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';

// --- (Imports are unchanged) ---
import StockHeader from '../components/Header/StockHeader';
import Technicals from '../components/Technicals/Technicals';
import TradingViewChart from '../components/Chart/TradingViewChart';
import { Tabs, TabPanel } from '../components/common/Tabs/Tabs';

// --- (Styled Components are unchanged) ---
const fadeIn = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

const DetailPageContainer = styled.div`
  padding: 2rem 3rem;
  max-width: 1800px;
  margin: 0 auto;
  animation: ${fadeIn} 0.5s ease-in;
`;

const LoadingContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 90vh;
  color: var(--color-primary);
  font-size: 1.5rem;
`;

const ErrorContainer = styled(LoadingContainer)`
  color: var(--color-danger);
`;

const BackButton = styled.button`
  background: none;
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  margin-bottom: 2rem;
  transition: all 0.2s ease;
  &:hover {
    background-color: var(--color-secondary);
    color: var(--color-text-primary);
  }
`;

// --- The Updated React Component ---

const IndexDetailPage = () => {
  const { encodedSymbol } = useParams();
  const navigate = useNavigate();

  const [staticData, setStaticData] = useState(null);
  const [liveQuote, setLiveQuote] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const symbol = decodeURIComponent(encodedSymbol);

  useEffect(() => {
    const fetchIndexDetails = async () => {
      if (!encodedSymbol) return;
      setIsLoading(true);
      setError(null);
      try {
        const response = await axios.get(`/api/indices/${encodedSymbol}/details`);
        setStaticData(response.data);
        setLiveQuote(response.data.quote); 
      } catch (err) {
        console.error("Failed to fetch index details:", err);
        setError(`Could not retrieve data for ${symbol}. Please try again.`);
      } finally {
        setIsLoading(false);
      }
    };
    fetchIndexDetails();
  }, [encodedSymbol, symbol]);

  useEffect(() => {
    if (!staticData) return;
    const fetchLivePrice = async () => {
      try {
        const response = await axios.get(`/api/indices/${encodedSymbol}/live-price`);
        setLiveQuote(response.data);
      } catch (error) {
        console.error("Failed to fetch live index price:", error);
      }
    };
    fetchLivePrice();
    const intervalId = setInterval(fetchLivePrice, 10000);
    return () => clearInterval(intervalId);
  }, [staticData, encodedSymbol]);

  if (isLoading) {
    return <LoadingContainer><p>Loading market data for {symbol}...</p></LoadingContainer>;
  }

  if (error || !staticData) {
    return (
      <ErrorContainer>
        <h2>An Error Occurred</h2>
        <p>{error || `Could not retrieve data for ${symbol}.`}</p>
        <BackButton style={{ marginTop: '2rem' }} onClick={() => navigate('/')}>Go Back Home</BackButton>
      </ErrorContainer>
    );
  }

  // --- THIS IS THE CRITICAL FIX ---
  // We get the correct TradingView symbol from our new, intelligent profile object.
  // We use the original 'symbol' as a fallback, just in case.
  const tradingViewSymbol = staticData.profile?.tradingview_symbol || symbol;

  return (
    <DetailPageContainer>
      <BackButton onClick={() => navigate('/')}>
        &larr; Back to Home
      </BackButton>

      <StockHeader profile={staticData.profile} quote={liveQuote} />
      
      <Tabs>
        <TabPanel label="Overview">
            {/* We now pass the new, correct symbol to the chart */}
            <TradingViewChart symbol={tradingViewSymbol} />
        </TabPanel>
        
        <TabPanel label="Technicals">
            <Technicals
                analystRatings={staticData.analyst_ratings}
                technicalIndicators={staticData.technical_indicators}
            />
        </TabPanel>
      </Tabs>

    </DetailPageContainer>
  );
};

export default IndexDetailPage;