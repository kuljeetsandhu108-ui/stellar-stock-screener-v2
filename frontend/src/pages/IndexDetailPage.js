import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';
import { FaArrowLeft, FaGlobeAmericas, FaChartLine, FaExclamationTriangle } from 'react-icons/fa';

// --- COMPONENTS ---
import StockHeader from '../components/Header/StockHeader';
import CustomChart from '../components/Chart/CustomChart';
import IndexChartAnalysis from '../components/IndexDetailPage/IndexChartAnalysis';
import Technicals from '../components/Technicals/Technicals';
import Card from '../components/common/Card';

// --- CONFIGURATION ---
// Critical for Vercel deployment to find the Railway backend
const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

// --- ANIMATIONS ---
const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

const spin = keyframes`
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
`;

// --- STYLED COMPONENTS ---

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
    border-color: #EBCB8B; /* Gold Accent for Indices */
  }
`;

const DashboardGrid = styled.div`
  display: grid;
  /* If AI data exists (upload), split 50/50. Otherwise full width. */
  grid-template-columns: ${({ hasUpload }) => hasUpload ? '1fr 1fr' : '1fr'};
  gap: 2rem;
  
  @media (max-width: 1200px) {
    grid-template-columns: 1fr; /* Stack on smaller screens */
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

const Spinner = styled.div`
  border: 3px solid rgba(235, 203, 139, 0.3);
  border-top: 3px solid #EBCB8B;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: ${spin} 1s linear infinite;
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
  
  // Data State
  const aiAnalysisData = location.state?.chartAnalysis;
  const [indexData, setIndexData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // --- FETCH LIVE DATA ---
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        // Use the configured API URL
        const response = await axios.get(`${API_URL}/api/indices/${encodedSymbol}/details`);
        
        if (!response.data || !response.data.profile) {
            throw new Error("Incomplete data received");
        }
        
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
            <Spinner />
            <span>Loading Macro Data for {symbol}...</span>
        </LoadingContainer>
    );
  }

  if (error || !indexData) {
      return (
        <ErrorContainer>
            <FaExclamationTriangle size={50} />
            <p>{error || "Index Data Unavailable."}</p>
            <BackButton onClick={() => navigate('/')}>Return Home</BackButton>
        </ErrorContainer>
      );
  }

  // Destructure Data from Backend
  const { profile, quote, technical_indicators, moving_averages, pivot_points, analyst_ratings } = indexData;

  return (
    <PageContainer>
      <BackButton onClick={() => navigate('/')}>
        <FaArrowLeft /> Back to Command Center
      </BackButton>

      {/* 1. Header (Price, Name, Logo) */}
      <StockHeader profile={profile} quote={quote} />

      <DashboardGrid hasUpload={!!aiAnalysisData}>
        
        {/* --- LEFT PANEL: AI ANALYSIS (Only if uploaded) --- */}
        {aiAnalysisData && (
          <LeftPanel>
            <SectionHeader><FaGlobeAmericas /> Macro Analysis</SectionHeader>
            
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

          {/* B. Technical Dashboard */}
          {/* CRITICAL: Passing snake_case backend data to camelCase props */}
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