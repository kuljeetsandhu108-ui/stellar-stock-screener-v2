import React, { useMemo } from 'react';
import styled, { keyframes } from 'styled-components';
import Card from '../common/Card';
import { 
  FaGlobeAmericas, FaChartLine, FaShieldAlt, FaBullseye, 
  FaLayerGroup, FaArrowUp, FaArrowDown, FaExchangeAlt,
  FaCrosshairs, FaStopCircle, FaMoneyBillWave
} from 'react-icons/fa';

// --- STYLED COMPONENTS (Gold/Macro Theme) ---
const fadeIn = keyframes`from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); }`;

const AnalysisContainer = styled.div`display: flex; flex-direction: column; gap: 1.5rem; animation: ${fadeIn} 0.6s ease-out;`;

const MacroVerdictCard = styled(Card)`
  text-align: center; border-left: 4px solid #EBCB8B; 
  background: linear-gradient(145deg, rgba(235, 203, 139, 0.05), rgba(13, 17, 23, 1));
`;

const TrendDisplay = styled.div`
  display: flex; align-items: center; justify-content: center; gap: 1rem; font-size: 2rem; font-weight: 800; margin-bottom: 1rem; color: ${({ color }) => color}; text-transform: uppercase; letter-spacing: 1px;
`;

const MacroText = styled.p`font-size: 1.1rem; color: var(--color-text-primary); line-height: 1.8; font-style: italic; max-width: 90%; margin: 0 auto;`;

const GridSection = styled.div`display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; @media (max-width: 768px) { grid-template-columns: 1fr; }`;

const ZoneCard = styled.div`background: rgba(255, 255, 255, 0.03); border: 1px solid var(--color-border); border-radius: 12px; padding: 1.5rem; position: relative; overflow: hidden;`;
const ZoneTitle = styled.h4`color: #EBCB8B; font-size: 1rem; font-weight: 700; margin-bottom: 1rem; display: flex; align-items: center; gap: 8px;`;
const LevelList = styled.ul`list-style: none; padding: 0; margin: 0;`;
const LevelItem = styled.li`color: var(--color-text-secondary); margin-bottom: 0.8rem; display: flex; align-items: start; gap: 10px; line-height: 1.5; svg { color: #EBCB8B; margin-top: 4px; }`;

const StrategyBox = styled.div`
  background: linear-gradient(135deg, #161B22 0%, #0D1117 100%);
  border: 1px solid ${({ action }) => (action === 'BUY' ? '#238636' : action === 'SELL' ? '#DA3633' : '#8B949E')};
  border-radius: 16px; padding: 0; position: relative; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.3);
`;

const StrategyHeader = styled.div`display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 2rem; background: rgba(255,255,255,0.02); border-bottom: 1px solid rgba(255,255,255,0.05);`;

const DirectionBadge = styled.span`
  background: ${({ action }) => (action === 'BUY' ? 'rgba(57, 211, 83, 0.15)' : action === 'SELL' ? 'rgba(248, 81, 73, 0.15)' : 'rgba(139, 148, 158, 0.15)')};
  color: ${({ action }) => (action === 'BUY' ? '#3FB950' : action === 'SELL' ? '#F85149' : '#8B949E')};
  border: 1px solid ${({ action }) => (action === 'BUY' ? '#3FB950' : action === 'SELL' ? '#F85149' : '#8B949E')};
  padding: 0.5rem 1.5rem; border-radius: 8px; font-weight: 800; font-size: 1.1rem; letter-spacing: 1.5px;
`;

const MetricGrid = styled.div`display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px; background: rgba(255,255,255,0.05); @media (max-width: 768px) { grid-template-columns: 1fr 1fr; }`;
const MetricBox = styled.div`background: #0D1117; padding: 1.5rem; text-align: center; transition: background 0.2s; &:hover { background: #161B22; }`;
const MetricLabel = styled.div`font-size: 0.7rem; color: #8B949E; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 6px;`;
const MetricVal = styled.div`font-size: 1.25rem; font-weight: 700; font-family: 'Roboto Mono', monospace; color: ${({ color }) => color || '#C9D1D9'};`;

const RationaleBox = styled.div`padding: 1.5rem 2rem; background: rgba(235, 203, 139, 0.05); border-top: 1px solid rgba(235, 203, 139, 0.1); color: #C9D1D9; line-height: 1.6; font-size: 0.95rem;`;

// --- COMPONENT ---
const IndexChartAnalysis = ({ analysisData }) => {
  
  // --- PERFECT PARSER (Includes 0-9 for targets and \n fix) ---
  const parsed = useMemo(() => {
    if (!analysisData || typeof analysisData !== 'string') return null;
    
    const rawKeys =['TREND', 'PATTERNS', 'LEVELS', 'VOLUME', 'MOMENTUM', 'INDICATORS', 'CONCLUSION', 'ACTION', 'ENTRY_ZONE', 'STOP_LOSS', 'TARGET_1', 'TARGET_2', 'RISK_REWARD', 'CONFIDENCE', 'RATIONALE'];
    const sections = {};
    
    let text = "\n" + analysisData.replace(/\\\\n/g, '\n').replace(/\*\*/g, '').replace(/-- TRADE TICKET --/g, '');

    rawKeys.forEach(key => {
      const regex = new RegExp(`(?:^|\\n)\\s*${key}\\s*:\\s*([\\s\\S]*?)(?=\\n\\s*[A-Z0-9_]{3,}\\s*:|$)`, 'i');
      const match = text.match(regex);
      if (match) sections[key] = match[1].trim();
    });
    return sections;
  }, [analysisData]);

  if (!parsed) return null;

  const isBullish = parsed.TREND?.toLowerCase().includes('uptrend') || parsed.TREND?.toLowerCase().includes('bullish');
  const isBearish = parsed.TREND?.toLowerCase().includes('downtrend') || parsed.TREND?.toLowerCase().includes('bearish');
  
  const TrendIcon = isBullish ? FaArrowUp : isBearish ? FaArrowDown : FaExchangeAlt;
  const trendColor = isBullish ? '#3FB950' : isBearish ? '#F85149' : '#EBCB8B';
  const action = parsed.ACTION?.toUpperCase() || 'WAIT';

  return (
    <AnalysisContainer>
      <MacroVerdictCard>
        <div style={{color: '#EBCB8B', fontSize: '0.8rem', fontWeight: 600, marginBottom: '10px', textTransform: 'uppercase'}}>Quantitative Macro Outlook</div>
        <TrendDisplay color={trendColor}><TrendIcon /> {parsed.TREND || 'Consolidation'}</TrendDisplay>
        <MacroText>"{parsed.CONCLUSION || parsed.RATIONALE}"</MacroText>
      </MacroVerdictCard>

      {parsed.ENTRY_ZONE && (
        <StrategyBox action={action}>
            <StrategyHeader>
                <div>
                    <div style={{fontSize:'0.75rem', color:'#8B949E', letterSpacing:'1px', marginBottom:'5px'}}>STRATEGY SIGNAL</div>
                    <DirectionBadge action={action}>{action}</DirectionBadge>
                </div>
                <div style={{textAlign:'right'}}>
                    <div style={{fontSize:'0.75rem', color:'#8B949E', letterSpacing:'1px', marginBottom:'5px'}}>CONFIDENCE</div>
                    <div style={{fontSize:'1.5rem', fontWeight:'bold', color:'#C9D1D9'}}>{parsed.CONFIDENCE || 'High (Data-Driven)'}</div>
                </div>
            </StrategyHeader>
            
            <MetricGrid>
                <MetricBox>
                    <MetricLabel><FaCrosshairs /> Entry Zone</MetricLabel>
                    <MetricVal color="#58A6FF">{parsed.ENTRY_ZONE}</MetricVal>
                </MetricBox>
                <MetricBox>
                    <MetricLabel><FaStopCircle /> Stop Loss (SL)</MetricLabel>
                    <MetricVal color="#F85149">{parsed.STOP_LOSS}</MetricVal>
                </MetricBox>
                <MetricBox style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    <MetricLabel><FaMoneyBillWave /> Take Profit Targets</MetricLabel>
                    <div style={{display:'flex', justifyContent:'space-around', width: '100%', marginTop: '4px'}}>
                        <div style={{display:'flex', flexDirection:'column', alignItems:'center'}}>
                            <span style={{fontSize:'0.65rem', color:'#8B949E', fontWeight:'bold', letterSpacing:'1px'}}>T1 (1:1.5)</span>
                            <span style={{color:'#3FB950', fontWeight:'700', fontSize:'1.15rem', fontFamily:'Roboto Mono'}}>{parsed.TARGET_1}</span>
                        </div>
                        <div style={{width: '1px', backgroundColor: 'rgba(255,255,255,0.1)', height: '100%'}}></div>
                        <div style={{display:'flex', flexDirection:'column', alignItems:'center'}}>
                            <span style={{fontSize:'0.65rem', color:'#8B949E', fontWeight:'bold', letterSpacing:'1px'}}>T2 (1:3.0)</span>
                            <span style={{color:'#17C3B2', fontWeight:'700', fontSize:'1.15rem', fontFamily:'Roboto Mono'}}>{parsed.TARGET_2}</span>
                        </div>
                    </div>
                </MetricBox>
                <MetricBox>
                    <MetricLabel><FaChartLine /> Risk / Reward</MetricLabel>
                    <MetricVal color="#EBCB8B" style={{fontSize: '1.05rem'}}>{parsed.RISK_REWARD}</MetricVal>
                </MetricBox>
            </MetricGrid>
            
            <RationaleBox>
                <strong style={{color:'#EBCB8B', marginRight:'8px'}}>Mathematical Rationale:</strong> {parsed.RATIONALE}
            </RationaleBox>
        </StrategyBox>
      )}

      <GridSection>
        <ZoneCard>
          <ZoneTitle><FaShieldAlt /> Key Levels</ZoneTitle>
          <LevelList>
             <LevelItem><FaChartLine /> {parsed.LEVELS || 'Calculating Support/Resistance...'}</LevelItem>
             <LevelItem><FaBullseye /> Momentum: {parsed.MOMENTUM || 'Neutral'}</LevelItem>
          </LevelList>
        </ZoneCard>
        <ZoneCard>
          <ZoneTitle><FaLayerGroup /> Market Structure</ZoneTitle>
          <LevelList>
             <LevelItem><FaGlobeAmericas /> {parsed.PATTERNS || 'Algorithmic structural review.'}</LevelItem>
             {parsed.INDICATORS && <LevelItem><FaChartLine /> {parsed.INDICATORS}</LevelItem>}
          </LevelList>
        </ZoneCard>
      </GridSection>
    </AnalysisContainer>
  );
};

export default IndexChartAnalysis;
