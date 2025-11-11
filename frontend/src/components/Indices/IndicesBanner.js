import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

// --- Styled Components & Animations ---

const fadeIn = keyframes`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`;

const BannerContainer = styled.div`
  width: 100%;
  padding: 1.5rem 0;
  margin-bottom: 3rem;
  overflow: hidden; /* Important for the scrolling animation */
`;

const CardScroller = styled.div`
  display: flex;
  gap: 1rem;
  /* Allows horizontal scrolling on smaller screens or if there are many cards */
  overflow-x: auto;
  padding-bottom: 1rem; /* Space for the scrollbar */

  /* Hide scrollbar for a cleaner look, but keep functionality */
  &::-webkit-scrollbar {
    display: none;
  }
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
`;

const IndexCard = styled.div`
  flex-shrink: 0; /* Prevents cards from shrinking */
  width: 220px;
  padding: 1rem;
  background-color: var(--color-secondary);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  animation: ${fadeIn} 0.5s ease-out;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  }
`;

const IndexName = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-text-primary);
  white-space: nowrap;
`;

const IndexPrice = styled.div`
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0.5rem 0;
`;

const IndexChange = styled.div`
  font-size: 1rem;
  font-weight: 500;
  color: ${({ isPositive }) => (isPositive ? 'var(--color-success)' : 'var(--color-danger)')};
`;


// --- The React Component ---

const IndicesBanner = () => {
  const [indices, setIndices] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  // This is the core logic for fetching and auto-refreshing the data
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/indices/summary');
        setIndices(response.data);
      } catch (error) {
        console.error("Failed to fetch indices summary:", error);
      } finally {
        // Only set loading to false on the first fetch
        if (isLoading) {
            setIsLoading(false);
        }
      }
    };

    fetchData(); // Fetch immediately on component mount

    // --- The "Live Ticking" Polling ---
    // Set up an interval to re-fetch the data every 10 seconds
    const intervalId = setInterval(fetchData, 10000);

    // This is a cleanup function. React runs this when the component is unmounted
    // to prevent memory leaks by stopping the interval.
    return () => clearInterval(intervalId);
  }, [isLoading]); // Rerun effect if isLoading changes (though it won't)

  const handleCardClick = (symbol) => {
    // URL-encode the symbol to handle special characters like '^'
    const encodedSymbol = encodeURIComponent(symbol);
    // We will build this page in the next big step
    navigate(`/index/${encodedSymbol}`);
  };

  if (isLoading) {
    return <BannerContainer><p style={{ textAlign: 'center' }}>Loading market data...</p></BannerContainer>;
  }

  if (!indices || indices.length === 0) {
    return null; // Don't render anything if there's no data or an error
  }

  return (
    <BannerContainer>
      <CardScroller>
        {indices.map(index => {
          const isPositive = index.change >= 0;
          return (
            <IndexCard key={index.symbol} onClick={() => handleCardClick(index.symbol)}>
              <IndexName>{index.name}</IndexName>
              <IndexPrice>{index.price.toFixed(2)}</IndexPrice>
              <IndexChange isPositive={isPositive}>
                {isPositive ? '+' : ''}{index.change.toFixed(2)} ({isPositive ? '+' : ''}{index.percent_change.toFixed(2)}%)
              </IndexChange>
            </IndexCard>
          );
        })}
      </CardScroller>
    </BannerContainer>
  );
};

export default IndicesBanner;