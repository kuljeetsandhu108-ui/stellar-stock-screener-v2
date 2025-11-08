import React, { useEffect, useRef, memo } from 'react';
import Card from '../common/Card';

const TradingViewChart = ({ symbol }) => {
  const container = useRef();

  useEffect(() => {
    // Ensure the TradingView script is loaded and the container ref is set
    if (window.TradingView && container.current) {
      // Clear the container before creating a new widget
      // This is crucial for preventing duplicate charts when the component re-renders
      container.current.innerHTML = '';

      // Create a new TradingView widget instance
      new window.TradingView.widget({
        autosize: true, // This makes the chart fill its container
        symbol: symbol,
        interval: "D", // Daily interval
        timezone: "Etc/UTC",
        theme: "dark", // Dark theme to match our app
        style: "1",
        locale: "en",
        enable_publishing: false,
        allow_symbol_change: true,
        withdateranges: true,
        hide_side_toolbar: false,
        studies: [
          "Volume@tv-basicstudies" // Add volume as a default study
        ],
        container_id: container.current.id,
      });
    }
  }, [symbol]); // Re-run the effect if the stock symbol changes

  return (
    <Card title="Advanced Chart">
      <div 
        ref={container} 
        id={`tradingview_${symbol}`} 
        style={{ height: "600px", width: "100%" }} 
      />
    </Card>
  );
};

// Use React.memo to prevent unnecessary re-renders of the chart
// The chart will only re-render if its 'symbol' prop changes.
export default memo(TradingViewChart);