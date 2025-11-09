import React from 'react';
import styled from 'styled-components';

// --- Import all our components ---
import Card from '../common/Card';
import RevenueChart from './RevenueChart';
import KeyStats from './KeyStats';
import AboutCompany from './AboutCompany';

// --- Styled Components ---

const FinancialsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem; /* Adds space between each section */
`;

// --- The Refactored React Component ---

const Financials = ({ profile, quote, keyMetrics, keyStats, financialData }) => {
  // Defensive check: If we don't have the core profile data, show a generic message.
  if (!profile) {
    return (
      <Card>
        <p>Financial data is not available for this stock.</p>
      </Card>
    );
  }

  return (
    // We use a single, borderless Card for a cleaner, integrated look within the tab
    <Card>
      <FinancialsContainer>

        {/* --- Section 1: Key Stats --- */}
        {/* Pass the consolidated keyStats object we created in the backend */}
        <KeyStats stats={keyStats} />

        {/* --- Section 2: Financials Overview Chart --- */}
        <div>
            <h3 style={{ fontSize: '1.5rem', fontWeight: 600, marginBottom: '1.5rem' }}>Financials Overview</h3>
            <RevenueChart data={financialData} />
        </div>

        {/* --- Section 3: About the Company --- */}
        <AboutCompany profile={profile} />

      </FinancialsContainer>
    </Card>
  );
};

export default Financials;