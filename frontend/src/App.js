import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { GlobalStyles } from './styles/GlobalStyles';
import HomePage from './pages/HomePage';
import StockDetailPage from './pages/StockDetailPage';

function App() {
  return (
    <>
      {/* This component injects our beautiful dark theme styles into the entire app */}
      <GlobalStyles />

      {/* The Router handles all page navigation */}
      <Router>
        <Routes>
          {/* Route for the main landing/search page */}
          <Route path="/" element={<HomePage />} />

          {/* Route for the detailed stock analysis page. 
              The ":symbol" part is a dynamic parameter that will hold the stock ticker. 
              e.g., /stock/AAPL or /stock/MSFT */}
          <Route path="/stock/:symbol" element={<StockDetailPage />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;