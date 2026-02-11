import React, { useEffect, useRef } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';
import { FaSpinner } from 'react-icons/fa';

const fadeIn = keyframes`from { opacity: 0; } to { opacity: 1; }`;

const Container = styled.div`
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: var(--color-background);
  color: var(--color-text-primary);
  animation: ${fadeIn} 0.5s ease-in;
`;

const Spinner = styled(FaSpinner)`
  font-size: 3rem;
  color: var(--color-primary);
  animation: spin 1s linear infinite;
  margin-bottom: 1.5rem;
  
  @keyframes spin { 100% { transform: rotate(360deg); } }
`;

const AuthCallback = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const processed = useRef(false);

  useEffect(() => {
    const code = searchParams.get('auth_code');
    
    if (code && !processed.current) {
        processed.current = true;
        
        // Exchange Code for Token
        axios.post('/api/auth/fyers/validate', { auth_code: code })
            .then(res => {
                const { access_token, client_id } = res.data;
                
                // Save to Local Storage (Persistent)
                localStorage.setItem('fyers_token', access_token);
                localStorage.setItem('fyers_client_id', client_id);
                
                // Redirect to Home
                setTimeout(() => navigate('/'), 1000);
            })
            .catch(err => {
                console.error("Auth Failed", err);
                alert("Login Failed. Please try again.");
                navigate('/');
            });
    } else if (!code) {
        navigate('/');
    }
  }, [searchParams, navigate]);

  return (
    <Container>
      <Spinner />
      <h2>Connecting to Fyers...</h2>
      <p style={{color: '#8B949E'}}>Securing your data feed.</p>
    </Container>
  );
};

export default AuthCallback;