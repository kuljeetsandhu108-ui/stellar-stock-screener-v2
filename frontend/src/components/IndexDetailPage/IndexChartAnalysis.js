import React, { useMemo } from 'react';
import styled, { keyframes } from 'styled-components';
import Card from '../common/Card';
import { 
  FaGlobeAmericas, FaChartLine, FaShieldAlt, FaBullseye, 
  FaExclamationTriangle, FaLayerGroup, FaArrowUp, FaArrowDown, FaExchangeAlt 
} from 'react-icons/fa';

// --- STYLED COMPONENTS (Gold/Macro Theme) ---

const fadeIn = keyframes`from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); }`;

const AnalysisContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  animation: ${fadeIn} 0.6s ease-out;
`;

const MacroVerdictCard = styled(Card)`
  text-align: center;
  border-left: 4px solid #EBCB8B; /* Gold Border */
  background: linear-gradient(145deg, rgba(235, 203, 139, 0.05), rgba(13, 17, 23, 1));
`;

const TrendDisplay = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: ${({ color }) => color};
  text-transform: uppercase;
  letter-spacing: 1px;
`;

const MacroText = styled.p`
  font-size: 1.1rem;
  color: var(--color-text-primary);
  line-height: 1.8;
  font-style: italic;
  max-width: 90%;
  margin: 0 auto;
`;

const GridSection = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const ZoneCard = styled.div`
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
`;

const ZoneTitle = styled.h4`
  color: #EBCB8B; /* Gold */
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const LevelList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const LevelItem = styled.li`
  color: var(--color-text-secondary);
  margin-bottom: 0.8rem;
  display: flex;
  align-items: start;
  gap: 10px;
  line-height: 1.5;

  svg { color: #EBCB8B; margin-top: 4px; }
`;

const StrategyBox = styled.div`
  background: linear-gradient(135deg, rgba(235, 203, 139, 0.1), rgba(13, 17, 23, 0.8));
  border: 1px solid #EBCB8B;
  border-radius: 12px;
  padding: 2rem;
  position: relative;
`;

const StrategyHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(235, 203, 139, 0.2);
  padding-bottom: 1rem;
`;

const DirectionBadge = styled.span`
  background: ${({ isBullish }) => isBullish ? '#3FB950' : '#F85149'};
  color: #000;
  padding: 5px 15px;
  border-radius: 50px;
  font-weight: 800;
  font-size: 1rem;
  text-transform: uppercase;
`;

const MetricRow = styled.div`
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-size: 1.1rem;
`;

const Label = styled.span` color: var(--color-text-secondary); font-size: 0.9rem; `;
const Value = styled.span` font-weight: 700; color: #EBCB8B; font-family: 'Roboto Mono'; `;

// --- COMPONENT ---

const IndexChartAnalysis = ({ analysisData }) => {
  
  // --- PARSER ---
  const parsed = useMemo(() => {
    if (!analysisData || typeof analysisData !== 'string') return null;
    
    const rawKeys = ['TREND', 'PATTERNS', 'LEVELS', 'VOLUME', 'MOMENTUM', 'INDICATORS', 'CONCLUSION', 'ACTION', 'ENTRY_ZONE', 'STOP_LOSS', 'TARGET_1', 'TARGET_2', 'RISK_REWARD', 'CONFIDENCE', 'RATIONALE'];
    const sections = {};
    let text = "\n" + analysisData.replace(/\*\*/g, '');

    rawKeys.forEach(key => {
      const regex = new RegExp(`(?:^|\\n)\\s*${key}\\s*:\\s*([\\s\\S]*?)(?=\\n\\s*[A-Z_]{3,}\\s*:|$)`, 'i');
      const match = text.match(regex);
      if (match) sections[key] = match[1].trim();
    });
    return sections;
  }, [analysisData]);

  if (!parsed) return null;

  // Visual Logic
  const isBullish = parsed.TREND?.toLowerCase().includes('uptrend') || parsed.TREND?.toLowerCase().includes('bullish');
  const isBearish = parsed.TREND?.toLowerCase().includes('downtrend') || parsed.TREND?.toLowerCase().includes('bearish');
  
  const TrendIcon = isBullish ? FaArrowUp : isBearish ? FaArrowDown : FaExchangeAlt;
  const trendColor = isBullish ? '#3FB950' : isBearish ? '#F85149' : '#EBCB8B';

  return (
    <AnalysisContainer>
      
      {/* 1. MACRO VERDICT */}
      <MacroVerdictCard>
        <div style={{color: '#EBCB8B', fontSize: '0.8rem', fontWeight: 600, marginBottom: '10px', textTransform: 'uppercase'}}>AI Macro Outlook</div>
        <TrendDisplay color={trendColor}>
           <TrendIcon /> {parsed.TREND || 'Consolidation'}
        </TrendDisplay>
        <MacroText>
          "{parsed.CONCLUSION || parsed.RATIONALE}"
        </MacroText>
      </MacroVerdictCard>

      {/* 2. STRATEGY ROOM */}
      <StrategyBox>
        <StrategyHeader>
           <div style={{display:'flex', flexDirection:'column'}}>
               <span style={{color:'#EBCB8B', fontSize:'0.8rem', fontWeight: 700}}>MARKET BIAS</span>
               <span style={{color:'white', fontSize:'1.4rem', fontWeight: 700}}>
                   {parsed.ACTION?.toUpperCase() || 'WAIT'}
               </span>
           </div>
           <DirectionBadge isBullish={isBullish || parsed.ACTION?.includes('BUY')}>
               {parsed.ACTION?.includes('BUY') ? 'LONG' : parsed.ACTION?.includes('SELL') ? 'SHORT' : 'NEUTRAL'}
           </DirectionBadge>
        </StrategyHeader>
        
        <MetricRow><Label>Entry Zone</Label><Value>{parsed.ENTRY_ZONE}</Value></MetricRow>
        <MetricRow><Label>Invalidation (SL)</Label><Value style={{color:'#F85149'}}>{parsed.STOP_LOSS}</Value></MetricRow>
        <MetricRow><Label>Objective 1</Label><Value style={{color:'#3FB950'}}>{parsed.TARGET_1}</Value></MetricRow>
        <MetricRow><Label>Objective 2</Label><Value style={{color:'#3FB950'}}>{parsed.TARGET_2}</Value></MetricRow>
      </StrategyBox>

      {/* 3. TECHNICAL DEEP DIVE */}
      <GridSection>
        <ZoneCard>
          <ZoneTitle><FaShieldAlt /> Key Levels</ZoneTitle>
          <LevelList>
             <LevelItem><FaChartLine /> {parsed.LEVELS}</LevelItem>
          </LevelList>
        </ZoneCard>

        <ZoneCard>
          <ZoneTitle><FaLayerGroup /> Market Structure</ZoneTitle>
          <LevelList>
             {parsed.PATTERNS && <LevelItem><FaGlobeAmericas /> {parsed.PATTERNS}</LevelItem>}
             {parsed.VOLUME && <LevelItem><FaChartLine /> {parsed.VOLUME}</LevelItem>}
             {parsed.INDICATORS && <LevelItem><FaBullseye /> {parsed.INDICATORS}</LevelItem>}
          </LevelList>
        </ZoneCard>
      </GridSection>

    </AnalysisContainer>
  );
};

export default IndexChartAnalysis;