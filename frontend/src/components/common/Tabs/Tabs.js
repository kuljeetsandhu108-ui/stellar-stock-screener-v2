import React, { useState } from 'react';
import styled from 'styled-components';

// --- Styled Components ---

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

  /* The active tab indicator line, just like the reference */
  &::after {
    content: '';
    position: absolute;
    bottom: -2px; /* Sits perfectly on top of the container's border */
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--color-primary);
    transform: ${({ active }) => (active ? 'scaleX(1)' : 'scaleX(0)')};
    transform-origin: bottom;
    transition: transform 0.3s ease-out;
  }
`;

const TabContent = styled.div`
  padding: 2rem 0; /* Add some space above and below the tab content */
`;

// --- The Main Tabs Component ---

const Tabs = ({ children }) => {
  // Use the first child's label as the default active tab
  const [activeTab, setActiveTab] = useState(children[0].props.label);

  const handleClick = (e, newActiveTab) => {
    e.preventDefault();
    setActiveTab(newActiveTab);
  };

  return (
    <TabsContainer>
      <TabList>
        {/* Map over the children to create the tab buttons */}
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
        {/* Map over the children again to display the content of the active tab */}
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

// This is a simple "dummy" component that just holds content.
// We export it from here for convenience.
const TabPanel = ({ label, children }) => {
  return <div label={label}>{children}</div>;
};

export { Tabs, TabPanel };