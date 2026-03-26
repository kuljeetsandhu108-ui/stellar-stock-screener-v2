import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import GaugeChart from 'react-gauge-chart';
import Card from '../common/Card';
import axios from 'axios';
import { FaSync } from 'react-icons/fa';
import { calculateTechnicalSignal } from '../../utils/technical_calculator';

// --- STYLED COMPONENTS ---
const DashboardContainer = styled.div`display: flex; flex-direction: column; gap: 1.5rem;`;
const MainMeterWrapper = styled.div`display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 1rem;`;
const SubMetersGrid = styled.div`display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; @media (max-width: 768px) { grid-template-columns: 1fr; gap: 1.5rem; }`;
const SubMeterItem = styled.div`display: flex; flex-direction: column; align-items: center; background-color: var(--color-background); padding: 1rem; border-radius: 12px; border: 1px solid var(--color-border); box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.2s ease, border-color 0.2s ease; position: relative; overflow: hidden; &:hover { transform: translateY(-2px); border-color: var(--color-primary); }`;
const MeterHeader = styled.div`display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 0.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.05);`;
const MeterTitle = styled.h4`font-size: 0.8rem; font-weight: 600; color: var(--color-text-secondary); text-transform: uppercase; letter-spacing: 0.5px; margin: 0;`;
const TimeframeSelect = styled.select`background: rgba(255,255,255,0.1); border: 1px solid transparent; border-radius: 4px; color: var(--color-text-primary); font-size: 0.7rem; padding: 2px 6px; cursor: pointer; outline: none; font-weight: 600; transition: all 0.2s; &:hover { background: var(--color-primary); color: white; } &:focus { border-color: var(--color-primary); } option { background: #1C2128; color: white; }`;
const VerdictText = styled.div`font-size: 1.8rem; font-weight: 800; text-align: center; margin-top: -30px; color: ${({ color }) => color}; text-shadow: 0 0 15px ${({ color }) => color}44;`;
const SubVerdictText = styled.div`font-size: 1.1rem; font-weight: 700; text-align: center; margin-top: -15px; color: ${({ color }) => color};`;
const ScoreText = styled.div`font-size: 0.85rem; font-weight: 500; text-align: center; color: var(--color-text-secondary); margin-top: 5px;`;
const LoadingOverlay = styled.div`position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(13, 17, 23, 0.85); display: flex; flex-direction: column; align-items: center; justify-content: center; border-radius: 12px; z-index: 10; color: var(--color-primary); font-size: 1.5rem; backdrop-filter: blur(2px); @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } } svg { animation: spin 1s linear infinite; margin-bottom: 0.5rem; } span { font-size: 0.8rem; font-weight: 600; color: var(--color-text-primary); }`;

const getColor = (score) => { if (score >= 75) return 'var(--color-success)'; if (score >= 60) return '#34D399'; if (score <= 25) return 'var(--color-danger)'; if (score <= 40) return '#F87171'; return '#EDBB5A'; };

const CustomGauge = ({ id, score, label, size = "small" }) => {
  const color = getColor(score);
  const percent = Math.min(Math.max(score / 100, 0), 1); 
  return (
    <div style={{ width: '100%', maxWidth: size === 'large' ? '350px' : '200px' }}>
      <GaugeChart id={id} nrOfLevels={20} colors={['#F85149', '#F88149', '#EDBB5A', '#3FB950', '#17C3B2']} percent={percent} arcPadding={0.02} cornerRadius={3} textColor={'transparent'} needleBaseColor={'#FFFFFF'} needleColor={'#C9D1D9'} animate={true} animDelay={0} animateDuration={800} style={{ width: '100%' }} />
      {size === 'large' ? <VerdictText color={color}>{label}</VerdictText> : <SubVerdictText color={color}>{label}</SubVerdictText>}
      <ScoreText>{score.toFixed(0)} / 100</ScoreText>
    </div>
  );
};

const OverallSentiment = ({ sentimentData, initialTechs, initialMAs, quote, symbol }) => {
  const[techTimeframe, setTechTimeframe] = useState('1d'); 
  const [techData, setTechData] = useState({ technicalIndicators: initialTechs, movingAverages: initialMAs });
  const [isUpdating, setIsUpdating] = useState(false);
  const[livePrice, setLivePrice] = useState(quote?.price || null);

  useEffect(() => {
    const handleTick = (e) => setLivePrice(e.detail.price);
    window.addEventListener('livePriceTick', handleTick);
    return () => window.removeEventListener('livePriceTick', handleTick);
  },[]);

  const handleTimeframeChange = async (e) => {
    const newTf = e.target.value;
    setTechTimeframe(newTf);
    setIsUpdating(true);
    try {
      // Fetch full raw metrics instead of a basic score so we can run identical logic
      const response = await axios.post(`/api/stocks/${symbol}/technicals-data`, { timeframe: newTf });
      if (response.data && response.data.technicalIndicators) {
          setTechData(response.data);
      }
    } catch (err) { console.error("Failed to update technical data", err); } finally { setIsUpdating(false); }
  };

  if (!sentimentData) return <Card title="Confidence Matrix"><p style={{color: 'var(--color-text-secondary)', padding: '1rem', textAlign: 'center'}}>Calculating market sentiment...</p></Card>;

  const bd = sentimentData.breakdown || { fundamental: { score: 50, label: '--' }, financial: { score: 50, label: '--' }, analyst: { score: 50, label: '--' } };

  // 🚀 UNIFIED REAL-TIME MATH ENGINE
  const currentPrice = livePrice || quote?.price;
  const techSignal = calculateTechnicalSignal(techData.technicalIndicators, techData.movingAverages, currentPrice);

  // 🚀 DYNAMIC OVERALL SCORE
  const dynamicOverallScore = (bd.fundamental.score + bd.financial.score + bd.analyst.score + techSignal.sentiment) / 4;
  
  let dynamicVerdict = "Neutral";
  if (dynamicOverallScore >= 75) dynamicVerdict = "Strong Buy";
  else if (dynamicOverallScore >= 60) dynamicVerdict = "Buy";
  else if (dynamicOverallScore <= 25) dynamicVerdict = "Strong Sell";
  else if (dynamicOverallScore <= 40) dynamicVerdict = "Sell";

  return (
    <Card title="Confidence Matrix">
      <DashboardContainer>
        <MainMeterWrapper>
          <MeterTitle style={{fontSize: '1rem', marginBottom: '1rem', opacity: 0.8}}>Overall Health Score</MeterTitle>
          <CustomGauge id="overall-gauge" score={dynamicOverallScore} label={dynamicVerdict} size="large" />
        </MainMeterWrapper>
        <SubMetersGrid>
          <SubMeterItem>
            {isUpdating && (<LoadingOverlay><FaSync /><span>Analyzing...</span></LoadingOverlay>)}
            <MeterHeader>
                <MeterTitle>Technical</MeterTitle>
                <TimeframeSelect value={techTimeframe} onChange={handleTimeframeChange}>
                    <option value="15m">15M</option><option value="1h">1H</option><option value="4h">4H</option><option value="1d">1D</option><option value="1wk">1W</option>
                </TimeframeSelect>
            </MeterHeader>
            <CustomGauge id="tech-gauge" score={techSignal.sentiment} label={techSignal.verdict} />
          </SubMeterItem>
          <SubMeterItem>
            <MeterHeader><MeterTitle>Financial</MeterTitle></MeterHeader>
            <CustomGauge id="fin-gauge" score={bd.financial.score} label={bd.financial.label} />
          </SubMeterItem>
          <SubMeterItem>
            <MeterHeader><MeterTitle>Fundamental</MeterTitle></MeterHeader>
            <CustomGauge id="fund-gauge" score={bd.fundamental.score} label={bd.fundamental.label} />
          </SubMeterItem>
        </SubMetersGrid>
      </DashboardContainer>
    </Card>
  );
};
export default OverallSentiment;
