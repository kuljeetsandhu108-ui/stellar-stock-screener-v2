import React, { useMemo } from 'react';
import styled, { keyframes } from 'styled-components';
import Card from '../common/Card';
import { NestedTabs, NestedTabPanel } from '../common/Tabs/NestedTabs';
import DarvasScan from './DarvasScan';
import BenjaminGrahamScan from './BenjaminGrahamScan';
import FundamentalConclusion from './FundamentalConclusion';

const fadeIn = keyframes`from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); }`;

const SectionContainer = styled.div`animation: ${fadeIn} 0.5s ease-out; padding: 0.5rem;`;
const SectionTitle = styled.h3`font-size: 1.4rem; font-weight: 600; margin-bottom: 1.5rem; color: var(--color-text-primary);`;
const Loader = styled.div`color: var(--color-primary); height: 200px; display: flex; align-items: center; justify-content: center; font-weight: 500;`;

// --- THE NEW FLAWLESS TABLE UI ---
const TableContainer = styled.div`width: 100%; overflow-x: auto; border-radius: 12px; border: 1px solid var(--color-border); background: var(--color-secondary); box-shadow: 0 4px 20px rgba(0,0,0,0.2);`;
const StyledTable = styled.table`width: 100%; border-collapse: collapse; min-width: 600px;`;
const Th = styled.th`text-align: left; padding: 16px; background: rgba(255, 255, 255, 0.03); color: var(--color-text-secondary); font-weight: 700; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 1px; border-bottom: 1px solid var(--color-border); &:last-child { text-align: right; }`;
const Tr = styled.tr`border-bottom: 1px solid rgba(255, 255, 255, 0.05); transition: background 0.2s; &:last-child { border-bottom: none; } &:hover { background: rgba(255, 255, 255, 0.02); }`;
const Td = styled.td`padding: 16px; font-size: 0.95rem; color: #C9D1D9; vertical-align: top; line-height: 1.6;`;

const StatusTag = styled.span`
  display: inline-flex; align-items: center; padding: 6px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; white-space: nowrap;
  background: ${({ status }) => status.includes('PASS') || status.includes('BUY') || status.includes('WIDE') ? 'rgba(57, 211, 83, 0.1)' : status.includes('FAIL') || status.includes('SELL') || status.includes('NO') || status.includes('OVER') ? 'rgba(248, 81, 73, 0.1)' : 'rgba(235, 203, 139, 0.1)'};
  color: ${({ status }) => status.includes('PASS') || status.includes('BUY') || status.includes('WIDE') ? '#3FB950' : status.includes('FAIL') || status.includes('SELL') || status.includes('NO') || status.includes('OVER') ? '#F85149' : '#EBCB8B'};
  border: 1px solid ${({ status }) => status.includes('PASS') || status.includes('BUY') || status.includes('WIDE') ? '#3FB950' : status.includes('FAIL') || status.includes('SELL') || status.includes('NO') || status.includes('OVER') ? '#F85149' : '#EBCB8B'};
`;

const PiotroskiGrid = styled.div`display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; align-items: center; @media (max-width: 768px) { grid-template-columns: 1fr; }`;
const ScoreCard = styled.div`display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2rem; background: rgba(255,255,255,0.02); border-radius: 50%; width: 180px; height: 180px; margin: 0 auto; border: 4px solid ${({ color }) => color}; box-shadow: 0 0 30px ${({ color }) => color}22;`;
const CriteriaList = styled.ul`list-style: none; padding: 0; li { margin-bottom: 0.8rem; display: flex; align-items: center; color: var(--color-text-secondary); &::before { content: '✓'; color: #3FB950; margin-right: 10px; font-weight: bold; } }`;

// Deep parsing logic ensures strings are chopped exactly at the | line
const parseTableData = (text) => {
    if (!text) return[];
    const normalized = text.replace(/\\\\n/g, '\n');
    return normalized.split('\n').filter(line => line.includes('|')).map(line => {
        const parts = line.split('|');
        const clean = (str) => str ? str.replace(/\*/g, '').trim() : '';
        return { col1: clean(parts[0]), col2: clean(parts[1]), col3: clean(parts[2]) };
    });
};

const Fundamentals = ({ symbol, profile, quote, keyMetrics, piotroskiData, darvasScanData, grahamScanData, quarterlyEarnings, annualEarnings, shareholding, philosophyAssessment, canslimAssessment, conclusion, isLoadingPhilosophy, isLoadingCanslim, isLoadingConclusion }) => {
  const canslimRows = useMemo(() => parseTableData(canslimAssessment),[canslimAssessment]);
  const valueRows = useMemo(() => parseTableData(philosophyAssessment),[philosophyAssessment]);
  const { score = 0, criteria =[] } = piotroskiData || {};
  const scoreColor = score >= 7 ? '#3FB950' : score >= 4 ? '#EDBB5A' : '#F85149';

  return (
    <Card>
      <NestedTabs>
        <NestedTabPanel label="Conclusion">
          <SectionContainer>
            {isLoadingConclusion ? <Loader>Calculating Final Verdict...</Loader> : <FundamentalConclusion conclusionData={conclusion} />}
          </SectionContainer>
        </NestedTabPanel>

        <NestedTabPanel label="CANSLIM">
          <SectionContainer>
            <SectionTitle>CANSLIM Checklist</SectionTitle>
            {isLoadingCanslim ? <Loader>Running Quantitative Strategy...</Loader> : (
              <TableContainer>
                <StyledTable>
                  <thead>
                    <tr>
                      <Th style={{width: '25%'}}>Criteria</Th>
                      <Th style={{width: '55%'}}>Quantitative Assessment</Th>
                      <Th style={{width: '20%', textAlign: 'right'}}>Verdict</Th>
                    </tr>
                  </thead>
                  <tbody>
                    {canslimRows.map((row, i) => (
                      <Tr key={i}>
                        <Td style={{fontWeight: '600', color: 'var(--color-primary)', borderRight: '1px solid rgba(255,255,255,0.05)'}}>
                            {row.col1}
                        </Td>
                        <Td>{row.col2}</Td>
                        <Td style={{textAlign: 'right'}}>
                            {/* Renders the perfect Green/Red pill and strips out emojis for cleanliness */}
                            {row.col3 && <StatusTag status={row.col3}>{row.col3.replace(/[❌✅⚠️]/g, '').trim()}</StatusTag>}
                        </Td>
                      </Tr>
                    ))}
                  </tbody>
                </StyledTable>
              </TableContainer>
            )}
          </SectionContainer>
        </NestedTabPanel>

        <NestedTabPanel label="Value Investing">
          <SectionContainer>
            <SectionTitle>Valuation Models</SectionTitle>
            {isLoadingPhilosophy ? <Loader>Computing Intrinsic Value...</Loader> : (
              <TableContainer>
                <StyledTable>
                  <thead>
                    <tr>
                      <Th style={{width: '35%'}}>Formula / Strategy</Th>
                      <Th>Mathematical Analysis</Th>
                    </tr>
                  </thead>
                  <tbody>
                    {valueRows.map((row, i) => (
                      <Tr key={i}>
                        <Td style={{fontWeight: '600', color: 'var(--color-primary)', borderRight: '1px solid rgba(255,255,255,0.05)'}}>
                            {row.col1}
                        </Td>
                        <Td>
                            <span style={{fontWeight: '500'}}>{row.col2}</span>
                        </Td>
                      </Tr>
                    ))}
                  </tbody>
                </StyledTable>
              </TableContainer>
            )}
          </SectionContainer>
        </NestedTabPanel>

        <NestedTabPanel label="Piotroski Score">
          <SectionContainer>
            <SectionTitle>Piotroski F-Score (Financial Health)</SectionTitle>
            <PiotroskiGrid>
              <ScoreCard color={scoreColor}>
                <span style={{fontSize: '4rem', fontWeight: 800, color: scoreColor}}>{score}</span>
                <span style={{color: '#8B949E'}}>/ 9</span>
              </ScoreCard>
              <div>
                <p style={{marginBottom: '1rem', color: '#C9D1D9'}}>Scores based on 9 points of Profitability, Leverage, and Operating Efficiency.</p>
                <CriteriaList>
                  {criteria.map((item, i) => <li key={i}>{item}</li>)}
                </CriteriaList>
              </div>
            </PiotroskiGrid>
          </SectionContainer>
        </NestedTabPanel>

        <NestedTabPanel label="Graham Scan">
          <SectionContainer>
            <BenjaminGrahamScan scanData={grahamScanData} />
          </SectionContainer>
        </NestedTabPanel>

        <NestedTabPanel label="Darvas Scan">
          <SectionContainer>
            <SectionTitle>Darvas Box Momentum</SectionTitle>
            <DarvasScan scanData={darvasScanData} currency={profile?.currency} />
          </SectionContainer>
        </NestedTabPanel>
      </NestedTabs>
    </Card>
  );
};

export default Fundamentals;
