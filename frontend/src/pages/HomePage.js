import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';
import { FaSearch, FaChartBar, FaGlobeAmericas, FaSpinner, FaBitcoin } from 'react-icons/fa';

// --- COMPONENTS ---
import IndicesBanner from '../components/Indices/IndicesBanner';
import ChartUploader from '../components/HomePage/ChartUploader';

// --- ANIMATIONS ---
const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const float = keyframes`
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
`;

const floatReverse = keyframes`
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(-30px, 50px) scale(0.9); }
  66% { transform: translate(20px, -20px) scale(1.1); } 
  100% { transform: translate(0px, 0px) scale(1); }
`;

// --- STYLED COMPONENTS ---

const HomePageContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
  width: 100%;
  position: relative;
  overflow-x: hidden;
  
  @media (min-width: 768px) {
    padding: 2rem;
  }
`;

const BackgroundLayer = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
  overflow: hidden;
`;

const GlowingBlob = styled.div`
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: ${float} 10s ease-in-out infinite;
`;

const BlobOne = styled(GlowingBlob)`
  top: -10%;
  left: -10%;
  width: 50vw;
  height: 50vw;
  background: var(--color-primary);
  animation-delay: 0s;
`;

const BlobTwo = styled(GlowingBlob)`
  bottom: -10%;
  right: -10%;
  width: 60vw;
  height: 60vw;
  background: #7c3aed; /* Deep Purple */
  animation: ${floatReverse} 12s ease-in-out infinite;
`;

const MainContent = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    width: 100%;
    margin-top: 5vh;
    z-index: 1;
    
    @media (min-width: 768px) {
        margin-top: 8vh;
    }
`;

const Title = styled.h1`
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--color-text-primary);
  margin-bottom: 1rem;
  animation: ${fadeIn} 1s ease-out;
  letter-spacing: -1px;
  text-shadow: 0 4px 30px rgba(0,0,0,0.5);
  
  @media (min-width: 768px) {
    font-size: 4.5rem;
    letter-spacing: -2px;
  }
`;

const Subtitle = styled.p`
  font-size: 1rem;
  color: var(--color-text-secondary);
  margin-bottom: 3rem;
  max-width: 600px;
  animation: ${fadeIn} 1.5s ease-out;
  padding: 0 1rem;
  line-height: 1.6;
  
  @media (min-width: 768px) {
    font-size: 1.2rem;
  }
`;

// --- SEARCH SECTION (High End Glassmorphism) ---

const SearchSection = styled.div`
  width: 100%;
  max-width: 650px;
  position: relative;
  animation: ${fadeIn} 1.8s ease-out;
  z-index: 100;
`;

const SearchWrapper = styled.div`
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
`;

const SearchInput = styled.input`
  width: 100%;
  padding: 18px 25px;
  padding-right: 70px;
  font-size: 1.1rem;
  color: var(--color-text-primary);
  background-color: rgba(22, 27, 34, 0.7); 
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 50px;
  outline: none;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);

  &::placeholder {
    color: rgba(255, 255, 255, 0.3);
  }

  &:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 25px rgba(88, 166, 255, 0.2);
    background-color: rgba(22, 27, 34, 0.95);
    transform: scale(1.02);
  }
`;

const SearchButton = styled.button`
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: linear-gradient(135deg, var(--color-primary), #3b82f6);
  color: white;
  border: none;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);

  &:hover {
    transform: translateY(-50%) scale(1.1);
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
  }
  
  &:active {
    transform: translateY(-50%) scale(0.95);
  }

  &:disabled {
      opacity: 0.8;
      cursor: default;
  }
`;

// --- AUTOCOMPLETE DROPDOWN ---

const SuggestionsList = styled.ul`
  position: absolute;
  top: 100%;
  left: 15px;
  right: 15px;
  margin-top: 15px;
  background-color: rgba(22, 27, 34, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.6);
  list-style: none;
  padding: 0;
  max-height: 350px;
  overflow-y: auto;
  z-index: 101;
  
  &::-webkit-scrollbar { width: 6px; }
  &::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
  &::-webkit-scrollbar-track { background: transparent; }
`;

const SuggestionItem = styled.li`
  padding: 14px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.2s ease;

  &:last-child { border-bottom: none; }
  
  &:hover { 
    background-color: rgba(88, 166, 255, 0.15); 
    padding-left: 25px;
  }
`;

const ItemLeft = styled.div`
  display: flex;
  flex-direction: column;
`;

const SuggestionSymbol = styled.span`
  font-weight: 700;
  font-size: 1rem;
  color: var(--color-primary);
  font-family: 'Roboto Mono', monospace;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const SuggestionName = styled.span`
  font-size: 0.85rem;
  color: var(--color-text-secondary);
  margin-top: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 300px;
`;

const SuggestionBadge = styled.span`
  font-size: 0.7rem;
  background-color: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  padding: 4px 8px;
  border-radius: 6px;
  color: var(--color-text-secondary);
  font-weight: 600;
  text-transform: uppercase;
`;

const LoadingText = styled.p`
  color: var(--color-primary); 
  margin-top: 1.5rem; 
  height: 20px; 
  font-weight: 600;
  letter-spacing: 0.5px;
  font-size: 0.9rem;
`;

// --- TRIPLE AI UPLOADER GRID ---
const UploadGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  width: 100%;
  max-width: 1200px;
  margin-top: 4rem;
  padding: 0 1rem;
  animation: ${fadeIn} 2s ease-out;

  @media (max-width: 1024px) {
    grid-template-columns: 1fr; /* Stack on mobile/tablet */
    gap: 1.5rem;
    max-width: 500px;
  }
`;

const SectionLabel = styled.p`
  color: var(--color-text-secondary);
  margin: 2rem 0;
  font-weight: 500;
  opacity: 0.6;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 0.8rem;
`;

// --- MAIN COMPONENT LOGIC ---

const HomePage = () => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isAutoCompleting, setIsAutoCompleting] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [error, setError] = useState('');
  
  const navigate = useNavigate();
  const searchRef = useRef(null);

  // --- SMART AUTOCOMPLETE ---
  useEffect(() => {
    if (query.length < 2) {
      setSuggestions([]);
      setShowSuggestions(false);
      return;
    }

    setIsAutoCompleting(true);

    const delayDebounceFn = setTimeout(async () => {
      try {
        const response = await axios.get(`/api/stocks/autocomplete?query=${query}`);
        if (Array.isArray(response.data)) {
            setSuggestions(response.data);
            setShowSuggestions(true);
        } else {
            setSuggestions([]);
        }
      } catch (error) {
        console.error("Autocomplete error:", error);
      } finally {
        setIsAutoCompleting(false);
      }
    }, 300); // 300ms delay for snappiness

    return () => clearTimeout(delayDebounceFn);
  }, [query]);

  // --- SEARCH HANDLER ---
  const performSearch = async (searchQuery = query) => {
    const target = searchQuery.trim();
    if (!target) return;

    setIsSearching(true);
    setError('');
    setShowSuggestions(false);
    
    try {
      const response = await axios.get(`/api/stocks/search?query=${target}`);
      navigate(`/stock/${response.data.symbol}`);
    } catch (err) {
      setError('Could not locate stock. Please try a valid ticker.');
    } finally {
      setIsSearching(false);
    }
  };

  const handleSuggestionClick = (symbol) => {
    setQuery(symbol);
    setSuggestions([]);
    setShowSuggestions(false);
    navigate(`/stock/${symbol}`);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      performSearch();
    }
  };

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
      
      {/* Background FX */}
      <BackgroundLayer>
        <BlobOne />
        <BlobTwo />
      </BackgroundLayer>
      
      {/* Ticker Tape */}
      <IndicesBanner />
      
      <MainContent>
        <Title>Stellar Stock Screener</Title>
        <Subtitle>
            Leveraging Advanced Data Models to provide comprehensive<br /> 
            technical and fundamental financial insights.
        </Subtitle>
        
        {/* Search Bar */}
        <SearchSection ref={searchRef}>
          <SearchWrapper>
            <SearchInput
              type="text"
              placeholder="Search (e.g. Reliance, Bitcoin, Gold, Apple)..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              onFocus={() => query.length >= 2 && setShowSuggestions(true)}
              disabled={isSearching}
              spellCheck={false}
            />
            
            <SearchButton onClick={() => performSearch()} disabled={isSearching || isAutoCompleting} aria-label="Search">
              {isSearching || isAutoCompleting ? (
                  <FaSpinner className="fa-spin" size={20} />
              ) : (
                  <FaSearch size={20} />
              )}
            </SearchButton>
          </SearchWrapper>

          {showSuggestions && suggestions.length > 0 && (
            <SuggestionsList>
              {suggestions.map((item) => (
                <SuggestionItem key={item.symbol} onClick={() => handleSuggestionClick(item.symbol)}>
                  <ItemLeft>
                    <SuggestionSymbol>
                        {item.symbol}
                    </SuggestionSymbol>
                    <SuggestionName>{item.name}</SuggestionName>
                  </ItemLeft>
                  <SuggestionBadge>
                     {item.exchangeShortName || (item.symbol.includes('.') ? 'INTL' : 'US')}
                  </SuggestionBadge>
                </SuggestionItem>
              ))}
            </SuggestionsList>
          )}
        </SearchSection>

        <LoadingText>{isSearching ? 'Processing Market Data...' : error || ''}</LoadingText>
        
        <SectionLabel>— AI ANALYST SUITE —</SectionLabel>
        
        {/* TRIPLE AI UPLOADER GRID */}
        <UploadGrid>
            {/* 1. STOCK (Blue) */}
            <ChartUploader 
                type="stock"
                title="Stocks"
                description="Analyze Equity Charts & Trends."
                color="#58A6FF" 
                icon={<FaChartBar />}
            />
            
            {/* 2. INDEX (Gold) */}
            <ChartUploader 
                type="index"
                title="Indices"
                description="Macro Market Vision (Nifty, SPX)."
                color="#EBCB8B"
                icon={<FaGlobeAmericas />}
            />

            {/* 3. CRYPTO & COMMODITIES (Purple - New High End) */}
            <ChartUploader 
                type="crypto"
                title="Crypto / Commodities"
                description="Bitcoin, Gold, Oil & Global Assets."
                color="#D500F9"
                icon={<FaBitcoin />}
            />
        </UploadGrid>

      </MainContent>
    </HomePageContainer>
  );
};

export default HomePage;