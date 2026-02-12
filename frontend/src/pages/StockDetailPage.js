import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';

// --- COMPONENTS ---
import StockHeader from '../components/Header/StockHeader';
import { Tabs, TabPanel } from '../components/common/Tabs/Tabs';
import CustomChart from '../components/Chart/CustomChart';
import SwotAnalysis from '../components/SWOT/SwotAnalysis';
import OverallSentiment from '../components/Sentiment/OverallSentiment';
import PriceLevels from '../components/Overview/PriceLevels';
import NewsList from '../components/News/NewsList';
import ChartAnalysis from '../components/StockDetailPage/ChartAnalysis';
import Fundamentals from '../components/Fundamentals/Fundamentals';
import Financials from '../components/Financials/Financials';
import Forecasts from '../components/Forecasts/Forecasts';
import PeersComparison from '../components/Peers/PeersComparison';
import Shareholding from '../components/Shareholding/Shareholding';
import Technicals from '../components/Technicals/Technicals';
import { FaArrowLeft } from 'react-icons/fa';

// --- CONFIGURATION ---
// This connects your Vercel Frontend to your Railway Backend
const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

// --- ANIMATIONS ---
const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

// --- STYLED COMPONENTS ---
const PageContainer = styled.div`
  padding: 2rem 3rem;
  max-width: 1800px;
  margin: 0 auto;
  animation: ${fadeIn} 0.4s ease-out;
  
  @media (max-width: 768px) {
    padding: 1rem;
  }
`;

const TabGrid = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr; /* Chart takes 66%, Info takes 33% */
  gap: 2rem;

  @media (max-width: 1200px) {
    grid-template-columns: 1fr; /* Stack on mobile */
  }
`;

const LeftCol = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const RightCol = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const LoadingBox = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 80vh;
  color: var(--color-primary);
  font-size: 1.2rem;
  font-weight: 500;
  gap: 1rem;
`;

const ErrorBox = styled(LoadingBox)`
  color: var(--color-danger);
`;

const BackBtn = styled.button`
  background: none;
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  margin-bottom: 2rem;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;

  &:hover {
    background-color: var(--color-secondary);
    color: var(--color-text-primary);
    border-color: var(--color-primary);
  }
`;

const StockDetailPage = () => {
  const { symbol } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  
  // Data passed from "Deep Scan" or "Chart Analysis" upload
  const chartAnalysisData = location.state?.chartAnalysis;
  const chartTechnicalData = location.state?.technicalData;

  // --- STATE ---
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // AI Analysis States
  const [swot, setSwot] = useState('');
  const [loadingSwot, setLoadingSwot] = useState(true);
  const [philosophy, setPhilosophy] = useState('');
  const [canslim, setCanslim] = useState('');
  const [conclusion, setConclusion] = useState('');
  const [loadingFundAI, setLoadingFundAI] = useState(true);

  // --- ASSET DETECTION ---
  const isCrypto = symbol.includes('.CC') || symbol.includes('BTC') || symbol.includes('ETH') || (symbol.includes('USD') && !symbol.includes('.'));
  const isIndex = symbol.includes('.INDX') || symbol.includes('^');
  const isCommodity = symbol.includes('GOLD') || symbol.includes('OIL') || symbol.includes('XAU') || symbol.includes('USO') || symbol.includes('CLUSD');
  
  // Logic: Stocks have financials. Crypto/Indices/Commodities do not.
  const isStock = !isCrypto && !isIndex && !isCommodity;

  // --- 1. MASTER DATA FETCH ---
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      // Reset AI states on symbol change
      setSwot(''); setPhilosophy(''); setCanslim(''); setConclusion('');
      
      try {
        // Use the Vercel-Compatible API_URL
        const res = await axios.get(`${API_URL}/api/stocks/${symbol}/all`);
        
        if (!res.data || !res.data.profile) {
            throw new Error("Incomplete Data");
        }
        setData(res.data);
      } catch (err) {
        console.error("Fetch Error:", err);
        setError("Unable to retrieve market data. Please try again.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [symbol]);

  // --- 2. AI HANDLERS (LAZY LOADING) ---
  
  // SWOT Analysis (Runs for everything)
  const fetchSwot = useCallback(() => {
      if (!data?.profile?.companyName) { 
          setLoadingSwot(false); 
          return; 
      }
      setLoadingSwot(true);
      
      const payload = { 
          companyName: data.profile.companyName, 
          description: data.profile.description || "Financial Asset"
      };
      
      axios.post(`${API_URL}/api/stocks/${symbol}/swot`, payload)
        .then(res => setSwot(res.data.swot_analysis))
        .catch(() => setSwot("Analysis currently unavailable."))
        .finally(() => setLoadingSwot(false));
  }, [data, symbol]);

  // Fundamental Analysis (Runs ONLY for Stocks)
  useEffect(() => {
    if (!data) return;

    // Trigger SWOT
    fetchSwot();

    if (isStock) {
        setLoadingFundAI(true);
        
        // Parallel Execution for Speed
        const req1 = axios.post(`${API_URL}/api/stocks/${symbol}/fundamental-analysis`, { 
            companyName: data.profile.companyName, 
            keyMetrics: data.key_metrics 
        }).then(r => setPhilosophy(r.data.assessment)).catch(() => setPhilosophy("N/A"));

        const req2 = axios.post(`${API_URL}/api/stocks/${symbol}/canslim-analysis`, {
            companyName: data.profile.companyName, 
            quote: data.quote, 
            quarterlyEarnings: data.quarterly_income_statements,
            annualEarnings: data.annual_revenue_and_profit, 
            institutionalHolders: data.shareholding ? data.shareholding.length : 0
        }).then(r => setCanslim(r.data.assessment)).catch(() => setCanslim("N/A"));

        const req3 = axios.post(`${API_URL}/api/stocks/${symbol}/conclusion-analysis`, {
            companyName: data.profile.companyName, 
            piotroskiData: data.piotroski_f_score,
            grahamData: data.graham_scan, 
            darvasData: data.darvas_scan,
            canslimAssessment: "Generated", 
            philosophyAssessment: "Generated",
            keyStats: data.keyStats,
            newsHeadlines: data.news ? data.news.slice(0, 5).map(n => n.title) : []
        }).then(r => setConclusion(r.data.conclusion)).catch(() => setConclusion("N/A"));

        Promise.allSettled([req1, req2, req3]).finally(() => setLoadingFundAI(false));
    } else {
        setLoadingFundAI(false); // Skip for non-stocks
    }
  }, [data, symbol, isStock, fetchSwot]);

  // --- RENDER STATES ---
  if (loading) return (
      <LoadingBox>
          <div className="spinner" />
          <p>Accessing Global Data Feeds...</p>
      </LoadingBox>
  );

  if (error || !data) return (
      <ErrorBox>
          <h2>Connection Interrupted</h2>
          <p>{error}</p>
          <BackBtn onClick={() => navigate('/')}><FaArrowLeft /> Return Home</BackBtn>
      </ErrorBox>
  );

  // --- MAIN RENDER ---
  return (
    <PageContainer>
      <BackBtn onClick={() => navigate('/')}><FaArrowLeft /> Back to Command Center</BackBtn>
      
      {/* 1. Header (Live Price & Broker Connect Button) */}
      <StockHeader profile={data.profile} quote={data.quote} />
      
      <Tabs>
        
        {/* Tab: Chart AI (Only if uploaded) */}
        {chartAnalysisData && (
          <TabPanel label="Chart Insight">
            <ChartAnalysis analysisData={chartAnalysisData} technicalData={chartTechnicalData} />
          </TabPanel>
        )}

        {/* Tab: Overview (The Main Dashboard) */}
        <TabPanel label="Overview">
          <TabGrid>
            <LeftCol>
              <CustomChart symbol={symbol} />
              <SwotAnalysis analysisText={swot} isLoading={loadingSwot} onRegenerate={fetchSwot} />
            </LeftCol>
            <RightCol>
              {isStock && <OverallSentiment sentimentData={data.overall_sentiment} />}
              <PriceLevels pivotPoints={data.pivot_points} quote={data.quote} profile={data.profile} />
              <NewsList newsArticles={data.news} />
            </RightCol>
          </TabGrid>
        </TabPanel>
        
        {/* Tab: Fundamentals (Stocks Only) */}
        {isStock && (
            <TabPanel label="Fundamentals">
                <Fundamentals
                    symbol={symbol} profile={data.profile} quote={data.quote} keyMetrics={data.key_metrics}
                    piotroskiData={data.piotroski_f_score} darvasScanData={data.darvas_scan}
                    grahamScanData={data.graham_scan} quarterlyEarnings={data.quarterly_income_statements}
                    annualEarnings={data.annual_revenue_and_profit} shareholding={data.shareholding}
                    delay={0} 
                    philosophyAssessment={philosophy} canslimAssessment={canslim} conclusion={conclusion}
                    isLoadingPhilosophy={loadingFundAI} isLoadingCanslim={loadingFundAI} isLoadingConclusion={loadingFundAI}
                />
            </TabPanel>
        )}

        {/* Tab: Financials (Stocks Only) */}
        {isStock && (
          <TabPanel label="Financials">
            <Financials 
              profile={data.profile} keyStats={data.keyStats}
              financialData={data.annual_revenue_and_profit} balanceSheetData={data.annual_balance_sheets}
              annualCashFlow={data.annual_cash_flow_statements} quarterlyIncome={data.quarterly_income_statements}
              quarterlyBalance={data.quarterly_balance_sheets} quarterlyCashFlow={data.quarterly_cash_flow_statements}
            />
          </TabPanel>
        )}
        
        {/* Tab: Forecasts (Universal) */}
        <TabPanel label="Forecasts">
            <Forecasts 
                symbol={symbol} quote={data.quote} analystRatings={data.analyst_ratings}
                priceTarget={data.price_target_consensus} keyStats={data.keyStats}
                news={data.news} delay={0} currency={data.profile?.currency}
            />
        </TabPanel>

        {/* Tab: Peers (Stocks Only) */}
        {isStock && (
            <TabPanel label="Peers">
                <PeersComparison symbol={symbol} />
            </TabPanel>
        )}
        
        {/* Tab: Shareholding (Stocks Only) */}
        {isStock && (
            <TabPanel label="Shareholding">
                <Shareholding 
                    shareholdingData={data.shareholding}
                    historicalStatements={data.annual_revenue_and_profit}
                    shareholdingBreakdown={data.shareholding_breakdown}
                />
            </TabPanel>
        )}
        
        {/* Tab: Technicals (Universal) */}
        <TabPanel label="Technicals">
            <Technicals 
              analystRatings={data.analyst_ratings} technicalIndicators={data.technical_indicators}
              movingAverages={data.moving_averages} pivotPoints={data.pivot_points}
              quote={data.quote}
            />
        </TabPanel>

      </Tabs>
    </PageContainer>
  );
};

export default StockDetailPage;