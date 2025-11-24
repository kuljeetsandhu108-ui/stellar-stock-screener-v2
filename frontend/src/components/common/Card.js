import React from 'react';
import styled from 'styled-components';

// This is our master styled component for all content blocks.
const CardContainer = styled.div`
  background-color: var(--color-secondary);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  margin-bottom: 1.5rem; 
  width: 100%;
  
  /* Mobile: Tight padding */
  padding: 1rem; 

  /* Desktop: Luxurious padding */
  @media (min-width: 768px) {
    padding: 2rem;
    margin-bottom: 2rem;
    
  }
`;

const CardHeader = styled.div`
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border);
`;

const CardTitle = styled.h2`
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text-primary);
`;

const CardContent = styled.div`
  /* The content inside the card will be placed here */
`;

// This is a reusable React component that accepts a title and content.
const Card = ({ title, children }) => {
  return (
    <CardContainer>
      {/* The title is optional; if a title is provided, the header will render. */}
      {title && (
        <CardHeader>
          <CardTitle>{title}</CardTitle>
        </CardHeader>
      )}
      <CardContent>
        {/* 'children' is a special prop in React that lets us pass components inside other components.
            Whatever we place inside <Card>...</Card> will be rendered here. */}
        {children}
      </CardContent>
    </CardContainer>
  );
};

export default Card;