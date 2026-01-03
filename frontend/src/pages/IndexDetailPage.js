import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';
import { FaArrowLeft, FaGlobeAmericas, FaChartLine } from 'react-icons/fa';

// --- COMPONENT IMPORTS ---
import StockHeader from '../components/Header/StockHeader';
import CustomChart from '../components/Chart/CustomChart';
import IndexChartAnalysis from '../components/IndexDetailPage/IndexChartAnalysis';
import Technicals from '../components/Technicals/Technicals';
import Card from '../components/common/Card';

// --- STYLED COMPONENTS ---

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

const PageContainer = styled.div`
  padding: 2rem 3rem;
  max-width: 1800px;
  margin: 0 auto;
  animation: ${fadeIn} 0.5s ease-in;
  
  @media (max-width: 768px) {
    padding: 1rem;
  }
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
  display: flex;
  align-items: center;
  gap: 0.5rem;

  &:hover {
    background-color: var(--color-secondary);
    color: var(--color-text-primary);
    border-color: #EBCB8B; /* Gold accent for Indices */
  }
`;

const DashboardGrid = styled.div`
  display: grid;
  /* If AI data exists: 50/50 split. If not: Full width (1fr) */
  grid-template-columns: ${({ hasUpload }) => hasUpload ? '1fr 1fr' : '1fr'};
  gap: 2rem;
  
  @media (max-width: 1200px) {
    grid-template-columns: 1fr; /* Always stack on smaller screens */
  }
`;

const LeftPanel = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const RightPanel = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const SectionHeader = styled.h2`
  font-size: 1.5rem;
  color: #EBCB8B; /* Gold Theme */
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid rgba(235, 203, 139, 0.2);
  padding-bottom: 0.5rem;
`;

const LoadingContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 80vh;
  color: #EBCB8B;
  font-size: 1.5rem;
  gap: 1rem;
`;

const ErrorContainer = styled(LoadingContainer)`
  color: #F85149;
`;

// --- MAIN COMPONENT ---

const IndexDetailPage = () => {
  const { encodedSymbol } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const symbol = decodeURIComponent(encodedSymbol);
  
  // 1. Check for Uploaded Analysis Data
  const aiAnalysisData = location.state?.chartAnalysis;

  // 2. Local State for Live Data
  const [indexData, setIndexData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // --- FETCH LIVE DATA ---
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        // This endpoint now calculates MAs and Pivots (from previous update)
        const response = await axios.get(`/api/indices/${encodedSymbol}/details`);
        setIndexData(response.data);
      } catch (err) {
        console.error("Index fetch error:", err);
        setError("Could not retrieve Global Market Data.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [encodedSymbol]);

  // --- RENDER STATES ---

  if (loading) {
    return (
        <LoadingContainer>
            <div className="spinner" style={{borderColor: '#EBCB8B', borderTopColor: 'transparent'}} />
            Loading Macro Data for {symbol}...
        </LoadingContainer>
    );
  }

  if (error || !indexData) {
      return (
        <ErrorContainer>
            {error || "Index Data Unavailable."}
            <BackButton onClick={() => navigate('/')}>Return Home</BackButton>
        </ErrorContainer>
      );
  }

  // Destructure the rich data from backend
  const { profile, quote, technical_indicators, moving_averages, pivot_points, analyst_ratings } = indexData;

  return (
    <PageContainer>
      <BackButton onClick={() => navigate('/')}>
        <FaArrowLeft /> Back to Command Center
      </BackButton>

      {/* 1. Header (Gold Themed via logic in StockHeader or generic style) */}
      <StockHeader profile={profile} quote={quote} />

      <DashboardGrid hasUpload={!!aiAnalysisData}>
        
        {/* --- LEFT PANEL: AI ANALYSIS (Only visible if User uploaded a chart) --- */}
        {aiAnalysisData && (
          <LeftPanel>
            <SectionHeader><FaGlobeAmericas /> AI Macro Analysis</SectionHeader>
            
            {/* The Gold-Themed AI Card */}
            <IndexChartAnalysis analysisData={aiAnalysisData} />
            
            <Card title="Context">
                 <p style={{color:'var(--color-text-secondary)', lineHeight: '1.6'}}>
                    This analysis is based on the technical structure provided in your uploaded chart. 
                    Compare this with the live market data on the right for maximum confluence.
                 </p>
            </Card>
          </LeftPanel>
        )}

        {/* --- RIGHT PANEL: LIVE MARKET DATA --- */}
        <RightPanel>
          <SectionHeader><FaChartLine /> Live Market Data</SectionHeader>
          
          {/* A. Live Interactive Chart */}
          <CustomChart symbol={symbol} />

          {/* B. Technical Dashboard (Now fully populated) */}
          {/* We pass 'quote' so it can calculate Price > SMA signals */}
          <Technicals 
             technicalIndicators={technical_indicators}
             movingAverages={moving_averages} 
             pivotPoints={pivot_points}
             analystRatings={analyst_ratings}
             quote={quote}
          />
        </RightPanel>

      </DashboardGrid>

    </PageContainer>
  );
};

export default IndexDetailPage;