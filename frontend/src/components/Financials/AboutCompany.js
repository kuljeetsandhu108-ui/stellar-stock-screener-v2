import React from 'react';
import styled from 'styled-components';

// --- Styled Components ---

const AboutContainer = styled.div`
  /* Styling for the container if needed in the future */
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--color-text-primary);
`;

const Description = styled.p`
  font-size: 1rem;
  color: var(--color-text-secondary);
  line-height: 1.7; /* Generous line spacing for readability */
`;


// --- The React Component ---

const AboutCompany = ({ profile }) => {
  // Defensive check: If there is no profile or description, render nothing.
  if (!profile || !profile.description) {
    return null;
  }

  return (
    <AboutContainer>
      <SectionTitle>About {profile.companyName}</SectionTitle>
      <Description>
        {profile.description}
      </Description>
    </AboutContainer>
  );
};

export default AboutCompany;