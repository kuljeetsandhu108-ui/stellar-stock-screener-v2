import React from 'react';
import Card from '../common/Card';
import RevenueChart from './RevenueChart';

// This component is currently a simple wrapper, but it's designed for future expansion.
// We could easily add tabs here for "Income Statement," "Balance Sheet," "Cash Flow," etc.
// to show different charts or tables within the same card.

const Financials = ({ financialData }) => {
  // Defensive check: If there's no data or the data is not an array, don't render anything.
  if (!financialData || !Array.isArray(financialData) || financialData.length === 0) {
    return (
      <Card title="Financials">
        <p>Financial statement data is not available for this stock.</p>
      </Card>
    );
  }

  return (
    // We use our reusable Card component and give it a title.
    <Card title="Financials Overview">
      {/* 
        The content inside this Card is the RevenueChart component.
        We pass the financial data down to the chart as a prop.
      */}
      <RevenueChart data={financialData} />
    </Card>
  );
};

export default Financials;