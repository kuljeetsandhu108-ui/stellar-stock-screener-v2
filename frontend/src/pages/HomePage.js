import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';
import { 
  FaSearch, FaChartBar, FaGlobeAmericas, FaSpinner, 
  FaBitcoin, FaBrain, FaMicrochip, FaFileUpload, FaArrowUp,
  FaChevronLeft, FaChevronRight 
} from 'react-icons/fa';
import IndicesBanner from '../components/Indices/IndicesBanner';
import ChartUploader from '../components/HomePage/ChartUploader';

const API_URL = process.env.REACT_APP_API_URL || '';

// --- ANIMATIONS ---
const fadeIn = keyframes`from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); }`;
const float = keyframes`0% { transform: translate(0px, 0px) scale(1); } 33% { transform: translate(30px, -50px) scale(1.1); } 66% { transform: translate(-20px, 20px) scale(0.9); } 100% { transform: translate(0px, 0px) scale(1); }`;
const floatReverse = keyframes`0% { transform: translate(0px, 0px) scale(1); } 33% { transform: translate(-30px, 50px) scale(0.9); } 66% { transform: translate(20px, -20px) scale(1.1); } 100% { transform: translate(0px, 0px) scale(1); }`;
const scanBeam = keyframes`0% { left: -100%; opacity: 0; } 50% { opacity: 1; } 100% { left: 100%; opacity: 0; }`;

// --- STYLED COMPONENTS ---
const HomePageContainer = styled.div`display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding: 1rem; width: 100%; position: relative; overflow-x: hidden; background-color: var(--color-background); @media (min-width: 768px) { padding: 2rem; }`;
const BackgroundLayer = styled.div`position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none; overflow: hidden;`;
const GlowingBlob = styled.div`position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.25; animation: ${float} 15s ease-in-out infinite;`;
const BlobOne = styled(GlowingBlob)`top: -10%; left: -10%; width: 60vw; height: 60vw; background: var(--color-primary);`;
const BlobTwo = styled(GlowingBlob)`bottom: -10%; right: -10%; width: 70vw; height: 70vw; background: #7c3aed; animation: ${floatReverse} 18s ease-in-out infinite;`;

const MainContent = styled.div`display: flex; flex-direction: column; align-items: center; text-align: center; width: 100%; margin-top: 5vh; z-index: 1; position: relative;`;
const Title = styled.h1`font-size: 2.8rem; font-weight: 900; background: linear-gradient(to right, #fff, #a5b4fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem; animation: ${fadeIn} 1s ease-out; letter-spacing: -1.5px; @media (min-width: 768px) { font-size: 4.5rem; }`;
const Subtitle = styled.p`font-size: 1rem; color: var(--color-text-secondary); margin-bottom: 3.5rem; max-width: 650px; animation: ${fadeIn} 1.5s ease-out; line-height: 1.8;`;

// SEARCH STYLES
const SearchSection = styled.div`width: 100%; max-width: 700px; position: relative; animation: ${fadeIn} 1.8s ease-out; z-index: 999;`;
const SearchWrapper = styled.div`position: relative; width: 100%; display: flex; align-items: center; transition: transform 0.3s ease; &:hover { transform: scale(1.01); }`;
const SearchInput = styled.input`width: 100%; padding: 20px 30px; padding-right: 80px; font-size: 1.1rem; color: #fff; background: rgba(22, 27, 34, 0.6); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 60px; outline: none; box-shadow: 0 15px 40px rgba(0,0,0,0.4); &:focus { border-color: var(--color-primary); }`;
const SearchButton = styled.button`position: absolute; right: 8px; top: 50%; transform: translateY(-50%); background: linear-gradient(135deg, var(--color-primary), #3b82f6); color: white; border: none; border-radius: 50%; width: 54px; height: 54px; cursor: pointer; display: flex; align-items: center; justify-content: center;`;

const SuggestionsList = styled.ul`position: absolute; top: calc(100% + 12px); left: 15px; right: 15px; background: #0D1117; border: 1px solid var(--color-border); border-radius: 16px; box-shadow: 0 20px 50px rgba(0,0,0,0.9); z-index: 9999; list-style: none; padding: 8px; max-height: 350px; overflow-y: auto; text-align: left; margin: 0;`;
const SuggestionItem = styled.li`padding: 12px 16px; border-radius: 10px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; transition: all 0.2s ease; &:hover { background-color: rgba(88, 166, 255, 0.15); transform: translateX(4px); }`;
const StatusItem = styled.li`padding: 16px; color: #8B949E; text-align: center; font-size: 0.95rem; font-weight: 500; display: flex; align-items: center; justify-content: center; gap: 10px;`;

const SectionLabel = styled.div`display: flex; align-items: center; gap: 15px; color: var(--color-text-secondary); margin: 4rem 0 2rem 0; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 2px; width: 100%; max-width: 1200px; &::before, &::after { content: ''; height: 1px; flex-grow: 1; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent); }`;

// SCREENER STYLES
const ScreenerContainer = styled.div`width: 100%; max-width: 1200px; margin-top: 4rem; animation: ${fadeIn} 2s ease-out;`;
const ScreenerTabs = styled.div`display: flex; gap: 1rem; margin-bottom: 1.5rem; overflow-x: auto; padding-bottom: 0.5rem; &::-webkit-scrollbar { display: none; }`;
const ScreenerTab = styled.button`
  background: ${({ $active }) => $active ? 'linear-gradient(135deg, rgba(88,166,255,0.2), rgba(35,134,54,0.2))' : 'rgba(255,255,255,0.02)'};
  border: 1px solid ${({ $active }) => $active ? 'var(--color-primary)' : 'var(--color-border)'};
  color: ${({ $active }) => $active ? '#fff' : 'var(--color-text-secondary)'};
  padding: 10px 20px; border-radius: 30px; font-weight: 700; cursor: pointer; transition: all 0.3s ease; white-space: nowrap;
  &:hover { border-color: var(--color-primary); color: #fff; }
`;

const CarouselWrapper = styled.div`
  position: relative;
  width: 100%;
`;

const ScrollArrow = styled.button`
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(22, 27, 34, 0.95);
  border: 1px solid var(--color-border);
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  box-shadow: 0 4px 20px rgba(0,0,0,0.8);
  transition: all 0.2s ease;
  backdrop-filter: blur(4px);
  
  &:hover {
    background: var(--color-primary);
    color: #fff;
    border-color: var(--color-primary);
    transform: translateY(-50%) scale(1.1);
  }

  &.left { left: -15px; }
  &.right { right: -15px; }
  
  @media (max-width: 768px) {
      width: 34px; height: 34px;
      &.left { left: 5px; }
      &.right { right: 5px; }
  }
`;

const StockCarousel = styled.div`display: flex; gap: 1.5rem; overflow-x: auto; scroll-behavior: smooth; padding: 1rem 0.5rem; width: 100%; &::-webkit-scrollbar { height: 6px; } &::-webkit-scrollbar-thumb { background: #30363D; border-radius: 3px; }`;
const ScreenerCard = styled.div`
  min-width: 240px; background: linear-gradient(145deg, rgba(22, 27, 34, 0.8), rgba(13, 17, 23, 0.95));
  border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 1.5rem; text-align: left;
  cursor: pointer; transition: all 0.3s; position: relative; overflow: hidden;
  &:hover { transform: translateY(-5px); border-color: var(--color-primary); box-shadow: 0 10px 25px rgba(88, 166, 255, 0.15); }
`;
const CardSymbol = styled.h3`font-size: 1.4rem; color: #fff; margin: 0 0 5px 0; font-family: 'Roboto Mono', monospace;`;
const CardPrice = styled.div`font-size: 1.2rem; font-weight: 700; color: #C9D1D9; margin-bottom: 10px;`;
const CardChange = styled.span`
  background: ${({ $isPositive }) => $isPositive ? 'rgba(63, 185, 80, 0.15)' : 'rgba(248, 81, 73, 0.15)'}; 
  color: ${({ $isPositive }) => $isPositive ? '#3FB950' : '#F85149'}; 
  padding: 4px 8px; border-radius: 6px; font-size: 0.8rem; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;
`;
const CardVol = styled.div`font-size: 0.75rem; color: #8B949E; margin-top: 15px; font-weight: 600; text-transform: uppercase;`;

const UploadGrid = styled.div`display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; width: 100%; max-width: 1200px; padding: 0 1rem; @media (max-width: 1024px) { grid-template-columns: 1fr; }`;

// VISION LABS STYLES
const VisionContainer = styled.div`width: 100%; max-width: 1200px; margin-bottom: 4rem; padding: 0 1rem; animation: ${fadeIn} 2.2s ease-out;`;
const VisionCard = styled.div`background: linear-gradient(165deg, rgba(22, 27, 34, 0.8), rgba(13, 17, 23, 0.95)); border: 1px solid rgba(88, 166, 255, 0.3); border-radius: 24px; padding: 4rem 2rem; text-align: center; position: relative; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.4); transition: all 0.4s ease; &:hover { border-color: #58A6FF; box-shadow: 0 20px 60px rgba(88, 166, 255, 0.15); }`;
const VisionGlow = styled.div`position: absolute; top: -50%; left: 50%; transform: translateX(-50%); width: 80%; height: 100%; background: radial-gradient(circle, rgba(88, 166, 255, 0.15) 0%, transparent 70%); pointer-events: none; z-index: 0;`;
const ScanBeam = styled.div`position: absolute; top: 0; left: -100%; width: 50%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent); transform: skewX(-20deg); animation: ${scanBeam} 4s infinite linear; pointer-events: none;`;
const VisionTitle = styled.h2`font-size: 2.2rem; margin-bottom: 1rem; color: #fff; position: relative; z-index: 1; display: flex; align-items: center; justify-content: center; gap: 15px; svg { color: #58A6FF; }`;
const VisionDesc = styled.p`color: #8B949E; font-size: 1.1rem; max-width: 700px; margin: 0 auto 3rem auto; line-height: 1.7; position: relative; z-index: 1;`;
const DeepScanButton = styled.label`background: #58A6FF; color: #0D1117; padding: 16px 40px; border-radius: 50px; font-weight: 800; font-size: 1.1rem; cursor: pointer; display: inline-flex; align-items: center; gap: 12px; transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1); position: relative; z-index: 2; box-shadow: 0 0 25px rgba(88, 166, 255, 0.4); &:hover { transform: translateY(-3px) scale(1.05); background: #fff; box-shadow: 0 0 40px rgba(255, 255, 255, 0.6); }`;

const HomePage = () => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const[isAutocompleteLoading, setIsAutocompleteLoading] = useState(false);
  
  const navigate = useNavigate();
  const searchRef = useRef(null);

  // SINGLE SCREENER STATE
  const [screenerConfigs, setScreenerConfigs] = useState([]);
  const [activeScreener, setActiveScreener] = useState("");
  const[screenerData, setScreenerData] = useState([]);
  const [loadingScreener, setLoadingScreener] = useState(true);
  const [isVisionLoading, setIsVisionLoading] = useState(false);
  
  // Carousel Ref for Buttons
  const carouselRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
        if (searchRef.current && !searchRef.current.contains(event.target)) {
            setShowSuggestions(false);
        }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [searchRef]);

  // Robust Autocomplete Hook
  useEffect(() => {
    if (query.length < 2) { 
        setSuggestions([]); 
        setShowSuggestions(false); 
        setIsAutocompleteLoading(false);
        return; 
    }
    
    setIsAutocompleteLoading(true);
    setShowSuggestions(true);

    const timer = setTimeout(async () => {
      try {
        const res = await axios.get('/api/stocks/autocomplete?query=' + query);
        if (res.data) {
            setSuggestions(res.data);
        } else {
            setSuggestions([]);
        }
      } catch (e) {
          setSuggestions([]);
      } finally {
          setIsAutocompleteLoading(false);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

  // Screener Hooks
  useEffect(() => {
    let isMounted = true;
    axios.get('/api/stocks/screener/configs').then(res => {
        if(isMounted && res.data.length > 0) {
            setScreenerConfigs(res.data);
            setActiveScreener(res.data[0].key);
        }
    }).catch(console.error);
    return () => { isMounted = false; };
  },[]);

  useEffect(() => {
    if(!activeScreener) return;
    let isMounted = true;
    setLoadingScreener(true);
    axios.get(`/api/stocks/screener/${activeScreener}`)
        .then(res => { if(isMounted) setScreenerData(res.data ||[]); })
        .catch(() => { if(isMounted) setScreenerData([]); })
        .finally(() => { if(isMounted) setLoadingScreener(false); });
    return () => { isMounted = false; };
  }, [activeScreener]);

  const performSearch = async (searchQuery = query) => {
    const target = searchQuery.trim();
    if (!target) return;
    setIsSearching(true); setShowSuggestions(false);
    try {
      const res = await axios.get('/api/stocks/search?query=' + target);
      navigate('/stock/' + res.data.symbol);
    } catch (err) { setIsSearching(false); }
  };

  const handleVisionUpload = async (e) => {
      const file = e.target.files[0];
      if (!file) return;
      setIsVisionLoading(true);
      const formData = new FormData(); formData.append('chart_image', file);
      try {
          const res = await axios.post('/api/charts/analyze-pure', formData);
          navigate('/vision-result', { state: { analysis: res.data.analysis, image: URL.createObjectURL(file) } });
      } catch (err) { setIsVisionLoading(false); }
  };

  // Scroll function triggered by arrows
  const scrollScreener = (dir) => {
      if (carouselRef.current) {
          const amount = window.innerWidth > 768 ? 600 : 250;
          carouselRef.current.scrollBy({ left: dir === 'left' ? -amount : amount, behavior: 'smooth' });
      }
  };

  return (
    <HomePageContainer>
      <BackgroundLayer><BlobOne /><BlobTwo /></BackgroundLayer>
      <IndicesBanner />
      
      <MainContent>
        <Title>Stellar Stock Screener</Title>
        <Subtitle>The Ultimate Financial Intelligence Platform. Leveraging Quantitative Models for Real-Time Trade Discovery.</Subtitle>
        
        {/* ROBUST SEARCH COMPONENT */}
        <SearchSection ref={searchRef}>
          <SearchWrapper>
            <SearchInput 
                type="text" 
                placeholder="Search (e.g. Reliance, Bitcoin, Gold)..." 
                value={query} 
                onChange={(e) => setQuery(e.target.value)} 
                onKeyPress={(e) => e.key === 'Enter' && performSearch()} 
                onFocus={() => query.length >= 2 && setShowSuggestions(true)} 
                disabled={isSearching} 
            />
            <SearchButton onClick={() => performSearch()} disabled={isSearching}>
              {isSearching ? <FaSpinner className="fa-spin" size={20} /> : <FaSearch size={20} />}
            </SearchButton>
          </SearchWrapper>
          
          {showSuggestions && query.length >= 2 && (
            <SuggestionsList>
              {isAutocompleteLoading ? (
                 <StatusItem>
                     <FaSpinner className="fa-spin" /> Scanning Markets...
                 </StatusItem>
              ) : suggestions.length > 0 ? (
                suggestions.map((item) => (
                  <SuggestionItem key={item.symbol} onClick={() => { setQuery(item.symbol); performSearch(item.symbol); setShowSuggestions(false); }}>
                    <div style={{display:'flex', flexDirection:'column'}}>
                        <span style={{fontWeight: 700, color: 'var(--color-primary)'}}>{item.symbol}</span>
                        <span style={{fontSize: '0.8rem', color: '#8b949e'}}>{item.name}</span>
                    </div>
                    <span style={{fontSize: '0.7rem', background: 'rgba(255,255,255,0.05)', padding: '4px 8px', borderRadius: '12px', color: '#8b949e'}}>
                        {item.exchangeShortName || 'INTL'}
                    </span>
                  </SuggestionItem>
                ))
              ) : (
                 <StatusItem>
                     No stocks found matching "{query}"
                 </StatusItem>
              )}
            </SuggestionsList>
          )}
        </SearchSection>

        <ScreenerContainer>
            <SectionLabel>Institutional Radar (Live)</SectionLabel>
            
            <ScreenerTabs>
                {screenerConfigs.map(config => (
                    <ScreenerTab 
                        key={config.key} 
                        $active={activeScreener === config.key}
                        onClick={() => setActiveScreener(config.key)}
                    >
                        {config.name}
                    </ScreenerTab>
                ))}
            </ScreenerTabs>

            {screenerConfigs.map(config => config.key === activeScreener && (
                <p key={`desc-${config.key}`} style={{color: 'var(--color-text-secondary)', fontSize: '0.9rem', marginBottom: '2rem'}}>
                    {config.description}
                </p>
            ))}

            {loadingScreener ? (
                <div style={{color: 'var(--color-primary)', marginTop: '2rem'}}><FaSpinner className="fa-spin" size={24} /></div>
            ) : screenerData && screenerData.length > 0 ? (
                <CarouselWrapper>
                    <ScrollArrow className="left" onClick={() => scrollScreener('left')}><FaChevronLeft size={14} /></ScrollArrow>
                    <StockCarousel ref={carouselRef}>
                        {screenerData.map((stock, i) => (
                            <ScreenerCard key={i} onClick={() => navigate('/stock/' + encodeURIComponent(stock.nsecode + '.NS'))}>
                                <CardSymbol>{stock.nsecode}</CardSymbol>
                                <CardPrice>{'\u20B9'}{stock.close}</CardPrice>
                                <CardChange $isPositive={stock.per_chg >= 0}>
                                    {stock.per_chg >= 0 ? <FaArrowUp size={10}/> : null} {stock.per_chg}%
                                </CardChange>
                                <CardVol>Vol: {(stock.volume / 1000000).toFixed(2)}M</CardVol>
                            </ScreenerCard>
                        ))}
                    </StockCarousel>
                    <ScrollArrow className="right" onClick={() => scrollScreener('right')}><FaChevronRight size={14} /></ScrollArrow>
                </CarouselWrapper>
            ) : (
                <div style={{color: '#8B949E', padding: '2rem', border: '1px dashed #30363D', borderRadius: '12px'}}>
                    No stocks currently matching parameters for this strategy.
                </div>
            )}
        </ScreenerContainer>

        <SectionLabel>AI Analyst Suite</SectionLabel>
        <UploadGrid>
            <ChartUploader type="stock" title="Stocks" description="Equities & ETFs (NSE, BSE, NASDAQ)." color="#58A6FF" icon={<FaChartBar />} />
            <ChartUploader type="index" title="Indices" description="Macro Analysis (Nifty 50, SPX)." color="#EBCB8B" icon={<FaGlobeAmericas />} />
            <ChartUploader type="crypto" title="Crypto / Commodities" description="Bitcoin, Gold, Oil & Global Assets." color="#D500F9" icon={<FaBitcoin />} />
        </UploadGrid>

        <SectionLabel>Pure Vision Labs</SectionLabel>
        <VisionContainer>
            <VisionCard>
                <VisionGlow /><ScanBeam />
                <VisionTitle><FaBrain /> Quantum Vision Engine<FaMicrochip style={{fontSize:'1.5rem', opacity:0.5}}/></VisionTitle>
                <VisionDesc>Upload any financial chart image. Our proprietary Vision Model will perform a <strong>Geometric & Mathematical Breakdown</strong> of price action, identifying hidden liquidity zones and institutional footprints <strong>without needing any external data feed</strong>.</VisionDesc>
                <DeepScanButton htmlFor="vision-upload">
                    {isVisionLoading ? (<><FaSpinner className="fa-spin"/> PROCESSING PIXELS...</>) : (<><FaFileUpload /> PERFORM DEEP SCAN</>)}
                </DeepScanButton>
                <input id="vision-upload" type="file" style={{display: 'none'}} accept="image/*" onChange={handleVisionUpload} disabled={isVisionLoading}/>
            </VisionCard>
        </VisionContainer>

      </MainContent>
    </HomePageContainer>
  );
};
export default HomePage;
