import React, { useState } from 'react';
import styled from 'styled-components';

// --- Styled Components for our new, sleek nested tabs ---

const TabsContainer = styled.div`
  width: 100%;
`;

const TabList = styled.div`
  display: flex;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--color-border);
`;

// A different, more subtle button style for nested tabs
const TabButton = styled.button`
  padding: 0.75rem 1.25rem;
  border: none;
  background-color: transparent;
  color: ${({ active }) => (active ? 'var(--color-primary)' : 'var(--color-text-secondary)')};
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  position: relative;
  transition: color 0.3s ease, background-color 0.3s ease;
  border-radius: 6px 6px 0 0;
  margin-bottom: -1px; /* Sits on top of the border */
  border: 1px solid transparent;

  &:hover {
    background-color: var(--color-secondary);
  }

  ${({ active }) => active && `
    background-color: var(--color-secondary);
    border-color: var(--color-border) var(--color-border) transparent var(--color-border);
  `}
`;

const TabContent = styled.div`
  padding: 1rem 0;
`;

// --- The Reusable Components ---

const NestedTabs = ({ children }) => {
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
      <TabContent>
        {children.map(child => {
          if (child.props.label === activeTab) {
            return <div key={child.props.label}>{child.props.children}</div>;
          }
          return null;
        })}
      </TabContent>
    </TabsContainer>
  );
};

// The TabPanel component remains the same simple wrapper.
const NestedTabPanel = ({ label, children }) => {
  return <div label={label}>{children}</div>;
};

export { NestedTabs, NestedTabPanel };