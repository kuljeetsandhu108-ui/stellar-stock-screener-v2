import React, { useState, useCallback, useRef } from 'react';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

// --- Styled Components & Animations ---

const pulse = keyframes`
  0% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(88, 166, 255, 0.7);
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

const UploaderContainer = styled.div`
  width: 100%;
  max-width: 650px;
  margin-top: 2rem;
  padding: 2rem;
  border: 2px dashed ${({ isDragActive }) => (isDragActive ? 'var(--color-primary)' : 'var(--color-border)')};
  border-radius: 12px;
  background-color: var(--color-secondary);
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    border-color: var(--color-primary);
  }
`;

const UploadText = styled.p`
  color: var(--color-text-secondary);
  font-size: 1.1rem;
`;

const HighlightText = styled.span`
  color: var(--color-primary);
  font-weight: 600;
`;

const LoaderText = styled.p`
  color: var(--color-primary);
  font-size: 1.2rem;
  font-weight: 600;
  animation: ${pulse} 2s infinite;
`;

const ErrorText = styled.p`
  color: var(--color-danger);
  font-size: 1.1rem;
  font-weight: 500;
`;

// --- The Final, Corrected React Component ---

const ChartUploader = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState('');
  const [isDragActive, setIsDragActive] = useState(false);
  const navigate = useNavigate();
  const fileInputRef = useRef(null); // Create a ref for the hidden file input

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
        setError('AI could not identify a stock symbol from the chart. Please try a clearer image.');
        setIsUploading(false);
        return;
      }
      
      // --- THIS IS THE CRITICAL NAVIGATION FIX ---
      // We check if the symbol is an index (contains '^') or a regular stock.
      const isIndex = identified_symbol.includes('^');
      
      // We MUST URL-encode the symbol to handle special characters like '^'.
      const encodedSymbol = encodeURIComponent(identified_symbol);

      // We navigate to the correct path based on the symbol type.
      if (isIndex) {
        navigate(`/index/${encodedSymbol}`, { state: { chartAnalysis: analysis_data } });
      } else {
        navigate(`/stock/${encodedSymbol}`, { state: { chartAnalysis: analysis_data } });
      }

    } catch (err) {
      console.error("Chart analysis failed:", err);
      setError('An error occurred during analysis. Please try again.');
      setIsUploading(false);
    }
  }, [navigate]);

  // --- Drag and Drop Handlers ---
  // We use useCallback for performance, preventing these functions from being recreated on every render.
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

  // --- Manual File Input Handlers ---
  const onFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleUpload(e.target.files[0]);
    }
  };

  const onContainerClick = () => {
    // This function programmatically "clicks" the hidden file input element.
    fileInputRef.current.click();
  };

  return (
    <div>
      <input
        type="file"
        id="chart-upload-input"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={onFileChange}
        accept="image/png, image/jpeg, image/webp"
      />
      
      {/* The main container now handles all events for a seamless experience */}
      <UploaderContainer
        onClick={onContainerClick}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        isDragActive={isDragActive}
      >
        {isUploading ? (
          <LoaderText>Analyzing with AI...</LoaderText>
        ) : (
          <UploadText>
            Drag & drop a chart screenshot here, or <HighlightText>click to upload</HighlightText>
          </UploadText>
        )}
      </UploaderContainer>
      
      {error && <ErrorText style={{ textAlign: 'center', marginTop: '1rem' }}>{error}</ErrorText>}
    </div>
  );
};

export default ChartUploader;