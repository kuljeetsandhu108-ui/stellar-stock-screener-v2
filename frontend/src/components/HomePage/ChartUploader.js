import React, { useState, useCallback, useRef, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

// --- Styled Components & Animations ---

const pulse = keyframes`
  0% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(88, 166, 255, 0.4);
  }
  70% {
    transform: scale(1.02);
    box-shadow: 0 0 10px 20px rgba(88, 166, 255, 0);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(88, 166, 255, 0);
  }
`;

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

// --- HIGH END "GLASSMORPHISM" UI ---
const UploaderContainer = styled.div`
  width: 100%;
  max-width: 750px;
  margin-top: 3rem;
  padding: 3rem 2rem;
  
  /* Glassmorphism Background */
  background: linear-gradient(145deg, rgba(22, 27, 34, 0.6), rgba(13, 17, 23, 0.8));
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  
  /* Border and Shadow */
  border: 2px dashed ${({ isDragActive }) => (isDragActive ? 'var(--color-primary)' : 'rgba(88, 166, 255, 0.2)')};
  border-radius: 20px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
  
  text-align: center;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  animation: ${fadeIn} 0.8s ease-out;

  &:hover {
    border-color: var(--color-primary);
    transform: translateY(-5px);
    box-shadow: 0 12px 40px 0 rgba(88, 166, 255, 0.15);
    background: linear-gradient(145deg, rgba(22, 27, 34, 0.8), rgba(13, 17, 23, 0.9));
  }
`;

const UploadText = styled.p`
  color: var(--color-text-secondary);
  font-size: 1.1rem;
  margin: 0;
  pointer-events: none; /* Ensures the click passes through to container */
`;

const HighlightText = styled.span`
  color: var(--color-primary);
  font-weight: 700;
  text-decoration: underline;
  text-underline-offset: 4px;
`;

const LoaderText = styled.p`
  color: var(--color-primary);
  font-size: 1.3rem;
  font-weight: 700;
  animation: ${pulse} 2s infinite;
  margin: 0;
`;

const ErrorText = styled.p`
  color: var(--color-danger);
  font-size: 1rem;
  font-weight: 500;
  margin-top: 1rem;
  background: rgba(248, 81, 73, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  display: inline-block;
  border: 1px solid rgba(248, 81, 73, 0.3);
`;

// --- The Final, Feature-Rich Component ---

const ChartUploader = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState('');
  const [isDragActive, setIsDragActive] = useState(false);
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  // --- CORE UPLOAD LOGIC ---
  const handleUpload = useCallback(async (file) => {
    if (!file) return;

    setIsUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('chart_image', file);

    try {
      const response = await axios.post('/api/charts/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      const { identified_symbol, analysis_data } = response.data;

      if (!identified_symbol || identified_symbol === 'NOT_FOUND') {
        setError('AI could not identify a stock symbol. Please upload a clearer chart screenshot.');
        setIsUploading(false);
        return;
      }
      
      // Intelligent Navigation based on Symbol Type
      const isIndex = identified_symbol.includes('^');
      const encodedSymbol = encodeURIComponent(identified_symbol);

      if (isIndex) {
        navigate(`/index/${encodedSymbol}`, { state: { chartAnalysis: analysis_data } });
      } else {
        navigate(`/stock/${encodedSymbol}`, { state: { chartAnalysis: analysis_data } });
      }

    } catch (err) {
      console.error("Chart analysis failed:", err);
      setError('An error occurred during AI analysis. Please try again.');
      setIsUploading(false);
    }
  }, [navigate]);

  // --- CLIPBOARD PASTE LISTENER (Ctrl+V) ---
  useEffect(() => {
    const handlePaste = (e) => {
      const items = e.clipboardData.items;
      for (let i = 0; i < items.length; i++) {
        // Look for items that are images
        if (items[i].type.indexOf('image') !== -1) {
          const file = items[i].getAsFile();
          handleUpload(file);
          // We found an image, so we can stop looking
          break;
        }
      }
    };

    // Attach listener to the document
    document.addEventListener('paste', handlePaste);

    // Cleanup listener when component unmounts
    return () => document.removeEventListener('paste', handlePaste);
  }, [handleUpload]);

  // --- DRAG AND DROP HANDLERS ---
  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragActive(true);
    } else if (e.type === "dragleave") {
      setIsDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleUpload(e.dataTransfer.files[0]);
    }
  }, [handleUpload]);

  // --- CLICK HANDLERS ---
  const onFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleUpload(e.target.files[0]);
    }
  };

  const onContainerClick = () => {
    fileInputRef.current.click();
  };

  return (
    <div style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <input
        type="file"
        id="chart-upload-input"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={onFileChange}
        accept="image/png, image/jpeg, image/webp"
      />
      
      <UploaderContainer
        onClick={onContainerClick}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        isDragActive={isDragActive}
      >
        {isUploading ? (
          <LoaderText>Analyzing Chart Pattern & Sentiment...</LoaderText>
        ) : (
          <UploadText>
            Drag & Drop, <strong>Paste (Ctrl+V)</strong>, or <HighlightText>Click to Upload</HighlightText>
          </UploadText>
        )}
      </UploaderContainer>
      
      {error && <ErrorText>{error}</ErrorText>}
    </div>
  );
};

export default ChartUploader;