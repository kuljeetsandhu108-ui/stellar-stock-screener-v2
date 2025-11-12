import React, { useState } from 'react';
import styled from 'styled-components';

// --- (Styled Components are mostly unchanged) ---

const TabsContainer = styled.div`
  width: 100%;
`;

const TabList = styled.div`
  display: flex;
  border-bottom: 2px solid var(--color-border);
`;

const TabButton = styled.button`
  padding: 1rem 1.5rem;
  border: none;
  background-color: transparent;
  color: ${({ active }) => (active ? 'var(--color-text-primary)' : 'var(--color-text-secondary)')};
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  position: relative;
  transition: color 0.3s ease;

  &:hover {
    color: var(--color-text-primary);
  }

  &::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--color-primary);
    transform: ${({ active }) => (active ? 'scaleX(1)' : 'scaleX(0)')};
    transform-origin: bottom;
    transition: transform 0.3s ease-out;
  }
`;

const TabContentContainer = styled.div`
  padding: 2rem 0;
`;

// --- THIS IS THE NEW, INTELLIGENT TAB PANEL WRAPPER ---
const TabPanelWrapper = styled.div`
  /* If this panel is not the active one, we HIDE it instead of destroying it. */
  display: ${({ active }) => (active ? 'block' : 'none')};
`;


// --- The Upgraded Tabs Component ---

const Tabs = ({ children }) => {
  const [activeTab, setActiveTab] = useState(children[0].props.label);

  const handleClick = (e, newActiveTab) => {
    e.preventDefault();
    setActiveTab(newActiveTab);
  };

  return (
    <TabsContainer>
      <TabList>
        {children.map(child => (
          <TabButton
            key={child.props.label}
            active={activeTab === child.props.label}
            onClick={e => handleClick(e, child.props.label)}
          >
            {child.props.label}
          </TabButton>
        ))}
      </TabList>
      <TabContentContainer>
        {/* We now map over the children and wrap each one in our new intelligent wrapper */}
        {children.map(child => (
          <TabPanelWrapper
            key={child.props.label}
            active={activeTab === child.props.label}
          >
            {child.props.children}
          </TabPanelWrapper>
        ))}
      </TabContentContainer>
    </TabsContainer>
  );
};

// The TabPanel component remains a simple "dummy" component.
const TabPanel = ({ label, children }) => {
  return <div label={label}>{children}</div>;
};

export { Tabs, TabPanel };