import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';

// --- Imports for all our high-end components ---
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
import { useLocation } from 'react-router-dom';
import ChartAnalysis from '../components/StockDetailPage/ChartAnalysis';

// --- Styled Components for the page layout ---
const fadeIn = keyframes`from { opacity: 0; } to { opacity: 1; }`;
const StockDetailPageContainer = styled.div`padding: 2rem 3rem; max-width: 1800px; margin: 0 auto; animation: ${fadeIn} 0.5s ease-in;`;
const TabContentGrid = styled.div`display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; @media (max-width: 1200px) { grid-template-columns: 1fr; }`;
const LeftColumn = styled.div`display: flex; flex-direction: column; gap: 2rem;`;
const RightColumn = styled.div`display: flex; flex-direction: column; gap: 2rem;`;
const LoadingContainer = styled.div`display: flex; flex-direction: column; align-items: center; justify-content: center; height: 90vh; color: var(--color-primary); font-size: 1.5rem;`;
const ErrorContainer = styled(LoadingContainer)`color: var(--color-danger);`;
const BackButton = styled.button`background: none; border: 1px solid var(--color-border); color: var(--color-text-secondary); padding: 8px 16px; border-radius: 20px; cursor: pointer; font-size: 0.9rem; margin-bottom: 2rem; transition: all 0.2s ease; &:hover { background-color: var(--color-secondary); color: var(--color-text-primary); }`;

// --- The Final, Architecturally Correct Page Component ---
const StockDetailPage = () => {
  const { symbol } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const chartAnalysisData = location.state?.chartAnalysis;
  
  const [stockData, setStockData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // State for all our "lazy-loading" AI components is managed here in the parent.
  const [swotAnalysis, setSwotAnalysis] = useState('');
  const [isLoadingSwot, setIsLoadingSwot] = useState(true);
  const [philosophyAssessment, setPhilosophyAssessment] = useState('');
  const [canslimAssessment, setCanslimAssessment] = useState('');
  const [conclusion, setConclusion] = useState('');
  const [isLoadingPhilosophy, setIsLoadingPhilosophy] = useState(true);
  const [isLoadingCanslim, setIsLoadingCanslim] = useState(true);
  const [isLoadingConclusion, setIsLoadingConclusion] = useState(true);

  // This hook fetches the main, non-AI data once per stock.
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

  // This single, powerful hook handles all the separate, staggered AI data fetches.
  useEffect(() => {
    if (!stockData) return;

    // --- Define all our individual AI fetch functions ---
    const fetchSwotAnalysis = () => {
      if (!stockData.profile?.description) { setIsLoadingSwot(false); return Promise.resolve(); }
      setIsLoadingSwot(true);
      const payload = { companyName: stockData.profile.companyName, description: stockData.profile.description };
      return axios.post(`/api/stocks/${symbol}/swot`, payload)
        .then(res => setSwotAnalysis(res.data.swot_analysis))
        .catch(() => setSwotAnalysis("Could not generate SWOT analysis."))
        .finally(() => setIsLoadingSwot(false));
    };
    const fetchPhilosophyAssessment = () => {
      if (!stockData.profile || !stockData.key_metrics) { setIsLoadingPhilosophy(false); return Promise.resolve(); }
      setIsLoadingPhilosophy(true);
      const payload = { companyName: stockData.profile.companyName, keyMetrics: stockData.key_metrics };
      return axios.post(`/api/stocks/${symbol}/fundamental-analysis`, payload)
        .then(res => setPhilosophyAssessment(res.data.assessment))
        .catch(() => setPhilosophyAssessment("Could not generate AI assessment."))
        .finally(() => setIsLoadingPhilosophy(false));
    };
    const fetchCanslimAssessment = () => {
      if (!stockData.profile || !stockData.quote || !stockData.quarterly_income_statements) { setIsLoadingCanslim(false); return; }
      setIsLoadingCanslim(true);
      const payload = {
        companyName: stockData.profile.companyName, quote: stockData.quote, quarterlyEarnings: stockData.quarterly_income_statements,
        annualEarnings: stockData.annual_revenue_and_profit, institutionalHolders: stockData.shareholding.length,
      };
      return axios.post(`/api/stocks/${symbol}/canslim-analysis`, payload)
        .then(res => setCanslimAssessment(res.data.assessment))
        .catch(() => setCanslimAssessment("Could not generate CANSLIM assessment."))
        .finally(() => setIsLoadingCanslim(false));
    };
    const fetchConclusionAnalysis = (philosophyRes, canslimRes) => {
      if (!stockData.piotroski_f_score || !stockData.graham_scan || !stockData.darvas_scan) { setIsLoadingConclusion(false); return; }
      setIsLoadingConclusion(true);
      const payload = {
        companyName: stockData.profile.companyName, piotroskiData: stockData.piotroski_f_score,
        grahamData: stockData.graham_scan, darvasData: stockData.darvas_scan,
        canslimAssessment: canslimRes, philosophyAssessment: philosophyRes,
      };
      axios.post(`/api/stocks/${symbol}/conclusion-analysis`, payload)
        .then(res => setConclusion(res.data.conclusion))
        .catch(() => setConclusion("GRADE: N/A\nTHESIS: Could not generate AI conclusion."))
        .finally(() => setIsLoadingConclusion(false));
    };

    // --- Execute the calls in a logical chain ---
    // We run the first three in parallel.
    Promise.all([
      fetchSwotAnalysis(),
      fetchPhilosophyAssessment(),
      fetchCanslimAssessment()
    ]).then(() => {
      // The conclusion runs ONLY after the others have finished.
      // We use the state callback to get the most up-to-date values for the final call.
      setPhilosophyAssessment(currentPhilosophy => {
        setCanslimAssessment(currentCanslim => {
          setTimeout(() => fetchConclusionAnalysis(currentPhilosophy, currentCanslim), 200);
          return currentCanslim;
        });
        return currentPhilosophy;
      });
    });

  }, [stockData, symbol]);

  if (isLoading) { return <LoadingContainer><p>Loading Financial Universe for {symbol}...</p></LoadingContainer>; }
  if (error) { return (<ErrorContainer><h2>An Error Occurred</h2><p>{error}</p><BackButton onClick={() => navigate('/')}>Go Back</BackButton></ErrorContainer>); }
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
          <TabContentGrid>
            <LeftColumn>
              <TradingViewChart symbol={tradingViewSymbol} />
              <SwotAnalysis analysisText={swotAnalysis} isLoading={isLoadingSwot} />
            </LeftColumn>
            <RightColumn>
              <OverallSentiment sentimentData={stockData.overall_sentiment} />
              <NewsList newsArticles={stockData.news} />
            </RightColumn>
          </TabContentGrid>
        </TabPanel>
        <TabPanel label="Fundamentals">
            <Fundamentals
                piotroskiData={stockData.piotroski_f_score}
                darvasScanData={stockData.darvas_scan}
                grahamScanData={stockData.graham_scan}
                philosophyAssessment={philosophyAssessment}
                canslimAssessment={canslimAssessment}
                conclusion={conclusion}
                isLoadingPhilosophy={isLoadingPhilosophy}
                isLoadingCanslim={isLoadingCanslim}
                isLoadingConclusion={isLoadingConclusion}
                profile={stockData.profile}
            />
        </TabPanel>
        <TabPanel label="Financials">
          <Financials 
            profile={stockData.profile}
            keyStats={stockData.keyStats}
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
                news={stockData.news} currency={stockData.profile?.currency}
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