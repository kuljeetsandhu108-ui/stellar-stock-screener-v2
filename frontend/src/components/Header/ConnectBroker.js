import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import { FaPlug, FaCheckCircle, FaSignOutAlt } from 'react-icons/fa';

const Button = styled.button`
  background: ${({ connected }) => (connected ? 'rgba(63, 185, 80, 0.15)' : 'linear-gradient(135deg, #58A6FF, #238636)')};
  border: 1px solid ${({ connected }) => (connected ? '#3FB950' : 'transparent')};
  color: ${({ connected }) => (connected ? '#3FB950' : '#ffffff')};
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  white-space: nowrap;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  }
`;

const ConnectBroker = () => {
  const [token, setToken] = useState(localStorage.getItem('fyers_token'));

  const handleLogin = async () => {
    try {
      // 1. Get the login URL from backend
      // We use window.location.origin to dynamically pick localhost or 127.0.0.1
      const backendUrl = window.location.origin.replace('3000', '8000'); 
      const res = await axios.get(`${backendUrl}/api/auth/fyers/login-url`);
      
      if (res.data.url) {
        window.location.href = res.data.url;
      }
    } catch (e) {
      console.error("Login Error", e);
      // Detailed error message for debugging
      alert(`Could not connect to broker. Server says: ${e.message}`);
    }
  };

  const handleLogout = () => {
      localStorage.removeItem('fyers_token');
      localStorage.removeItem('fyers_client_id');
      setToken(null);
      window.location.reload(); // Refresh to reset sockets
  };

  if (token) {
    return (
      <Button connected onClick={handleLogout} title="Click to Disconnect">
        <FaCheckCircle /> Fyers Connected
      </Button>
    );
  }

  return (
    <Button onClick={handleLogin}>
      <FaPlug /> Connect Broker
    </Button>
  );
};

export default ConnectBroker;