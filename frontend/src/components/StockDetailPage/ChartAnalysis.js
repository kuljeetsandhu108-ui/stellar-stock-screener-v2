import React, { useMemo } from 'react';
import styled, { keyframes } from 'styled-components';
import Card from '../common/Card';
// We import beautiful, professional icons to enhance our UI
import { FaArrowUp, FaArrowDown, FaExchangeAlt, FaGem, FaExclamationTriangle, FaShieldAlt, FaBullseye, FaChartLine } from 'react-icons/fa';

// --- Styled Components & Animations for our "Extreme Graphics" UI ---

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const AnalysisGrid = styled.div`
  display: grid;
  gap: 1.5rem;
  animation: ${fadeIn} 0.5s ease-out;
`;

const VerdictCard = styled(Card)`
  text-align: center;
  /* Add a vibrant border based on the trend direction */
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
  max-width: 80%;
  margin: 0 auto;
`;

const DetailsGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  @media (max-width: 992px) {
    grid-template-columns: 1fr;
  }
`;

const InfoCard = styled(Card)`
  background-color: var(--color-background); /* Slightly darker for contrast */
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

// --- The New Masterpiece Component ---

const ChartAnalysis = ({ analysisData }) => {

  // This "parser" is the brain. It takes the raw AI text and splits it into a structured object.
  const parsedAnalysis = useMemo(() => {
    if (!analysisData || typeof analysisData !== 'string') {
      return null;
    }
    const sections = {};
    const keywords = ['TREND:', 'PATTERNS:', 'LEVELS:', 'VOLUME:', 'INDICATORS:', 'CONCLUSION:'];
    let currentKey = null;
    let contentBuffer = [];

    analysisData.split('\n').forEach(line => {
      const foundKeyword = keywords.find(kw => line.startsWith(kw));
      if (foundKeyword) {
        if (currentKey) {
          sections[currentKey] = contentBuffer.join('\n').trim();
        }
        currentKey = foundKeyword.replace(':', '').trim();
        contentBuffer = [line.replace(foundKeyword, '').trim()];
      } else if (currentKey) {
        contentBuffer.push(line.trim());
      }
    });
    if (currentKey) {
      sections[currentKey] = contentBuffer.join('\n').trim();
    }
    return sections;
  }, [analysisData]);

  // This helper function determines which icon and color to use for the trend.
  const getTrendInfo = () => {
    const trend = parsedAnalysis?.TREND?.toLowerCase() || '';
    if (trend.includes('uptrend')) {
      return { Icon: FaArrowUp, color: 'var(--color-success)', text: 'Primary Uptrend' };
    }
    if (trend.includes('downtrend')) {
      return { Icon: FaArrowDown, color: 'var(--color-danger)', text: 'Primary Downtrend' };
    }
    return { Icon: FaExchangeAlt, color: 'var(--color-text-secondary)', text: 'Sideways Consolidation' };
  };

  if (!parsedAnalysis) {
    return (
      <Card>
        <p>AI Chart Analysis data is not available or is in an invalid format.</p>
      </Card>
    );
  }

  const { Icon: TrendIcon, color: trendColor, text: trendText } = getTrendInfo();

  return (
    <AnalysisGrid>
      <VerdictCard color={trendColor}>
        <TrendDisplay color={trendColor}>
          <TrendIcon />
          {trendText}
        </TrendDisplay>
        <ConclusionText>
          "{parsedAnalysis.CONCLUSION || 'No conclusive summary available.'}"
        </ConclusionText>
      </VerdictCard>
      
      <DetailsGrid>
        <InfoCard>
          <SectionTitle><FaGem /> Key Patterns</SectionTitle>
          <InfoList>
            {/* We split the PATTERNS text into bullet points for a cleaner display */}
            {parsedAnalysis.PATTERNS?.split('\n').map((item, index) => (
              <InfoListItem key={`pattern-${index}`}><FaChartLine /> {item}</InfoListItem>
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
        <SectionTitle>Price Levels</SectionTitle>
        <DetailsGrid>
            <div>
                <SectionTitle style={{fontSize: '1rem'}}><FaShieldAlt /> Key Support</SectionTitle>
                <InfoList>
                    {/* A smart parser to find and list support levels from the text */}
                    {parsedAnalysis.LEVELS?.toLowerCase().includes('support at') 
                      ? parsedAnalysis.LEVELS.toLowerCase().split('support at')[1].split('resistance at')[0].trim().split(',').map((level, index) => (
                          level.trim() && <InfoListItem key={`support-${index}`}>{level.trim()}</InfoListItem>
                        ))
                      : <InfoListItem>Not specified.</InfoListItem>
                    }
                </InfoList>
            </div>
            <div>
                <SectionTitle style={{fontSize: '1rem'}}><FaBullseye /> Key Resistance</SectionTitle>
                <InfoList>
                    {/* A smart parser to find and list resistance levels from the text */}
                    {parsedAnalysis.LEVELS?.toLowerCase().includes('resistance at') 
                      ? parsedAnalysis.LEVELS.toLowerCase().split('resistance at')[1].trim().split(',').map((level, index) => (
                          level.trim() && <InfoListItem key={`resist-${index}`}>{level.trim()}</InfoListItem>
                        ))
                      : <InfoListItem>Not specified.</InfoListItem>
                    }
                </InfoList>
            </div>
        </DetailsGrid>
      </InfoCard>
    </AnalysisGrid>
  );
};

export default ChartAnalysis;