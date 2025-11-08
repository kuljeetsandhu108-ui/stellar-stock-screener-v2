import React from 'react';
import styled from 'styled-components';
import Card from '../common/Card';
import DonutChart from './DonutChart';
import TrendChart from './TrendChart';

// --- Styled Components ---

const GridContainer = styled.div`
  display: grid;
  /* Create two columns of equal width */
  grid-template-columns: 1fr 1fr; 
  gap: 2rem; /* Space between the two charts */
  align-items: center; /* Vertically align the content */
  
  /* On smaller screens, stack the charts on top of each other */
  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
  }
`;

const ChartContainer = styled.div`
  width: 100%;
`;

const SectionTitle = styled.h3`
    font-size: 1.2rem;
    font-weight: 500;
    color: var(--color-text-secondary);
    text-align: center;
    margin-bottom: 2rem;
`;

// --- React Component ---

const Shareholding = ({ shareholdingData }) => {

  // Defensive check: If data is missing or empty, show a message instead of the charts.
  if (!shareholdingData || !Array.isArray(shareholdingData) || shareholdingData.length === 0) {
    return (
      <Card title="Shareholding">
        <p>Shareholding data is not available for this stock.</p>
      </Card>
    );
  }

  return (
    // We use our reusable Card component with a title
    <Card title="Shareholding">
      <GridContainer>
        
        {/* Left Column: Summary Donut Chart */}
        <ChartContainer>
          <SectionTitle>Summary</SectionTitle>
          <DonutChart data={shareholdingData} />
        </ChartContainer>

        {/* Right Column: Trend Bar Chart */}
        <ChartContainer>
           <TrendChart />
        </ChartContainer>

      </GridContainer>
    </Card>
  );
};

export default Shareholding;