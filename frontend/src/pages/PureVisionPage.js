import React, { useState } from 'react';
import styled, { keyframes } from 'styled-components';
import { useLocation, useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import { FaArrowLeft, FaRobot, FaBrain, FaDraftingCompass, FaChartArea } from 'react-icons/fa';

// --- STYLES ---
const fadeIn = keyframes`from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); }`;

const PageContainer = styled.div`
  padding: 2rem; max-width: 1400px; margin: 0 auto; animation: ${fadeIn} 0.5s ease-out;
`;

const BackBtn = styled.button`
  background: transparent; border: 1px solid var(--color-border); color: var(--color-text-secondary);
  padding: 8px 16px; border-radius: 20px; cursor: pointer; display: flex; align-items: center; gap: 8px;
  margin-bottom: 2rem; transition: all 0.2s;
  &:hover { border-color: var(--color-primary); color: #fff; }
`;

const Grid = styled.div`
  display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;
  @media (max-width: 1024px) { grid-template-columns: 1fr; }
`;

const ImageCard = styled.div`
  background: var(--color-secondary); border: 1px solid var(--color-border); border-radius: 16px;
  padding: 1rem; display: flex; align-items: center; justify-content: center;
  img { max-width: 100%; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
`;

const AnalysisBox = styled.div`
  background: linear-gradient(145deg, #161B22, #0D1117); border: 1px solid var(--color-primary);
  border-radius: 16px; padding: 2rem; box-shadow: 0 0 30px rgba(88, 166, 255, 0.1);
  white-space: pre-line; line-height: 1.8; color: #C9D1D9; font-size: 1rem;
  
  strong { color: #58A6FF; font-weight: 700; }
  h1, h2, h3 { color: #fff; margin-top: 1.5rem; margin-bottom: 0.5rem; font-size: 1.2rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem; }
`;

const Header = styled.h1`
  font-size: 2rem; margin-bottom: 0.5rem; background: linear-gradient(90deg, #fff, #888); 
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
`;

const PureVisionPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { analysis, image } = location.state || {};

  if (!analysis) return <PageContainer>Loading...</PageContainer>;

  return (
    <PageContainer>
      <BackBtn onClick={() => navigate('/')}><FaArrowLeft /> Command Center</BackBtn>
      
      <div style={{marginBottom: '2rem'}}>
          <Header><FaBrain style={{color:'#58A6FF', marginRight:'10px'}}/> Quantum Vision Analysis</Header>
          <p style={{color:'var(--color-text-secondary)'}}>Pure Mathematical & Geometric Breakdown. Zero External Data.</p>
      </div>

      <Grid>
        {/* Left: The Image */}
        <ImageCard>
           {image && <img src={image} alt="Analyzed Chart" />}
        </ImageCard>

        {/* Right: The AI Brain */}
        <AnalysisBox>
            <div style={{display:'flex', alignItems:'center', gap:'10px', marginBottom:'1rem', color:'#58A6FF'}}>
                <FaDraftingCompass /> <span>GEOMETRIC ENGINE OUTPUT</span>
            </div>
            {/* Simple Markdown-like parser */}
            {analysis.split('**').map((part, i) => 
                i % 2 === 1 ? <strong key={i}>{part}</strong> : part
            )}
        </AnalysisBox>
      </Grid>
    </PageContainer>
  );
};

export default PureVisionPage;