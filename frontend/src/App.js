import React from 'react';
import PureVisionPage from './pages/PureVisionPage';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { GlobalStyles } from './styles/GlobalStyles';
import HomePage from './pages/HomePage';
import StockDetailPage from './pages/StockDetailPage';
// --- NEW: Import our new Index Detail Page ---
import IndexDetailPage from './pages/IndexDetailPage';

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

          {/* Route for the detailed stock analysis page */}
          <Route path="/stock/:symbol" element={<StockDetailPage />} />

          {/* --- NEW ROUTE ADDED HERE --- */}
          {/* Route for the detailed index analysis page. 
              The ":encodedSymbol" will hold the URL-safe version of the index symbol. */}
          <Route path="/index/:encodedSymbol" element={<IndexDetailPage />} />
          <Route path="/vision-result" element={<PureVisionPage />} />

        </Routes>
      </Router>
    </>
  );
}

export default App;