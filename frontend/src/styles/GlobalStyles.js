import { createGlobalStyle } from 'styled-components';

export const GlobalStyles = createGlobalStyle`
  /* CSS Variables for our color palette */
  :root {
    --color-background: #0D1117;       /* Deep, dark blue-grey (like GitHub) */
    --color-primary: #58A6FF;          /* A vibrant, accessible blue */
    --color-secondary: #161B22;       /* Slightly lighter background for cards/containers */
    --color-text-primary: #C9D1D9;     /* Light grey for primary text */
    --color-text-secondary: #8B949E;   /* Darker grey for secondary text/labels */
    --color-border: #30363D;          /* Border color */
    --color-success: #3FB950;          /* Green for positive changes */
    --color-danger: #F85149;           /* Red for negative changes */
    --font-family-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  }

  /* Resetting default styles */
  *,
  *::before,
  *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  html {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  body {
    background-color: var(--color-background);
    color: var(--color-text-primary);
    font-family: var(--font-family-sans);
    line-height: 1.5;
  }

  h1, h2, h3, h4, h5, h6 {
    color: var(--color-text-primary);
    font-weight: 600;
  }

  a {
    color: var(--color-primary);
    text-decoration: none;
  }

  /* Custom scrollbar for a more modern look */
  ::-webkit-scrollbar {
    width: 8px;
  }
  ::-webkit-scrollbar-track {
    background: var(--color-secondary);
  }
  ::-webkit-scrollbar-thumb {
    background: #4A5568; /* A neutral grey */
    border-radius: 4px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: #718096;
  }
`;