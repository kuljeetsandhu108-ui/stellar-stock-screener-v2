import React, { useState, useMemo, useEffect, useCallback } from 'react';
import styled, { keyframes } from 'styled-components';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import Card from '../common/Card';
import { 
  FaArrowUp, FaArrowDown, FaExchangeAlt, FaGem, FaExclamationTriangle, 
  FaBullseye, FaChartLine, FaMoneyBillWave, FaCrosshairs, FaStopCircle, 
  FaTachometerAlt, FaLayerGroup, FaRedo, FaRobot
} from 'react-icons/fa';

// ==========================================
// 1. ANIMATIONS & STYLES
// ==========================================

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const scanAnimation = keyframes`
  0% { top: 0%; opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { top: 100%; opacity: 0; }
`;

const pulseText = keyframes`
  0% { opacity: 0.4; }
  50% { opacity: 1; }
  100% { opacity: 0.4; }
`;

const spin = keyframes`
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
`;

const AnalysisGrid = styled.div`
  display: grid;
  gap: 1.5rem;
  animation: ${fadeIn} 0.5s ease-out;
  opacity: ${({ $isUpdating }) => ($isUpdating ? 0.5 : 1)};
  transition: opacity 0.3s ease;
  pointer-events: ${({ $isUpdating }) => ($isUpdating ? 'none' : 'auto')};
`;

const TimeframeBar = styled.div`
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
  padding: 0.5rem;
  background-color: var(--color-background);
  border-radius: 12px;
  border: 1px solid var(--color-border);
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  flex-wrap: wrap;
  
  @media (max-width: 768px) {
    width: 100%;
    justify-content: space-between;
    padding: 0.25rem;
    gap: 0.25rem;
  }
`;

const TimeframeButton = styled.button`
  background: ${({ active }) => (active ? 'var(--color-primary)' : 'transparent')};
  color: ${({ active }) => (active ? '#ffffff' : 'var(--color-text-secondary)')};
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 6px;

  &:hover {
    color: ${({ active }) => (active ? '#ffffff' : 'var(--color-text-primary)')};
    background: ${({ active }) => (active ? 'var(--color-primary)' : 'rgba(255,255,255,0.05)')};
  }

  @media (max-width: 768px) {
    padding: 0.5rem 0.8rem;
    font-size: 0.8rem;
    flex-grow: 1;
  }
`;

const VerdictCard = styled(Card)`
  text-align: center;
  border-left: 4px solid ${({ color }) => color};
  box-shadow: 0 4px 15px ${({ color }) => color}22;
  padding: 2rem;
  background: linear-gradient(180deg, rgba(22, 27, 34, 0.6) 0%, rgba(13, 17, 23, 1) 100%);
`;

const TrendDisplay = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  font-size: 1.8rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: ${({ color }) => color};
  text-transform: uppercase;
  letter-spacing: 1px;
  text-shadow: 0 0 20px ${({ color }) => color}44;
`;

const ConclusionText = styled.p`
  font-size: 1.1rem;
  font-style: italic;
  color: var(--color-text-primary);
  max-width: 85%;
  margin: 0 auto;
  line-height: 1.6;
  opacity: 0.9;
  font-weight: 500;
`;

const TradeTicket = styled.div`
  background: linear-gradient(135deg, rgba(22, 27, 34, 0.95), rgba(30, 41, 59, 0.95));
  border: 1px solid ${({ action }) => (action === 'BUY' ? 'var(--color-success)' : action === 'SELL' ? 'var(--color-danger)' : 'var(--color-border)')};
  border-radius: 16px;
  padding: 2rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  
  &::before {
    content: '${({ action }) => action}';
    position: absolute;
    top: -15px;
    right: -10px;
    font-size: 6rem;
    font-weight: 900;
    opacity: 0.03;
    color: ${({ action }) => (action === 'BUY' ? 'var(--color-success)' : action === 'SELL' ? 'var(--color-danger)' : '#FFF')};
    pointer-events: none;
    z-index: 0;
  }
`;

const TicketHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  padding-bottom: 1rem;
  position: relative;
  z-index: 1;
`;

const ActionBadge = styled.span`
  background-color: ${({ action }) => (action === 'BUY' ? 'rgba(16, 185, 129, 0.15)' : action === 'SELL' ? 'rgba(239, 68, 68, 0.15)' : 'rgba(100, 116, 139, 0.15)')};
  color: ${({ action }) => (action === 'BUY' ? 'var(--color-success)' : action === 'SELL' ? 'var(--color-danger)' : '#94A3B8')};
  border: 1px solid ${({ action }) => (action === 'BUY' ? 'var(--color-success)' : action === 'SELL' ? 'var(--color-danger)' : '#94A3B8')};
  padding: 0.5rem 1.5rem;
  border-radius: 6px;
  font-weight: 800;
  font-size: 1rem;
  letter-spacing: 1px;
  box-shadow: 0 0 15px ${({ action }) => (action === 'BUY' ? 'rgba(16, 185, 129, 0.1)' : action === 'SELL' ? 'rgba(239, 68, 68, 0.1)' : 'transparent')};
`;

const TradeMetricGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;

  @media (max-width: 768px) {
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
`;

const TradeMetric = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
`;

const MetricLabel = styled.span`
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--color-text-secondary);
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: 600;
`;

const MetricValue = styled.span`
  font-size: 1.2rem;
  font-weight: 700;
  font-family: 'Roboto Mono', monospace;
  color: ${({ color }) => color || 'var(--color-text-primary)'};
  word-break: break-word;
`;

const RationaleBox = styled.div`
  background: rgba(255,255,255,0.03);
  padding: 1.25rem;
  border-radius: 8px;
  border-left: 3px solid var(--color-primary);
  position: relative;
  z-index: 1;
`;

const DetailsGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const InfoCard = styled(Card)`
  background-color: var(--color-background);
  height: 100%;
`;

const SectionTitle = styled.h4`
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const InfoList = styled.ul`
  list-style-type: none;
  padding-left: 0;
`;

const InfoListItem = styled.li`
  margin-bottom: 1rem;
  color: var(--color-text-secondary);
  line-height: 1.6;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  font-size: 0.95rem;
  
  & > svg {
    flex-shrink: 0;
    margin-top: 4px;
    color: var(--color-primary);
    opacity: 0.8;
  }
`;

const ContentText = styled.p`
  font-size: 1rem;
  color: var(--color-text-secondary);
  line-height: 1.7;
  white-space: pre-wrap;
`;

// --- SCANNER / LOADING STATE ---
const ScannerContainer = styled.div`
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

const ScannerLine = styled.div`
  position: absolute;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, transparent, var(--color-primary), transparent);
  box-shadow: 0 0 15px var(--color-primary);
  animation: ${scanAnimation} 2s linear infinite;
  z-index: 1;
`;

const ProcessingIcon = styled(FaRobot)`
  font-size: 3.5rem;
  color: var(--color-primary);
  margin-bottom: 1.5rem;
  filter: drop-shadow(0 0 10px rgba(88, 166, 255, 0.4));
  animation: ${pulseText} 1.5s infinite ease-in-out;
`;

const ProcessingText = styled.h3`
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: 1px;
  margin-bottom: 0.5rem;
`;

const ProcessingSubtext = styled.p`
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  animation: ${pulseText} 2s infinite;
`;

const ErrorStateContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
`;

const RefreshButton = styled.button`
  background-color: var(--color-secondary);
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1.5rem;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.2s ease;

  &:hover {
    background-color: var(--color-primary);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(88, 166, 255, 0.3);
  }

  & svg {
    transition: transform 0.5s ease;
  }

  &:hover svg {
    animation: ${spin} 1s linear infinite;
  }
`;

// ==========================================
// 2. MAIN COMPONENT LOGIC
// ==========================================

const ChartAnalysis = ({ analysisData: initialAnalysisData }) => {
  const { symbol } = useParams();
  
  // State for caching analysis of different timeframes
  const [analysisCache, setAnalysisCache] = useState({ 'Image': initialAnalysisData });
  const [activeTimeframe, setActiveTimeframe] = useState('Image');
  const [isUpdating, setIsUpdating] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  // Initialize with passed data
  useEffect(() => {
    setAnalysisCache({ 'Image': initialAnalysisData });
    setActiveTimeframe('Image');
    setErrorMessage(null);
  }, [initialAnalysisData, symbol]);

  const timeframes = ['5m', '15m', '1h', '4h', '1d'];

  // Fetch new analysis when switching timeframes
  const fetchAnalysisData = useCallback(async (tf) => {
    setIsUpdating(true);
    setErrorMessage(null);
    try {
        const response = await axios.post(`/api/stocks/${symbol}/timeframe-analysis`, {
            timeframe: tf
        });
        
        const newData = response.data.analysis;
        
        // Basic validation of AI response
        if (!newData || newData.length < 20 || newData.includes("RATIONALE: Analysis failed") || newData.includes("TREND: Error")) {
            throw new Error("Invalid Response");
        }

        setAnalysisCache(prev => ({ ...prev, [tf]: newData }));
    } catch (error) {
        console.error("Timeframe analysis failed:", error);
        setErrorMessage("AI Connection Interrupted. Please try again.");
    } finally {
        setIsUpdating(false);
    }
  }, [symbol]);

  // Handle Tab Click
  const handleTimeframeChange = (tf) => {
    if (activeTimeframe === tf) return;
    setActiveTimeframe(tf);
    
    // Check cache first
    if (analysisCache[tf] && !analysisCache[tf].includes("TREND: Error")) { 
        setErrorMessage(null); 
        return; 
    }
    
    fetchAnalysisData(tf);
  };

  // Retry Logic
  const handleRetry = () => {
      setAnalysisCache(prev => { 
          const newCache = { ...prev }; 
          delete newCache[activeTimeframe]; 
          return newCache; 
      });
      fetchAnalysisData(activeTimeframe);
  };

  const currentAnalysis = analysisCache[activeTimeframe];

  // --- 3. ROBUST PARSER (The Key to Clean UI) ---
  const parsedAnalysis = useMemo(() => {
    if (!currentAnalysis || typeof currentAnalysis !== 'string') return null;
    
    const rawKeys = [
        'TREND', 'PATTERNS', 'LEVELS', 'VOLUME', 'MOMENTUM', 'INDICATORS', 'CONCLUSION', 
        'ACTION', 'ENTRY_ZONE', 'STOP_LOSS', 'TARGET_1', 'TARGET_2', 'RISK_REWARD', 'CONFIDENCE', 'RATIONALE'
    ];
    const sections = {};
    
    // Clean artifacts like "**" bold markers and "-- TRADE TICKET --" separators
    let text = "\n" + currentAnalysis.replace(/\*\*/g, '').replace(/-- TRADE TICKET --/g, '');

    rawKeys.forEach(key => {
      // Regex finds the content after "KEY:" until the next newline followed by a "KEY:"
      const regex = new RegExp(`(?:^|\\n)\\s*${key}\\s*:\\s*([\\s\\S]*?)(?=\\n\\s*[A-Z_]{3,}\\s*:|$)`, 'i');
      const match = text.match(regex);
      if (match) sections[key] = match[1].trim();
    });
    return sections;
  }, [currentAnalysis]);

  // --- 4. RENDER HELPERS ---
  const getTrendInfo = () => {
    const trend = parsedAnalysis?.TREND?.toLowerCase() || '';
    if (trend.includes('uptrend') || trend.includes('bullish')) 
        return { Icon: FaArrowUp, color: 'var(--color-success)', text: 'Bullish Trend' };
    if (trend.includes('downtrend') || trend.includes('bearish')) 
        return { Icon: FaArrowDown, color: 'var(--color-danger)', text: 'Bearish Trend' };
    return { Icon: FaExchangeAlt, color: 'var(--color-text-secondary)', text: 'Sideways / Range' };
  };

  const action = parsedAnalysis?.ACTION ? parsedAnalysis.ACTION.toUpperCase() : 'WAIT';
  const { Icon: TrendIcon, color: trendColor, text: trendText } = getTrendInfo();

  // Logic to show/hide states
  const isBackendError = parsedAnalysis?.TREND && parsedAnalysis.TREND.includes('Error');
  const showRefreshButton = !isUpdating && (errorMessage || isBackendError);
  const showContent = parsedAnalysis && !isBackendError && !showRefreshButton && !isUpdating;

  return (
    <div style={{ position: 'relative' }}>
      
      {/* Timeframe Selector */}
      <TimeframeBar>
        <TimeframeButton 
            active={activeTimeframe === 'Image'} 
            onClick={() => handleTimeframeChange('Image')} 
            disabled={isUpdating}
        >
            <FaGem /> Original Image
        </TimeframeButton>
        {timeframes.map(tf => (
            <TimeframeButton 
                key={tf} 
                active={activeTimeframe === tf} 
                onClick={() => handleTimeframeChange(tf)} 
                disabled={isUpdating}
            >
                {tf.toUpperCase()}
            </TimeframeButton>
        ))}
      </TimeframeBar>

      {/* State 1: Loading */}
      {isUpdating ? (
        <ScannerContainer>
            <ScannerLine />
            <ProcessingIcon />
            <ProcessingText>SYSTEM ANALYST INITIALIZING</ProcessingText>
            <ProcessingSubtext>
                Scanning {activeTimeframe === 'Image' ? 'Chart Image' : `${activeTimeframe.toUpperCase()} Data`}...
            </ProcessingSubtext>
        </ScannerContainer>
      ) : showRefreshButton ? (
        /* State 2: Error / Retry */
        <Card>
            <ErrorStateContainer>
                <FaExclamationTriangle style={{fontSize: '3rem', color: 'var(--color-text-secondary)', marginBottom: '1rem'}} />
                <h3 style={{color: 'var(--color-text-primary)', marginBottom: '0.5rem'}}>Analysis Unavailable</h3>
                <RefreshButton onClick={handleRetry}><FaRedo /> Regenerate Analysis</RefreshButton>
            </ErrorStateContainer>
        </Card>
      ) : showContent ? (
        /* State 3: Analysis Content */
        <AnalysisGrid $isUpdating={isUpdating}>
            
            {/* Trend Verdict */}
            <VerdictCard color={trendColor}>
              <TrendDisplay color={trendColor}>
                  <TrendIcon /> {trendText}
              </TrendDisplay>
              <ConclusionText>
                  "{parsedAnalysis?.CONCLUSION || parsedAnalysis?.RATIONALE}"
              </ConclusionText>
            </VerdictCard>

            {/* Trade Ticket (Only if Action is clear) */}
            {parsedAnalysis?.ENTRY_ZONE && (
                <TradeTicket action={action}>
                <TicketHeader>
                    <div>
                        <div style={{fontSize: '0.8rem', color: 'var(--color-text-secondary)', marginBottom: '5px', letterSpacing: '1px'}}>STRATEGY SIGNAL</div>
                        <ActionBadge action={action}>{action}</ActionBadge>
                    </div>
                    <div style={{textAlign: 'right'}}>
                        <div style={{fontSize: '0.8rem', color: 'var(--color-text-secondary)', marginBottom: '5px', letterSpacing: '1px'}}>CONFIDENCE</div>
                        <div style={{fontSize: '1.2rem', fontWeight: 'bold', color: 'var(--color-text-primary)'}}>{parsedAnalysis.CONFIDENCE || 'Medium'}</div>
                    </div>
                </TicketHeader>

                <TradeMetricGrid>
                    <TradeMetric>
                        <MetricLabel><FaCrosshairs /> ENTRY ZONE</MetricLabel>
                        <MetricValue color="#60A5FA">{parsedAnalysis.ENTRY_ZONE}</MetricValue>
                    </TradeMetric>
                    <TradeMetric>
                        <MetricLabel><FaStopCircle /> STOP LOSS</MetricLabel>
                        <MetricValue color="#F87171">{parsedAnalysis.STOP_LOSS}</MetricValue>
                    </TradeMetric>
                    <TradeMetric>
                        <MetricLabel><FaMoneyBillWave /> TARGET 1</MetricLabel>
                        <MetricValue color="#34D399">{parsedAnalysis.TARGET_1}</MetricValue>
                    </TradeMetric>
                    <TradeMetric>
                        <MetricLabel><FaChartLine /> R/R RATIO</MetricLabel>
                        <MetricValue color="#FBBF24">{parsedAnalysis.RISK_REWARD}</MetricValue>
                    </TradeMetric>
                </TradeMetricGrid>

                <RationaleBox>
                    <strong style={{color: 'var(--color-primary)', display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem', textTransform: 'uppercase'}}>Trade Rationale</strong>
                    <span style={{color: 'var(--color-text-secondary)', lineHeight: '1.6', fontSize: '0.95rem'}}>{parsedAnalysis.RATIONALE}</span>
                </RationaleBox>
                </TradeTicket>
            )}
            
            {/* Deep Dive Grid */}
            <DetailsGrid>
              <InfoCard>
                  <SectionTitle><FaLayerGroup /> Key Patterns</SectionTitle>
                  <InfoList>
                  {parsedAnalysis?.PATTERNS ? (
                      parsedAnalysis.PATTERNS.split('\n').map((item, index) => (
                        <InfoListItem key={index}><FaChartLine /> {item.replace(/^- /, '')}</InfoListItem>
                      ))
                  ) : <p style={{color: 'var(--color-text-secondary)', fontStyle: 'italic'}}>No specific chart patterns detected.</p>}
                  </InfoList>
              </InfoCard>

              <InfoCard>
                  <SectionTitle><FaExclamationTriangle /> Market Internals</SectionTitle>
                  <InfoList>
                  {parsedAnalysis?.VOLUME && (
                      <InfoListItem><strong><FaChartLine /> Volume:</strong> {parsedAnalysis.VOLUME}</InfoListItem>
                  )}
                  {parsedAnalysis?.MOMENTUM && (
                      <InfoListItem><strong><FaTachometerAlt /> Momentum:</strong> {parsedAnalysis.MOMENTUM}</InfoListItem>
                  )}
                  </InfoList>
              </InfoCard>
            </DetailsGrid>
        </AnalysisGrid>
      ) : null}
    </div>
  );
};

export default ChartAnalysis;