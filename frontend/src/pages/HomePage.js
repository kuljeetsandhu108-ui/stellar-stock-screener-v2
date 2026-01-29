import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import styled, { keyframes, css } from 'styled-components';
import axios from 'axios';
import { 
  FaSearch, FaChartBar, FaGlobeAmericas, FaSpinner, 
  FaBitcoin, FaBrain, FaMicrochip, FaFileUpload 
} from 'react-icons/fa';

// --- COMPONENTS ---
import IndicesBanner from '../components/Indices/IndicesBanner';
import ChartUploader from '../components/HomePage/ChartUploader';

// ==========================================
// 1. CINEMATIC ANIMATIONS
// ==========================================

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

const scanBeam = keyframes`
  0% { left: -100%; opacity: 0; }
  50% { opacity: 1; }
  100% { left: 100%; opacity: 0; }
`;

const pulseGlow = keyframes`
  0% { box-shadow: 0 0 5px rgba(88, 166, 255, 0.4); }
  50% { box-shadow: 0 0 20px rgba(88, 166, 255, 0.8); }
  100% { box-shadow: 0 0 5px rgba(88, 166, 255, 0.4); }
`;

// ==========================================
// 2. HIGH-END STYLED COMPONENTS
// ==========================================

const HomePageContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
  width: 100%;
  position: relative;
  overflow-x: hidden;
  background-color: var(--color-background);
  
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
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
`;

const GlowingBlob = styled.div`
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.25;
  animation: ${float} 15s ease-in-out infinite;
`;

const BlobOne = styled(GlowingBlob)`
  top: -10%;
  left: -10%;
  width: 60vw;
  height: 60vw;
  background: var(--color-primary);
`;

const BlobTwo = styled(GlowingBlob)`
  bottom: -10%;
  right: -10%;
  width: 70vw;
  height: 70vw;
  background: #7c3aed; /* Deep Purple */
  animation: ${floatReverse} 18s ease-in-out infinite;
`;

const MainContent = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    width: 100%;
    margin-top: 5vh;
    z-index: 1;
    position: relative;
    
    @media (min-width: 768px) {
        margin-top: 8vh;
    }
`;

const Title = styled.h1`
  font-size: 2.8rem;
  font-weight: 900;
  background: linear-gradient(to right, #fff, #a5b4fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1rem;
  animation: ${fadeIn} 1s ease-out;
  letter-spacing: -1.5px;
  text-shadow: 0 10px 40px rgba(0,0,0,0.5);
  
  @media (min-width: 768px) {
    font-size: 4.5rem;
  }
`;

const Subtitle = styled.p`
  font-size: 1rem;
  color: var(--color-text-secondary);
  margin-bottom: 3.5rem;
  max-width: 650px;
  animation: ${fadeIn} 1.5s ease-out;
  padding: 0 1.5rem;
  line-height: 1.8;
  font-weight: 400;
  
  @media (min-width: 768px) {
    font-size: 1.25rem;
  }
`;

// --- SEARCH BAR (GLASS) ---

const SearchSection = styled.div`
  width: 100%;
  max-width: 700px;
  position: relative;
  animation: ${fadeIn} 1.8s ease-out;
  z-index: 50;
`;

const SearchWrapper = styled.div`
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.01);
  }
`;

const SearchInput = styled.input`
  width: 100%;
  padding: 20px 30px;
  padding-right: 80px;
  font-size: 1.1rem;
  color: #fff;
  background: rgba(22, 27, 34, 0.6); 
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 60px;
  outline: none;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);

  &::placeholder {
    color: rgba(255, 255, 255, 0.4);
  }

  &:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 30px rgba(88, 166, 255, 0.3);
    background: rgba(22, 27, 34, 0.9);
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
  width: 54px;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 5px 20px rgba(59, 130, 246, 0.5);

  &:hover {
    transform: translateY(-50%) scale(1.1);
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.7);
  }
  
  &:active {
    transform: translateY(-50%) scale(0.95);
  }

  &:disabled {
    filter: grayscale(1);
    cursor: default;
  }
`;

// --- AUTOCOMPLETE ---

const SuggestionsList = styled.ul`
  position: absolute;
  top: 110%;
  left: 15px;
  right: 15px;
  background: rgba(22, 27, 34, 0.95);
  backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  box-shadow: 0 25px 50px rgba(0,0,0,0.6);
  list-style: none;
  padding: 5px;
  max-height: 400px;
  overflow-y: auto;
  z-index: 100;
  
  &::-webkit-scrollbar { width: 6px; }
  &::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
`;

const SuggestionItem = styled.li`
  padding: 16px 20px;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.2s ease;
  margin-bottom: 2px;

  &:hover { 
    background-color: rgba(88, 166, 255, 0.15); 
  }
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
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 250px;
`;

const SuggestionBadge = styled.span`
  font-size: 0.7rem;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  padding: 4px 10px;
  border-radius: 20px;
  color: var(--color-text-secondary);
  font-weight: 600;
  text-transform: uppercase;
`;

const LoadingText = styled.p`
  color: var(--color-primary); 
  margin-top: 1.5rem; 
  height: 24px; 
  font-weight: 600;
  letter-spacing: 0.5px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 10px;
`;

// --- GRID & SECTIONS ---

const SectionLabel = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
  color: var(--color-text-secondary);
  margin: 4rem 0 2rem 0;
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  width: 100%;
  max-width: 1200px;
  
  &::before, &::after {
    content: '';
    height: 1px;
    flex-grow: 1;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
  }
`;

const UploadGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  width: 100%;
  max-width: 1200px;
  padding: 0 1rem;
  animation: ${fadeIn} 2s ease-out;

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    max-width: 500px;
  }
`;

// --- QUANTUM VISION SECTION (NEW) ---

const VisionContainer = styled.div`
  width: 100%;
  max-width: 1200px;
  margin-bottom: 4rem;
  padding: 0 1rem;
  animation: ${fadeIn} 2.2s ease-out;
`;

const VisionCard = styled.div`
  background: linear-gradient(165deg, rgba(22, 27, 34, 0.8), rgba(13, 17, 23, 0.95));
  border: 1px solid rgba(88, 166, 255, 0.3);
  border-radius: 24px;
  padding: 4rem 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0,0,0,0.4);
  transition: all 0.4s ease;

  &:hover {
    border-color: #58A6FF;
    box-shadow: 0 20px 60px rgba(88, 166, 255, 0.15);
  }
`;

const VisionGlow = styled.div`
  position: absolute;
  top: -50%;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 100%;
  background: radial-gradient(circle, rgba(88, 166, 255, 0.15) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
`;

const ScanBeam = styled.div`
  position: absolute;
  top: 0;
  left: -100%;
  width: 50%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
  transform: skewX(-20deg);
  animation: ${scanBeam} 4s infinite linear;
  pointer-events: none;
`;

const VisionTitle = styled.h2`
  font-size: 2.2rem;
  margin-bottom: 1rem;
  color: #fff;
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;

  svg { color: #58A6FF; }
`;

const VisionDesc = styled.p`
  color: #8B949E;
  font-size: 1.1rem;
  max-width: 700px;
  margin: 0 auto 3rem auto;
  line-height: 1.7;
  position: relative;
  z-index: 1;
`;

const DeepScanButton = styled.label`
  background: #58A6FF;
  color: #0D1117;
  padding: 16px 40px;
  border-radius: 50px;
  font-weight: 800;
  font-size: 1.1rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  z-index: 2;
  box-shadow: 0 0 25px rgba(88, 166, 255, 0.4);

  &:hover {
    transform: translateY(-3px) scale(1.05);
    background: #fff;
    box-shadow: 0 0 40px rgba(255, 255, 255, 0.6);
  }

  &:active {
    transform: translateY(0) scale(0.98);
  }
`;

// ==========================================
// 3. MAIN COMPONENT LOGIC
// ==========================================

const HomePage = () => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isAutoCompleting, setIsAutoCompleting] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [isVisionLoading, setIsVisionLoading] = useState(false);
  const [error, setError] = useState('');
  
  const navigate = useNavigate();
  const searchRef = useRef(null);

  // --- AUTOCOMPLETE ENGINE ---
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
        if (Array.isArray(response.data) && response.data.length > 0) {
            setSuggestions(response.data);
            setShowSuggestions(true);
        } else {
            setSuggestions([]);
            setShowSuggestions(false);
        }
      } catch (error) {
        console.warn("Autocomplete silent fail");
      } finally {
        setIsAutoCompleting(false);
      }
    }, 250); // Fast debounce

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
      // 1. Try exact match first
      const response = await axios.get(`/api/stocks/search?query=${target}`);
      navigate(`/stock/${response.data.symbol}`);
    } catch (err) {
      setError('Ticker not found. Please try again.');
    } finally {
      setIsSearching(false);
    }
  };

  // --- QUANTUM VISION HANDLER ---
  const handleVisionUpload = async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      setIsVisionLoading(true);
      setError("");

      const formData = new FormData();
      formData.append('chart_image', file);

      try {
          // Direct call to Pure Vision Endpoint
          const res = await axios.post('/api/charts/analyze-pure', formData);
          
          // Navigate to result page with payload
          navigate('/vision-result', { 
              state: { 
                  analysis: res.data.analysis, 
                  image: URL.createObjectURL(file) 
              } 
          });
      } catch (err) {
          console.error("Vision Error:", err);
          setError("Vision Scan Failed. Please try a clearer image.");
          setIsVisionLoading(false);
      }
  };

  // --- EVENT LISTENERS ---
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [searchRef]);

  // ==========================================
  // 4. RENDER
  // ==========================================

  return (
    <HomePageContainer>
      
      {/* Background FX */}
      <BackgroundLayer>
        <BlobOne />
        <BlobTwo />
      </BackgroundLayer>
      
      {/* Live Ticker Tape */}
      <IndicesBanner />
      
      <MainContent>
        <Title>Stellar Stock Screener</Title>
        <Subtitle>
            The Ultimate Financial Intelligence Platform.<br /> 
            Leveraging Neural Networks & Quantitative Models for Real-Time Analysis.
        </Subtitle>
        
        {/* Search Engine */}
        <SearchSection ref={searchRef}>
          <SearchWrapper>
            <SearchInput
              type="text"
              placeholder="Search (e.g. Reliance, Bitcoin, Gold, Apple)..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && performSearch()}
              onFocus={() => query.length >= 2 && setShowSuggestions(true)}
              disabled={isSearching}
              spellCheck={false}
            />
            
            <SearchButton onClick={() => performSearch()} disabled={isSearching || isAutoCompleting}>
              {isSearching ? <FaSpinner className="fa-spin" size={20} /> : <FaSearch size={20} />}
            </SearchButton>
          </SearchWrapper>

          {/* Autocomplete Dropdown */}
          {showSuggestions && (
            <SuggestionsList>
              {suggestions.map((item) => (
                <SuggestionItem key={item.symbol} onClick={() => { setQuery(item.symbol); performSearch(item.symbol); }}>
                  <div style={{display:'flex', flexDirection:'column'}}>
                    <SuggestionSymbol>{item.symbol}</SuggestionSymbol>
                    <SuggestionName>{item.name}</SuggestionName>
                  </div>
                  <SuggestionBadge>
                     {item.exchangeShortName || (item.symbol.includes('.') ? 'INTL' : 'US')}
                  </SuggestionBadge>
                </SuggestionItem>
              ))}
            </SuggestionsList>
          )}
        </SearchSection>

        {/* Status Text */}
        <LoadingText>
            {isSearching && <><FaSpinner className="fa-spin"/> Establishing Data Uplink...</>}
            {error && <span style={{color:'#F85149'}}>{error}</span>}
        </LoadingText>
        
        {/* --- AI ANALYST SUITE --- */}
        <SectionLabel>AI Analyst Suite</SectionLabel>
        
        <UploadGrid>
            <ChartUploader 
                type="stock"
                title="Stocks"
                description="Equities & ETFs (NSE, BSE, NASDAQ)."
                color="#58A6FF" 
                icon={<FaChartBar />}
            />
            <ChartUploader 
                type="index"
                title="Indices"
                description="Macro Analysis (Nifty 50, SPX)."
                color="#EBCB8B"
                icon={<FaGlobeAmericas />}
            />
            <ChartUploader 
                type="crypto"
                title="Crypto / Commodities"
                description="Bitcoin, Gold, Oil & Global Assets."
                color="#D500F9"
                icon={<FaBitcoin />}
            />
        </UploadGrid>

        {/* --- QUANTUM VISION ENGINE (NEW) --- */}
        <SectionLabel>Pure Vision Labs</SectionLabel>

        <VisionContainer>
            <VisionCard>
                <VisionGlow />
                <ScanBeam />
                
                <VisionTitle>
                    <FaBrain /> Quantum Vision Engine
                    <FaMicrochip style={{fontSize:'1.5rem', opacity:0.5}}/>
                </VisionTitle>
                
                <VisionDesc>
                    Upload any financial chart image. Our proprietary Vision Model will perform a 
                    <strong> Geometric & Mathematical Breakdown </strong> of price action, 
                    identifying hidden liquidity zones and institutional footprints 
                    <strong> without needing any external data feed</strong>.
                </VisionDesc>

                <DeepScanButton htmlFor="vision-upload">
                    {isVisionLoading ? (
                        <><FaSpinner className="fa-spin"/> PROCESSING PIXELS...</>
                    ) : (
                        <><FaFileUpload /> PERFORM DEEP SCAN</>
                    )}
                </DeepScanButton>
                
                <input 
                    id="vision-upload" 
                    type="file" 
                    style={{display: 'none'}} 
                    accept="image/*"
                    onChange={handleVisionUpload}
                    disabled={isVisionLoading}
                />
            </VisionCard>
        </VisionContainer>

      </MainContent>
    </HomePageContainer>
  );
};

export default HomePage;