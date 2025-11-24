import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import styled, { keyframes, css } from 'styled-components';
import axios from 'axios';
// We need icons for the slider arrows
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa';

import StockHeader from '../components/Header/StockHeader';
import Financials from '../components/Financials/Financials';
import Shareholding from '../components/Shareholding/Shareholding';
import Technicals from '../components/Technicals/Technicals';
import TradingViewChart from '../components/Chart/TradingViewChart';
import SwotAnalysis from '../components/SWOT/SwotAnalysis';
import NewsList from '../components/News/NewsList';
import { Tabs, TabPanel } from '../components/common/Tabs/Tabs';
import Forecasts from '../components/Forecasts/Forecasts';
import Fundamentals from '../components/Fundamentals/Fundamentals';
import OverallSentiment from '../components/Sentiment/OverallSentiment';
import PeersComparison from '../components/Peers/PeersComparison';
import ChartAnalysis from '../components/StockDetailPage/ChartAnalysis';

// --- Styled Components ---

const fadeIn = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

const StockDetailPageContainer = styled.div`
  padding: 2rem 3rem;
  max-width: 1800px;
  margin: 0 auto;
  animation: ${fadeIn} 0.5s ease-in;
  position: relative; /* Needed for arrow positioning */

  @media (max-width: 768px) {
    padding: 1rem;
  }
`;

// --- THE NEW SLIDER CONTAINER ---
const SliderContainer = styled.div`
  position: relative;
  width: 100%;
`;

const TabContentGrid = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;

  /* Mobile Slider Logic */
  @media (max-width: 1200px) {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory; /* Forces the scroll to lock on items */
    scroll-behavior: smooth;
    gap: 0; /* We remove gap and use padding inside columns for separation */
    
    /* Hide scrollbar for a cleaner look */
    scrollbar-width: none; 
    &::-webkit-scrollbar { 
      display: none; 
    }
  }
`;

// Shared styles for columns to make them act as slides on mobile
const MobileSlideStyles = css`
  @media (max-width: 1200px) {
    min-width: 100%; /* Takes up full width of the screen */
    scroll-snap-align: center; /* Locks to the center */
    padding: 0 5px; /* Small padding so content doesn't touch edges */
  }
`;

const LeftColumn = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
  ${MobileSlideStyles}
`;

const RightColumn = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
  ${MobileSlideStyles}
`;

// --- NAVIGATION ARROWS (Mobile Only) ---
const NavButton = styled.button`
  display: none; /* Hidden on desktop */
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(22, 27, 34, 0.8); /* Semi-transparent dark background */
  border: 1px solid var(--color-border);
  color: var(--color-primary);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  box-shadow: 0 4px 10px rgba(0,0,0,0.5);
  backdrop-filter: blur(4px);
  transition: all 0.2s ease;

  &:active {
    transform: translateY(-50%) scale(0.9);
  }

  @media (max-width: 1200px) {
    display: flex;
  }
`;

const PrevButton = styled(NavButton)`
  left: -10px;
`;

const NextButton = styled(NavButton)`
  right: -10px;
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

// --- The Final, Architecturally Correct Page Component ---

const StockDetailPage = () => {
  const { symbol } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const chartAnalysisData = location.state?.chartAnalysis;
  
  // Ref for our slider container to control scrolling
  const sliderRef = useRef(null);

  const [stockData, setStockData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // AI State
  const [swotAnalysis, setSwotAnalysis] = useState('');
  const [isLoadingSwot, setIsLoadingSwot] = useState(true);
  const [philosophyAssessment, setPhilosophyAssessment] = useState('');
  const [canslimAssessment, setCanslimAssessment] = useState('');
  const [conclusion, setConclusion] = useState('');
  const [isLoadingPhilosophy, setIsLoadingPhilosophy] = useState(true);
  const [isLoadingCanslim, setIsLoadingCanslim] = useState(true);
  const [isLoadingConclusion, setIsLoadingConclusion] = useState(true);

  useEffect(() => {
    const fetchAllData = async () => {
      setIsLoading(true);
      setError(null);
      setSwotAnalysis(''); setPhilosophyAssessment(''); setCanslimAssessment(''); setConclusion('');
      try {
        const response = await axios.get(`/api/stocks/${symbol}/all`);
        setStockData(response.data);
      } catch (err) {
        console.error("Failed to fetch stock data:", err);
        setError(`Could not retrieve data for ${symbol}. Please check the symbol and try again.`);
      } finally {
        setIsLoading(false);
      }
    };
    fetchAllData();
  }, [symbol]);

  // --- REPLACED AI FETCHING LOGIC ---
  useEffect(() => {
    if (!stockData) return;

    // 1. SWOT Analysis
    const fetchSwot = () => {
        if (!stockData.profile?.description) { setIsLoadingSwot(false); return; }
        setIsLoadingSwot(true);
        const payload = { companyName: stockData.profile.companyName, description: stockData.profile.description };
        axios.post(`/api/stocks/${symbol}/swot`, payload)
             .then(res => setSwotAnalysis(res.data.swot_analysis))
             .catch(() => setSwotAnalysis("Analysis unavailable."))
             .finally(() => setIsLoadingSwot(false));
    };

    // 2. Philosophy Assessment
    const fetchPhilosophy = () => {
        if (!stockData.profile || !stockData.key_metrics) { setIsLoadingPhilosophy(false); return; }
        setIsLoadingPhilosophy(true);
        const payload = { companyName: stockData.profile.companyName, keyMetrics: stockData.key_metrics };
        axios.post(`/api/stocks/${symbol}/fundamental-analysis`, payload)
             .then(res => setPhilosophyAssessment(res.data.assessment))
             .catch(() => setPhilosophyAssessment("Analysis unavailable."))
             .finally(() => setIsLoadingPhilosophy(false));
    };

    // 3. CANSLIM Assessment
    const fetchCanslim = () => {
        if (!stockData.profile || !stockData.quote || !stockData.quarterly_income_statements) { setIsLoadingCanslim(false); return; }
        setIsLoadingCanslim(true);
        const payload = {
            companyName: stockData.profile.companyName, quote: stockData.quote, quarterlyEarnings: stockData.quarterly_income_statements,
            annualEarnings: stockData.annual_revenue_and_profit, institutionalHolders: stockData.shareholding.length,
        };
        axios.post(`/api/stocks/${symbol}/canslim-analysis`, payload)
             .then(res => setCanslimAssessment(res.data.assessment))
             .catch(() => setCanslimAssessment("Analysis unavailable."))
             .finally(() => setIsLoadingCanslim(false));
    };

    // 4. Conclusion Analysis (NOW INDEPENDENT!)
    // It no longer waits for the others. It just needs the hard data we already have.
    const fetchConclusion = () => {
        if (!stockData.piotroski_f_score || !stockData.graham_scan || !stockData.keyStats) { setIsLoadingConclusion(false); return; }
        setIsLoadingConclusion(true);
        const payload = {
            companyName: stockData.profile.companyName,
            piotroskiData: stockData.piotroski_f_score,
            grahamData: stockData.graham_scan,
            darvasData: stockData.darvas_scan,
            keyStats: stockData.keyStats, // Sending raw stats
            newsHeadlines: stockData.news ? stockData.news.slice(0, 3).map(n => n.title) : [] // Sending headlines
        };
        axios.post(`/api/stocks/${symbol}/conclusion-analysis`, payload)
             .then(res => setConclusion(res.data.conclusion))
             .catch(() => setConclusion("GRADE: N/A\nTHESIS: Analysis unavailable."))
             .finally(() => setIsLoadingConclusion(false));
    };

    // Stagger them slightly to be nice to the API, but they don't depend on each other.
    const t1 = setTimeout(fetchSwot, 100);
    const t2 = setTimeout(fetchPhilosophy, 400);
    const t3 = setTimeout(fetchCanslim, 700);
    const t4 = setTimeout(fetchConclusion, 1000); // Runs 1 second after page load

    return () => { clearTimeout(t1); clearTimeout(t2); clearTimeout(t3); clearTimeout(t4); };
  }, [stockData, symbol]);

  // --- Functions to handle slider navigation ---
  const scrollLeft = () => {
    if (sliderRef.current) {
      // Scroll width of container to go to previous slide
      sliderRef.current.scrollBy({ left: -sliderRef.current.offsetWidth, behavior: 'smooth' });
    }
  };

  const scrollRight = () => {
    if (sliderRef.current) {
      // Scroll width of container to go to next slide
      sliderRef.current.scrollBy({ left: sliderRef.current.offsetWidth, behavior: 'smooth' });
    }
  };

  if (isLoading) {
    return ( <LoadingContainer><p>Loading Financial Universe for {symbol}...</p></LoadingContainer> );
  }

  if (error) {
    return ( <ErrorContainer><h2>An Error Occurred</h2><p>{error}</p><BackButton style={{ marginTop: '2rem' }} onClick={() => navigate('/')}>Go Back to Search</BackButton></ErrorContainer> );
  }

  if (!stockData) { return null; }

  const tradingViewSymbol = stockData.profile?.tradingview_symbol || symbol;

  return (
    <StockDetailPageContainer>
      <BackButton onClick={() => navigate('/')}>&larr; Back to Search</BackButton>
      
      <StockHeader profile={stockData.profile} quote={stockData.quote} />
      
      <Tabs>
        {chartAnalysisData && (
          <TabPanel label="Chart AI">
            <ChartAnalysis analysisData={chartAnalysisData} />
          </TabPanel>
        )}
        <TabPanel label="Overview">
          {/* --- THE NEW SLIDER LAYOUT --- */}
          <SliderContainer>
             {/* Arrows are hidden on desktop via CSS, visible on mobile */}
            <PrevButton onClick={scrollLeft}><FaChevronLeft /></PrevButton>
            
            <TabContentGrid ref={sliderRef}>
              <LeftColumn>
                <TradingViewChart symbol={tradingViewSymbol} />
                <SwotAnalysis analysisText={swotAnalysis} isLoading={isLoadingSwot} />
              </LeftColumn>
              
              <RightColumn>
                <OverallSentiment sentimentData={stockData.overall_sentiment} />
                <NewsList newsArticles={stockData.news} />
              </RightColumn>
            </TabContentGrid>
            
            <NextButton onClick={scrollRight}><FaChevronRight /></NextButton>
          </SliderContainer>
        </TabPanel>
        
        <TabPanel label="Fundamentals">
            <Fundamentals
                symbol={symbol} profile={stockData.profile} quote={stockData.quote}
                keyMetrics={stockData.key_metrics} piotroskiData={stockData.piotroski_f_score}
                darvasScanData={stockData.darvas_scan} grahamScanData={stockData.graham_scan}
                quarterlyEarnings={stockData.quarterly_income_statements}
                annualEarnings={stockData.annual_revenue_and_profit}
                shareholding={stockData.shareholding} delay={300}
                philosophyAssessment={philosophyAssessment} canslimAssessment={canslimAssessment}
                conclusion={conclusion}
                isLoadingPhilosophy={isLoadingPhilosophy} isLoadingCanslim={isLoadingCanslim}
                isLoadingConclusion={isLoadingConclusion}
            />
        </TabPanel>

        <TabPanel label="Financials">
          <Financials 
            profile={stockData.profile} keyStats={stockData.keyStats}
            financialData={stockData.annual_revenue_and_profit} 
            balanceSheetData={stockData.annual_balance_sheets}
            annualCashFlow={stockData.annual_cash_flow_statements}
            quarterlyIncome={stockData.quarterly_income_statements}
            quarterlyBalance={stockData.quarterly_balance_sheets}
            quarterlyCashFlow={stockData.quarterly_cash_flow_statements}
          />
        </TabPanel>
        
        <TabPanel label="Forecasts">
            <Forecasts 
                symbol={symbol} quote={stockData.quote} analystRatings={stockData.analyst_ratings}
                priceTarget={stockData.price_target_consensus} keyStats={stockData.keyStats}
                news={stockData.news} currency={stockData.profile?.currency} delay={200}
            />
        </TabPanel>

        <TabPanel label="Peers">
            <PeersComparison symbol={symbol} />
        </TabPanel>
        
        <TabPanel label="Shareholding">
            <Shareholding 
                shareholdingData={stockData.shareholding}
                historicalStatements={stockData.annual_revenue_and_profit}
                shareholdingBreakdown={stockData.shareholding_breakdown}
            />
        </TabPanel>
        
        <TabPanel label="Technicals">
            <Technicals 
              analystRatings={stockData.analyst_ratings} 
              technicalIndicators={stockData.technical_indicators}
              movingAverages={stockData.moving_averages}
              pivotPoints={stockData.pivot_points}
            />
        </TabPanel>
      </Tabs>
    </StockDetailPageContainer>
  );
};

export default StockDetailPage;