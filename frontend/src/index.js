import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Find the div with the id of 'root' in the index.html file
const rootElement = document.getElementById('root');

// Create a root for our React application to render into
const root = ReactDOM.createRoot(rootElement);

// Render the main App component
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);