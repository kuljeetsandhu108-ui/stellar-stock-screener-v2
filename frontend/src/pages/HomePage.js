import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';
import { FaSearch } from 'react-icons/fa';
import IndicesBanner from '../components/Indices/IndicesBanner';
import ChartUploader from '../components/HomePage/ChartUploader';

// --- 1. ANIMATIONS (Unchanged) ---
const fadeIn = keyframes`from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); }`;
const float = keyframes`0% { transform: translate(0px, 0px) scale(1); } 33% { transform: translate(30px, -50px) scale(1.1); } 66% { transform: translate(-20px, 20px) scale(0.9); } 100% { transform: translate(0px, 0px) scale(1); }`;
const floatReverse = keyframes`0% { transform: translate(0px, 0px) scale(1); } 33% { transform: translate(-30px, 50px) scale(0.9); } 66% { transform: translate(20px, -20px) scale(1.1); } 100% { transform: translate(0px, 0px) scale(1); }`;

// --- 2. STYLED COMPONENTS ---

const HomePageContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
  width: 100%;
  position: relative;
  overflow-x: hidden;
  @media (min-width: 768px) { padding: 2rem; }
`;

const BackgroundLayer = styled.div`position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; pointer-events: none; overflow: hidden;`;
const GlowingBlob = styled.div`position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.4; animation: ${float} 10s ease-in-out infinite;`;
const BlobOne = styled(GlowingBlob)`top: -10%; left: -10%; width: 50vw; height: 50vw; background: var(--color-primary); animation-delay: 0s;`;
const BlobTwo = styled(GlowingBlob)`bottom: -10%; right: -10%; width: 60vw; height: 60vw; background: #7c3aed; animation: ${floatReverse} 12s ease-in-out infinite;`;

const MainContent = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    width: 100%;
    margin-top: 2vh;
    z-index: 1;
    @media (min-width: 768px) { margin-top: 5vh; }
`;

const Title = styled.h1`font-size: 2.5rem; font-weight: 800; color: var(--color-text-primary); margin-bottom: 1rem; animation: ${fadeIn} 1s ease-out; letter-spacing: -1px; text-shadow: 0 4px 20px rgba(0,0,0,0.3); @media (min-width: 768px) { font-size: 4.5rem; letter-spacing: -2px; }`;
const Subtitle = styled.p`font-size: 1rem; color: var(--color-text-secondary); margin-bottom: 2rem; max-width: 600px; animation: ${fadeIn} 1.5s ease-out; padding: 0 1rem;`;

// --- NEW: SEARCH STYLES WITH DROPDOWN ---

const SearchSection = styled.div`
  width: 100%;
  max-width: 650px;
  position: relative; /* Crucial for absolute positioning of dropdown */
  animation: ${fadeIn} 1.8s ease-out;
`;

const SearchWrapper = styled.div`
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
  z-index: 10; /* Ensure search bar is above other content */
`;

const SearchInput = styled.input`
  width: 100%;
  padding: 15px 20px;
  padding-right: 60px;
  font-size: 1rem;
  color: var(--color-text-primary);
  background-color: rgba(22, 27, 34, 0.8); 
  backdrop-filter: blur(10px);
  border: 1px solid var(--color-border);
  border-radius: 50px; /* When dropdown is open, we might want to change this, but 50px is fine */
  outline: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);

  &:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 20px rgba(88, 166, 255, 0.4);
    background-color: rgba(22, 27, 34, 0.95);
  }

  @media (min-width: 768px) {
    padding: 20px 30px;
    padding-right: 70px;
    font-size: 1.2rem;
  }
`;

const SearchButton = styled.button`
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background-color: var(--color-primary);
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.1s ease;

  &:hover { background-color: #4FA0EE; transform: translateY(-50%) scale(1.05); }
  &:active { transform: translateY(-50%) scale(0.95); }
  @media (min-width: 768px) { width: 48px; height: 48px; right: 10px; }
`;

// --- THE NEW DROPDOWN STYLES ---
const SuggestionsList = styled.ul`
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 10px;
  background-color: rgba(22, 27, 34, 0.95);
  backdrop-filter: blur(12px);
  border: 1px solid var(--color-border);
  border-radius: 15px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.5);
  list-style: none;
  padding: 0;
  max-height: 300px;
  overflow-y: auto;
  z-index: 100; /* Must be on top of everything */
  
  /* Custom Scrollbar */
  &::-webkit-scrollbar { width: 6px; }
  &::-webkit-scrollbar-thumb { background: var(--color-border); border-radius: 3px; }
`;

const SuggestionItem = styled.li`
  padding: 12px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.2s;

  &:last-child { border-bottom: none; }
  &:hover { background-color: rgba(88, 166, 255, 0.15); }
`;

const SuggestionSymbol = styled.span`
  font-weight: 700;
  color: var(--color-primary);
  font-family: 'Roboto Mono', monospace;
`;

const SuggestionName = styled.span`
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  margin-left: 10px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 60%;
`;

const SuggestionExchange = styled.span`
  font-size: 0.75rem;
  background-color: var(--color-border);
  padding: 2px 6px;
  border-radius: 4px;
  color: var(--color-text-secondary);
`;

const LoadingText = styled.p`color: var(--color-primary); margin-top: 1rem; height: 20px; font-weight: 500;`;

// --- 3. THE COMPONENT ---

const HomePage = () => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  
  // Ref to help with clicking outside to close
  const searchRef = useRef(null);

  // --- DEBOUNCE LOGIC FOR AUTOCOMPLETE ---
  useEffect(() => {
    // Don't search if query is too short
    if (query.length < 2) {
      setSuggestions([]);
      return;
    }

    // Set a delay (debounce) to avoid spamming the API while typing
    const delayDebounceFn = setTimeout(async () => {
      try {
        // Call our new fast autocomplete endpoint
        const response = await axios.get(`/api/stocks/autocomplete?query=${query}`);
        setSuggestions(response.data);
        setShowSuggestions(true);
      } catch (error) {
        console.error("Autocomplete error:", error);
      }
    }, 300); // Wait 300ms after user stops typing

    return () => clearTimeout(delayDebounceFn);
  }, [query]);


  // --- SEARCH HANDLERS ---

  const performSearch = async (searchQuery = query) => {
    // If user clicked a suggestion, use that symbol directly.
    // Otherwise use what's typed.
    const target = searchQuery.trim();

    if (target !== '') {
      setIsLoading(true);
      setError('');
      setShowSuggestions(false); // Hide dropdown
      try {
        // If it looks like a symbol (from dropdown), go direct.
        // If it's raw text, use the AI search.
        // A simple heuristic: if we clicked a suggestion, we pass the symbol.
        
        // For now, we stick to the AI search for robustness unless we are sure it is a symbol
        const response = await axios.get(`/api/stocks/search?query=${target}`);
        const symbol = response.data.symbol;
        navigate(`/stock/${symbol}`);
      } catch (err) {
        setError('Could not find a stock for that query. Please try again.');
        console.error("Search failed:", err);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleSuggestionClick = (symbol) => {
    setQuery(symbol); // Update input box
    setSuggestions([]); // Clear suggestions
    navigate(`/stock/${symbol}`); // Go directly to the page! Faster than AI search.
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      performSearch();
    }
  };

  // Close suggestions if clicked outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [searchRef]);

  return (
    <HomePageContainer>
      <BackgroundLayer><BlobOne /><BlobTwo /></BackgroundLayer>
      <IndicesBanner />
      <MainContent>
        <Title>Stellar Stock Screener</Title>
        <Subtitle>Leveraging AI to provide comprehensive financial insights.</Subtitle>
        
        <SearchSection ref={searchRef}>
          <SearchWrapper>
            <SearchInput
              type="text"
              placeholder="Search for a company (e.g. Apple, Tata Motors)..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              onFocus={() => query.length >= 2 && setShowSuggestions(true)}
              disabled={isLoading}
            />
            <SearchButton onClick={() => performSearch()} disabled={isLoading} aria-label="Search">
              <FaSearch size={18} />
            </SearchButton>
          </SearchWrapper>

          {/* --- THE SUGGESTIONS DROPDOWN --- */}
          {showSuggestions && suggestions.length > 0 && (
            <SuggestionsList>
              {suggestions.map((item) => (
                <SuggestionItem key={item.symbol} onClick={() => handleSuggestionClick(item.symbol)}>
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <SuggestionSymbol>{item.symbol}</SuggestionSymbol>
                    <SuggestionName>{item.name}</SuggestionName>
                  </div>
                  <SuggestionExchange>{item.exchangeShortName}</SuggestionExchange>
                </SuggestionItem>
              ))}
            </SuggestionsList>
          )}
        </SearchSection>

        <LoadingText>{isLoading ? 'Searching with AI...' : error || ''}</LoadingText>
        <p style={{ color: 'var(--color-text-secondary)', margin: '2rem 0', fontWeight: '500' }}>OR</p>
        <ChartUploader />
      </MainContent>
    </HomePageContainer>
  );
};

export default HomePage;