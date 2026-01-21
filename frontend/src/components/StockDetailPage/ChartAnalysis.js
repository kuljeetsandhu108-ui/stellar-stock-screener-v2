import React, { useState, useMemo, useEffect } from 'react';
import styled, { keyframes, css } from 'styled-components';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import Card from '../common/Card';
import { 
  FaArrowUp, FaArrowDown, FaExchangeAlt, FaGem, FaExclamationTriangle, 
  FaChartLine, FaCrosshairs, FaStopCircle, FaMoneyBillWave, FaLayerGroup, FaRobot, FaTachometerAlt
} from 'react-icons/fa';

// ==========================================
// 1. HIGH-END ANIMATIONS & STYLES
// ==========================================

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const scanAnimation = keyframes`
  0% { top: 0%; opacity: 0; }
  15% { opacity: 1; }
  85% { opacity: 1; }
  100% { top: 100%; opacity: 0; }
`;

const pulseGlow = keyframes`
  0% { box-shadow: 0 0 5px rgba(88, 166, 255, 0.2); }
  50% { box-shadow: 0 0 20px rgba(88, 166, 255, 0.6); }
  100% { box-shadow: 0 0 5px rgba(88, 166, 255, 0.2); }
`;

const AnalysisContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
`;

const TimeframeBar = styled.div`
  display: flex;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding: 0.75rem;
  background: #161B22;
  border-radius: 16px;
  border: 1px solid var(--color-border);
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
  flex-wrap: wrap;

  @media (max-width: 768px) {
    width: 100%;
    gap: 0.5rem;
  }
`;

const TimeframeButton = styled.button`
  background: ${({ active }) => (active ? 'linear-gradient(135deg, #58A6FF, #238636)' : 'transparent')};
  color: ${({ active }) => (active ? '#ffffff' : '#8B949E')};
  border: 1px solid ${({ active }) => (active ? 'transparent' : 'rgba(255,255,255,0.1)')};
  padding: 0.6rem 1.2rem;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  overflow: hidden;

  &:hover {
    transform: translateY(-2px);
    color: #ffffff;
    border-color: #58A6FF;
    box-shadow: 0 4px 12px rgba(88, 166, 255, 0.2);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }

  /* Active glow effect */
  ${({ active }) => active && css`
    box-shadow: 0 0 15px rgba(35, 134, 54, 0.4);
  `}
`;

const AnalysisGrid = styled.div`
  display: grid;
  gap: 2rem;
  animation: ${fadeIn} 0.5s ease-out;
`;

// --- VERDICT CARD ---
const VerdictCard = styled(Card)`
  text-align: center;
  border-left: 5px solid ${({ color }) => color};
  background: linear-gradient(180deg, rgba(22, 27, 34, 0.8) 0%, rgba(13, 17, 23, 1) 100%);
  padding: 2.5rem;
  position: relative;
  overflow: hidden;
  
  /* Background glow based on trend */
  &::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 100%;
    background: ${({ color }) => color};
    opacity: 0.03;
    pointer-events: none;
  }
`;

const TrendDisplay = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-size: 2.2rem;
  font-weight: 900;
  margin-bottom: 1rem;
  color: ${({ color }) => color};
  text-transform: uppercase;
  letter-spacing: 2px;
  text-shadow: 0 0 30px ${({ color }) => color}44;

  svg {
    filter: drop-shadow(0 0 10px ${({ color }) => color});
  }
`;

const ConclusionText = styled.p`
  font-size: 1.1rem;
  color: #C9D1D9;
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.8;
  font-style: italic;
  font-weight: 500;
  border-top: 1px solid rgba(255,255,255,0.1);
  padding-top: 1.5rem;
`;

// --- TRADE TICKET ---
const TradeTicket = styled.div`
  background: linear-gradient(135deg, #161B22 0%, #0D1117 100%);
  border: 1px solid ${({ action }) => (action === 'BUY' ? '#238636' : action === 'SELL' ? '#DA3633' : '#8B949E')};
  border-radius: 16px;
  padding: 0;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0,0,0,0.3);
`;

const TicketHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: rgba(255,255,255,0.02);
  border-bottom: 1px solid rgba(255,255,255,0.05);
`;

const ActionBadge = styled.span`
  background: ${({ action }) => (action === 'BUY' ? 'rgba(57, 211, 83, 0.15)' : action === 'SELL' ? 'rgba(248, 81, 73, 0.15)' : 'rgba(139, 148, 158, 0.15)')};
  color: ${({ action }) => (action === 'BUY' ? '#3FB950' : action === 'SELL' ? '#F85149' : '#8B949E')};
  border: 1px solid ${({ action }) => (action === 'BUY' ? '#3FB950' : action === 'SELL' ? '#F85149' : '#8B949E')};
  padding: 0.5rem 1.5rem;
  border-radius: 8px;
  font-weight: 800;
  font-size: 1.1rem;
  letter-spacing: 1.5px;
  box-shadow: 0 0 15px ${({ action }) => (action === 'BUY' ? 'rgba(57, 211, 83, 0.1)' : action === 'SELL' ? 'rgba(248, 81, 73, 0.1)' : 'transparent')};
`;

const MetricGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background: rgba(255,255,255,0.05); /* Grid lines */
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr 1fr;
  }
`;

const MetricBox = styled.div`
  background: #0D1117;
  padding: 1.5rem;
  text-align: center;
  transition: background 0.2s;
  
  &:hover {
    background: #161B22;
  }
`;

const MetricLabel = styled.div`
  font-size: 0.7rem;
  color: #8B949E;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
`;

const MetricVal = styled.div`
  font-size: 1.25rem;
  font-weight: 700;
  font-family: 'Roboto Mono', monospace;
  color: ${({ color }) => color || '#C9D1D9'};
`;

const RationaleBox = styled.div`
  padding: 2rem;
  background: rgba(88, 166, 255, 0.05);
  border-top: 1px solid rgba(88, 166, 255, 0.1);
  
  strong {
    color: #58A6FF;
    display: block;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  
  p {
    color: #C9D1D9;
    line-height: 1.6;
    margin: 0;
    font-size: 1rem;
  }
`;

// --- SCANNER LOADING STATE ---
const ScannerBox = styled.div`
  position: relative;
  width: 100%;
  height: 400px;
  background: rgba(22, 27, 34, 0.4);
  border: 1px dashed var(--color-border);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  animation: ${fadeIn} 0.3s ease-out;
`;

const ScanLine = styled.div`
  position: absolute;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #58A6FF, transparent);
  box-shadow: 0 0 20px #58A6FF;
  animation: ${scanAnimation} 2s linear infinite;
`;

const ProcessingIcon = styled(FaRobot)`
  font-size: 4rem;
  color: #58A6FF;
  margin-bottom: 1.5rem;
  animation: ${pulseGlow} 2s infinite;
`;

const DetailGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-top: 1.5rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const InfoList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const InfoItem = styled.li`
  display: flex;
  align-items: start;
  gap: 10px;
  margin-bottom: 0.8rem;
  color: #8B949E;
  font-size: 0.95rem;
  line-height: 1.5;

  svg {
    margin-top: 4px;
    color: #EBCB8B;
  }
`;

// ==========================================
// 2. MAIN COMPONENT
// ==========================================

const ChartAnalysis = ({ analysisData }) => {
  const { symbol } = useParams();
  
  // Cache stores all analysis: { "image": "...", "1h": "...", "4h": "..." }
  // Initialize with the Image analysis passed from props (if any)
  const [cache, setCache] = useState({ 'Image': analysisData });
  const [activeTab, setActiveTab] = useState('Image');
  const [isLoading, setIsLoading] = useState(false);
  const [isOmniLoaded, setIsOmniLoaded] = useState(false);

  // --- OMNI-FETCH ENGINE ---
  useEffect(() => {
      const fetchAllTimeframes = async () => {
          // If we already loaded the "Omni" packet, stop.
          if (isOmniLoaded) return;

          setIsLoading(true);
          try {
              // This endpoint calculates 5M, 15M, 1H, 4H, 1D concurrently on server
              const res = await axios.post(`/api/stocks/${symbol}/all-timeframe-analysis`);
              
              if (res.data && !res.data.error) {
                  // Merge new data with existing Image data
                  setCache(prev => ({ ...prev, ...res.data }));
                  setIsOmniLoaded(true);
              }
          } catch (e) {
              console.error("Omni-Analysis Failed:", e);
          } finally {
              setIsLoading(false);
          }
      };
      
      // Delay slightly to let UI render first
      const timer = setTimeout(fetchAllTimeframes, 500);
      return () => clearTimeout(timer);
  }, [symbol, isOmniLoaded]);

  // --- INSTANT SWITCHING ---
  const handleTabChange = (tf) => {
      setActiveTab(tf);
  };

  // Get current text for active tab (Handle case sensitivity)
  const currentText = cache[activeTab] || cache[activeTab.toLowerCase()] || cache[activeTab.toUpperCase()];

  // --- PARSER ENGINE ---
  const parsed = useMemo(() => {
    if (!currentText || typeof currentText !== 'string') return null;
    
    const rawKeys = ['TREND', 'PATTERNS', 'LEVELS', 'VOLUME', 'MOMENTUM', 'INDICATORS', 'CONCLUSION', 'ACTION', 'ENTRY_ZONE', 'STOP_LOSS', 'TARGET_1', 'TARGET_2', 'RISK_REWARD', 'CONFIDENCE', 'RATIONALE'];
    const sections = {};
    
    // Clean artifacts
    let text = "\n" + currentText.replace(/\*\*/g, '').replace(/-- TRADE TICKET --/g, '');

    rawKeys.forEach(key => {
      const regex = new RegExp(`(?:^|\\n)\\s*${key}\\s*:\\s*([\\s\\S]*?)(?=\\n\\s*[A-Z_]{3,}\\s*:|$)`, 'i');
      const match = text.match(regex);
      if (match) sections[key] = match[1].trim();
    });
    return sections;
  }, [currentText]);

  // --- VISUAL HELPERS ---
  const getTrendInfo = () => {
    const t = parsed?.TREND?.toLowerCase() || '';
    if (t.includes('uptrend') || t.includes('bullish')) return { icon: FaArrowUp, color: '#3FB950', text: 'Bullish Structure' };
    if (t.includes('downtrend') || t.includes('bearish')) return { icon: FaArrowDown, color: '#F85149', text: 'Bearish Structure' };
    return { icon: FaExchangeAlt, color: '#EBCB8B', text: 'Consolidation / Range' };
  };

  const { icon: TrendIcon, color: trendColor, text: trendText } = getTrendInfo();
  const action = parsed?.ACTION?.toUpperCase() || 'WAIT';

  // ==========================================
  // 3. RENDER
  // ==========================================
  
  return (
    <AnalysisContainer>
      
      {/* 1. Navigation Bar */}
      <TimeframeBar>
        <TimeframeButton 
            active={activeTab === 'Image'} 
            onClick={() => handleTabChange('Image')}
        >
            <FaGem /> Original Image
        </TimeframeButton>
        {['5m', '15m', '1h', '4h', '1d'].map(tf => (
            <TimeframeButton 
                key={tf} 
                active={activeTab === tf} 
                onClick={() => handleTabChange(tf)}
                disabled={!isOmniLoaded && !cache[tf]} // Disable if math not ready
            >
               {tf.toUpperCase()}
            </TimeframeButton>
        ))}
      </TimeframeBar>

      {/* 2. Content Area */}
      
      {/* STATE A: Loading Math Models */}
      {isLoading && !currentText ? (
          <ScannerBox>
              <ScanLine />
              <ProcessingIcon />
              <h3 style={{color:'#C9D1D9', letterSpacing:'2px'}}>QUANT ENGINE RUNNING</h3>
              <p style={{color:'#8B949E'}}>Calculating Math Models for All Timeframes...</p>
          </ScannerBox>
      ) : parsed ? (
          /* STATE B: Data Loaded */
          <AnalysisGrid>
              
              {/* Verdict Section */}
              <VerdictCard color={trendColor}>
                  <div style={{color: trendColor, fontSize:'0.9rem', textTransform:'uppercase', letterSpacing:'1px', marginBottom:'0.5rem'}}>
                      MARKET STRUCTURE ({activeTab.toUpperCase()})
                  </div>
                  <TrendDisplay color={trendColor}>
                      <TrendIcon /> {trendText}
                  </TrendDisplay>
                  <ConclusionText>
                      "{parsed.CONCLUSION || parsed.RATIONALE}"
                  </ConclusionText>
              </VerdictCard>

              {/* Trade Ticket (Only if Actionable) */}
              {parsed.ENTRY_ZONE && (
                  <TradeTicket action={action}>
                      <TicketHeader>
                          <div>
                              <div style={{fontSize:'0.75rem', color:'#8B949E', letterSpacing:'1px', marginBottom:'5px'}}>STRATEGY SIGNAL</div>
                              <ActionBadge action={action}>{action}</ActionBadge>
                          </div>
                          <div style={{textAlign:'right'}}>
                              <div style={{fontSize:'0.75rem', color:'#8B949E', letterSpacing:'1px', marginBottom:'5px'}}>AI CONFIDENCE</div>
                              <div style={{fontSize:'1.5rem', fontWeight:'bold', color:'#C9D1D9'}}>{parsed.CONFIDENCE || 'Medium'}</div>
                          </div>
                      </TicketHeader>

                      <MetricGrid>
                          <MetricBox>
                              <MetricLabel><FaCrosshairs /> Entry Zone</MetricLabel>
                              <MetricVal color="#58A6FF">{parsed.ENTRY_ZONE}</MetricVal>
                          </MetricBox>
                          <MetricBox>
                              <MetricLabel><FaStopCircle /> Invalidation</MetricLabel>
                              <MetricVal color="#F85149">{parsed.STOP_LOSS}</MetricVal>
                          </MetricBox>
                          <MetricBox>
                              <MetricLabel><FaMoneyBillWave /> Target 1</MetricLabel>
                              <MetricVal color="#3FB950">{parsed.TARGET_1}</MetricVal>
                          </MetricBox>
                          <MetricBox>
                              <MetricLabel><FaChartLine /> R:R Ratio</MetricLabel>
                              <MetricVal color="#EBCB8B">{parsed.RISK_REWARD}</MetricVal>
                          </MetricBox>
                      </MetricGrid>

                      <RationaleBox>
                          <strong><FaRobot style={{marginRight:'8px'}}/> Mathematical Rationale</strong>
                          <p>{parsed.RATIONALE}</p>
                      </RationaleBox>
                  </TradeTicket>
              )}

              {/* Technical Details Grid */}
              <DetailGrid>
                  <Card title="Key Levels">
                      <InfoList>
                         <InfoItem><FaLayerGroup /> {parsed.LEVELS || 'Analyzing key levels...'}</InfoItem>
                         <InfoItem><FaTachometerAlt /> {parsed.MOMENTUM || 'Analyzing momentum...'}</InfoItem>
                      </InfoList>
                  </Card>
                  <Card title="Patterns & Indicators">
                      <InfoList>
                         <InfoItem><FaChartLine /> {parsed.PATTERNS || 'No specific patterns detected.'}</InfoItem>
                         <InfoItem><FaExclamationTriangle /> {parsed.INDICATORS || 'Calculating indicators...'}</InfoItem>
                      </InfoList>
                  </Card>
              </DetailGrid>

          </AnalysisGrid>
      ) : (
          /* STATE C: Error / Empty */
          <div style={{textAlign:'center', padding:'3rem', color:'#8B949E', border:'1px dashed #30363D', borderRadius:'16px'}}>
              <FaExclamationTriangle size={30} style={{marginBottom:'1rem'}} />
              <p>Analysis data unavailable for this timeframe.</p>
              <p style={{fontSize:'0.8rem'}}>Try regenerating from the chart image.</p>
          </div>
      )}
    </AnalysisContainer>
  );
};

export default ChartAnalysis;