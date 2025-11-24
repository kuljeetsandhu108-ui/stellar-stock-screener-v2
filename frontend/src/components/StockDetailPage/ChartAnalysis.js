import React, { useMemo } from 'react';
import styled, { keyframes } from 'styled-components';
import Card from '../common/Card';
// We import beautiful, professional icons to enhance our UI
import { 
  FaArrowUp, FaArrowDown, FaExchangeAlt, FaGem, FaExclamationTriangle, 
  FaShieldAlt, FaBullseye, FaChartLine, FaMoneyBillWave, FaCrosshairs, FaStopCircle 
} from 'react-icons/fa';

// --- Styled Components & Animations ---

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const AnalysisGrid = styled.div`
  display: grid;
  gap: 1.5rem;
  animation: ${fadeIn} 0.5s ease-out;
`;

// --- 1. THE VERDICT CARD STYLES ---
const VerdictCard = styled(Card)`
  text-align: center;
  border-left: 4px solid ${({ color }) => color};
  box-shadow: 0 4px 15px ${({ color }) => color}22;
`;

const TrendDisplay = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: ${({ color }) => color};
`;

const ContentText = styled.p`
  font-size: 1rem;
  color: var(--color-text-secondary);
  line-height: 1.7;
`;

const ConclusionText = styled(ContentText)`
  font-size: 1.1rem;
  font-style: italic;
  color: var(--color-text-primary);
  max-width: 85%;
  margin: 0 auto;
`;

// --- 2. THE NEW "TRADE TICKET" STYLES ---
const TradeTicket = styled.div`
  background: linear-gradient(135deg, rgba(22, 27, 34, 0.95), rgba(30, 41, 59, 0.95));
  border: 1px solid ${({ action }) => (action === 'BUY' ? 'var(--color-success)' : action === 'SELL' ? 'var(--color-danger)' : 'var(--color-border)')};
  border-radius: 16px;
  padding: 2rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  
  /* Watermark effect in background */
  &::before {
    content: '${({ action }) => action}';
    position: absolute;
    top: -10px;
    right: -10px;
    font-size: 6rem;
    font-weight: 900;
    opacity: 0.05;
    color: ${({ action }) => (action === 'BUY' ? 'var(--color-success)' : action === 'SELL' ? 'var(--color-danger)' : '#FFF')};
    pointer-events: none;
  }
`;

const TicketHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  padding-bottom: 1rem;
`;

const ActionBadge = styled.span`
  background-color: ${({ action }) => (action === 'BUY' ? 'rgba(16, 185, 129, 0.2)' : action === 'SELL' ? 'rgba(239, 68, 68, 0.2)' : 'rgba(100, 116, 139, 0.2)')};
  color: ${({ action }) => (action === 'BUY' ? 'var(--color-success)' : action === 'SELL' ? 'var(--color-danger)' : '#94A3B8')};
  border: 1px solid ${({ action }) => (action === 'BUY' ? 'var(--color-success)' : action === 'SELL' ? 'var(--color-danger)' : '#94A3B8')};
  padding: 0.5rem 1.5rem;
  border-radius: 50px;
  font-weight: 800;
  font-size: 1.2rem;
  letter-spacing: 1px;
  box-shadow: 0 0 15px ${({ action }) => (action === 'BUY' ? 'rgba(16, 185, 129, 0.2)' : action === 'SELL' ? 'rgba(239, 68, 68, 0.2)' : 'transparent')};
`;

const TradeMetricGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
`;

const TradeMetric = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
`;

const MetricLabel = styled.span`
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--color-text-secondary);
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 5px;
`;

const MetricValue = styled.span`
  font-size: 1.3rem;
  font-weight: 700;
  color: ${({ color }) => color || 'var(--color-text-primary)'};
`;

const RationaleBox = styled.div`
  background: rgba(255,255,255,0.03);
  padding: 1rem;
  border-radius: 8px;
  border-left: 3px solid var(--color-primary);
`;

// --- 3. DETAILS GRID STYLES ---
const DetailsGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  @media (max-width: 992px) {
    grid-template-columns: 1fr;
  }
`;

const InfoCard = styled(Card)`
  background-color: var(--color-background);
`;

const SectionTitle = styled.h4`
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
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

  & > svg {
    flex-shrink: 0;
    margin-top: 5px;
    color: var(--color-primary);
  }
`;

// --- The React Component ---

const ChartAnalysis = ({ analysisData }) => {

  // --- The Parser: Extracts data for both the Verdict and the Trade Ticket ---
  const parsedAnalysis = useMemo(() => {
    if (!analysisData || typeof analysisData !== 'string') {
      return null;
    }
    const sections = {};
    // Extended keywords list to capture the new Trade Ticket fields
    const keywords = [
        'TREND:', 'TIMEFRAME:', 'PATTERNS:', 'LEVELS:', 'VOLUME:', 'INDICATORS:', 'CONCLUSION:', 
        'ACTION:', 'ENTRY_ZONE:', 'STOP_LOSS:', 'TARGET_1:', 'TARGET_2:', 'RISK_REWARD:', 'CONFIDENCE:', 'RATIONALE:'
    ];
    
    let currentKey = null;
    let contentBuffer = [];

    analysisData.split('\n').forEach(line => {
      const foundKeyword = keywords.find(kw => line.startsWith(kw));
      if (foundKeyword) {
        if (currentKey) {
          sections[currentKey] = contentBuffer.join('\n').trim();
        }
        currentKey = foundKeyword.replace(':', '').trim(); // Remove colon
        contentBuffer = [line.replace(foundKeyword, '').trim()]; // Remove keyword from content
      } else if (currentKey) {
        contentBuffer.push(line.trim());
      }
    });
    if (currentKey) {
      sections[currentKey] = contentBuffer.join('\n').trim();
    }
    return sections;
  }, [analysisData]);

  const getTrendInfo = () => {
    const trend = parsedAnalysis?.TREND?.toLowerCase() || '';
    if (trend.includes('uptrend')) return { Icon: FaArrowUp, color: 'var(--color-success)', text: 'Primary Uptrend' };
    if (trend.includes('downtrend')) return { Icon: FaArrowDown, color: 'var(--color-danger)', text: 'Primary Downtrend' };
    return { Icon: FaExchangeAlt, color: 'var(--color-text-secondary)', text: 'Sideways / Consolidation' };
  };

  if (!parsedAnalysis) {
    return <Card><p>AI Chart Analysis data is not available.</p></Card>;
  }

  const { Icon: TrendIcon, color: trendColor, text: trendText } = getTrendInfo();
  const action = parsedAnalysis.ACTION ? parsedAnalysis.ACTION.toUpperCase() : 'WAIT';

  return (
    <AnalysisGrid>
      
      {/* --- 1. VERDICT CARD --- */}
      <VerdictCard color={trendColor}>
        <TrendDisplay color={trendColor}>
          <TrendIcon />
          {trendText}
        </TrendDisplay>
        <ConclusionText>
          "{parsedAnalysis.CONCLUSION || 'No conclusive summary available.'}"
        </ConclusionText>
      </VerdictCard>

      {/* --- 2. TRADE TICKET (New High-End Feature) --- */}
      {parsedAnalysis.ENTRY_ZONE && (
          <TradeTicket action={action}>
            <TicketHeader>
                <div>
                    <div style={{fontSize: '0.8rem', color: 'var(--color-text-secondary)', marginBottom: '5px', letterSpacing: '1px'}}>STRATEGY SIGNAL</div>
                    <ActionBadge action={action}>{action}</ActionBadge>
                </div>
                <div style={{textAlign: 'right'}}>
                    <div style={{fontSize: '0.8rem', color: 'var(--color-text-secondary)', marginBottom: '5px', letterSpacing: '1px'}}>AI CONFIDENCE</div>
                    <div style={{fontSize: '1.2rem', fontWeight: 'bold', color: 'var(--color-text-primary)'}}>{parsedAnalysis.CONFIDENCE}</div>
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
                <strong style={{color: 'var(--color-primary)', display: 'block', marginBottom: '0.5rem'}}>Trade Rationale:</strong>
                <span style={{color: 'var(--color-text-secondary)', lineHeight: '1.6'}}>{parsedAnalysis.RATIONALE}</span>
            </RationaleBox>
          </TradeTicket>
      )}
      
      {/* --- 3. DETAILS GRID --- */}
      <DetailsGrid>
        <InfoCard>
          <SectionTitle><FaGem /> Key Patterns</SectionTitle>
          <InfoList>
            {parsedAnalysis.PATTERNS?.split('\n').map((item, index) => (
              <InfoListItem key={index}><FaChartLine /> {item}</InfoListItem>
            ))}
          </InfoList>
        </InfoCard>

        <InfoCard>
          <SectionTitle><FaExclamationTriangle /> Volume & Indicators</SectionTitle>
          <InfoList>
            <InfoListItem><strong>Volume:</strong> {parsedAnalysis.VOLUME}</InfoListItem>
            <InfoListItem><strong>Indicators:</strong> {parsedAnalysis.INDICATORS}</InfoListItem>
          </InfoList>
        </InfoCard>
      </DetailsGrid>

      <InfoCard>
        <SectionTitle>Key Price Levels</SectionTitle>
        <DetailsGrid>
            <div>
                <SectionTitle style={{fontSize: '1rem', color: '#34D399'}}><FaShieldAlt /> Support</SectionTitle>
                <ContentText>{parsedAnalysis.LEVELS}</ContentText> 
                {/* Note: Complex parsing of levels can be added here if the AI output is standardized further */}
            </div>
            <div>
                <SectionTitle style={{fontSize: '1rem', color: '#F87171'}}><FaBullseye /> Resistance</SectionTitle>
                 <ContentText>{parsedAnalysis.LEVELS}</ContentText>
            </div>
        </DetailsGrid>
      </InfoCard>
    </AnalysisGrid>
  );
};

export default ChartAnalysis;