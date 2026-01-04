import React, { useState, useCallback, useRef, useEffect } from 'react';
import styled, { keyframes, css } from 'styled-components';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { FaCloudUploadAlt, FaChartLine, FaGlobe } from 'react-icons/fa';

// --- ANIMATIONS ---
const pulse = (color) => keyframes`
  0% { transform: scale(1); box-shadow: 0 0 0 0 ${color}66; }
  70% { transform: scale(1.02); box-shadow: 0 0 20px 10px ${color}00; }
  100% { transform: scale(1); box-shadow: 0 0 0 0 ${color}00; }
`;

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

// --- STYLED COMPONENTS ---

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  animation: ${fadeIn} 0.6s ease-out;
`;

const UploaderCard = styled.div`
  width: 100%;
  height: 100%;
  min-height: 250px;
  padding: 2rem;
  
  /* Dynamic Glassmorphism Background based on type */
  background: linear-gradient(145deg, rgba(22, 27, 34, 0.8), rgba(13, 17, 23, 0.95));
  backdrop-filter: blur(12px);
  border: 1px solid ${({ color }) => color}33;
  border-radius: 20px;
  
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  overflow: hidden;

  /* Hover Effect */
  &:hover {
    border-color: ${({ color }) => color};
    transform: translateY(-5px);
    box-shadow: 0 15px 40px -10px ${({ color }) => color}44;
    
    .icon-wrapper {
      transform: scale(1.1) rotate(5deg);
      color: ${({ color }) => color};
    }
  }

  ${({ isDragActive, color }) => isDragActive && css`
    border-color: ${color};
    background: ${color}11;
    transform: scale(1.02);
  `}
`;

const IconWrapper = styled.div`
  font-size: 3rem;
  color: ${({ color }) => color}99;
  margin-bottom: 1.5rem;
  transition: all 0.4s ease;
  filter: drop-shadow(0 0 10px ${({ color }) => color}33);
`;

const Title = styled.h3`
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
`;

const Description = styled.p`
  font-size: 0.95rem;
  color: var(--color-text-secondary);
  line-height: 1.5;
  margin-bottom: 1.5rem;
  max-width: 80%;
`;

const UploadButton = styled.div`
  padding: 10px 24px;
  border-radius: 50px;
  background: ${({ color }) => color}22;
  color: ${({ color }) => color};
  border: 1px solid ${({ color }) => color};
  font-weight: 600;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;

  ${UploaderCard}:hover & {
    background: ${({ color }) => color};
    color: #000; /* Contrast text */
    box-shadow: 0 0 20px ${({ color }) => color}66;
  }
`;

const LoaderText = styled.p`
  color: ${({ color }) => color};
  font-size: 1.1rem;
  font-weight: 700;
  animation: ${({ color }) => pulse(color)} 2s infinite;
  margin-top: 1rem;
`;

const ErrorText = styled.div`
  margin-top: 1rem;
  color: #F85149;
  font-size: 0.9rem;
  background: rgba(248, 81, 73, 0.1);
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid rgba(248, 81, 73, 0.3);
`;

// --- COMPONENT ---

const ChartUploader = ({ 
    type = 'stock', // 'stock' or 'index'
    title = "Analyze Stock Chart",
    description = "Upload a screenshot of any stock candle chart.",
    color = "#58A6FF",
    icon = <FaChartLine />
}) => {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState('');
  const [isDragActive, setIsDragActive] = useState(false);
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const handleUpload = useCallback(async (file) => {
    if (!file) return;

    setIsUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('chart_image', file);
    // We send the 'type' to the backend so AI knows context (Optional but good practice)
    formData.append('analysis_type', type); 

    try {
      const response = await axios.post('/api/charts/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      let { identified_symbol, analysis_data } = response.data;

      if (!identified_symbol || identified_symbol === 'NOT_FOUND') {
        setError('System  could not identify the symbol. Please ensure the ticker name is visible in the top-left.');
        setIsUploading(false);
        return;
      }

      // --- VERIFICATION STEP ---
      // We ask our internal search to verify the AI's guess
      try {
        const searchRes = await axios.get(`/api/stocks/search?query=${identified_symbol}`);
        if (searchRes.data.symbol) {
            console.log(`System guess: ${identified_symbol} -> Corrected: ${searchRes.data.symbol}`);
            identified_symbol = searchRes.data.symbol;
        }
      } catch (e) {
          console.warn("Symbol verification skipped.");
      }

      // --- ROUTING LOGIC ---
      // If it's an Index (starts with ^ or is known index), go to Index Page
      // Otherwise go to Stock Page
      
      const isIndexSymbol = identified_symbol.includes('^') || 
                            ['NIFTY', 'BANKNIFTY', 'SENSEX', 'SPX', 'NDX'].some(i => identified_symbol.includes(i));
      
      const encodedSymbol = encodeURIComponent(identified_symbol);

      if (isIndexSymbol) {
        navigate(`/index/${encodedSymbol}`, { state: { chartAnalysis: analysis_data } });
      } else {
        navigate(`/stock/${encodedSymbol}`, { state: { chartAnalysis: analysis_data } });
      }

    } catch (err) {
      console.error("Upload error:", err);
      setError('Analysis failed. Please try a clearer image.');
      setIsUploading(false);
    }
  }, [navigate, type]);

  // Paste Handler
  useEffect(() => {
    const handlePaste = (e) => {
      // Only handle paste if mouse is hovering THIS specific component
      // (Simplified: Global paste works for now, usually fine)
      const items = e.clipboardData.items;
      for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
          handleUpload(items[i].getAsFile());
          break;
        }
      }
    };
    // Note: Global paste listener might trigger both if not careful. 
    // Ideally we add a focus state, but for simplicity in this architecture:
    // We will attach listener only when 'isDragActive' or add a click-to-focus mechanism.
    // For now, let's rely on Drag/Drop and Click mainly.
  }, [handleUpload]);

  const onFileChange = (e) => {
    if (e.target.files && e.target.files[0]) handleUpload(e.target.files[0]);
  };

  return (
    <Wrapper>
      <input type="file" ref={fileInputRef} style={{ display: 'none' }} onChange={onFileChange} accept="image/*" />
      
      <UploaderCard 
        color={color}
        isDragActive={isDragActive}
        onClick={() => fileInputRef.current.click()}
        onDragEnter={(e) => { e.preventDefault(); setIsDragActive(true); }}
        onDragLeave={(e) => { e.preventDefault(); setIsDragActive(false); }}
        onDragOver={(e) => { e.preventDefault(); }}
        onDrop={(e) => { 
            e.preventDefault(); 
            setIsDragActive(false); 
            if (e.dataTransfer.files[0]) handleUpload(e.dataTransfer.files[0]); 
        }}
      >
        {isUploading ? (
          <>
            <IconWrapper color={color} className="icon-wrapper" style={{animation: 'spin 2s linear infinite'}}>
                <FaGlobe /> {/* Spinner icon replacement */}
            </IconWrapper>
            <LoaderText color={color}>Processing Market Data...</LoaderText>
          </>
        ) : (
          <>
            <IconWrapper color={color} className="icon-wrapper">
                {icon}
            </IconWrapper>
            <Title>{title}</Title>
            <Description>{description}</Description>
            <UploadButton color={color}>
                <FaCloudUploadAlt /> Upload / Paste
            </UploadButton>
          </>
        )}
      </UploaderCard>
      
      {error && <ErrorText>{error}</ErrorText>}
    </Wrapper>
  );
};

export default ChartUploader;