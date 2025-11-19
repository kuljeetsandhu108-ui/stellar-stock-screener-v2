import React, { useState, Children, isValidElement } from 'react';
import styled from 'styled-components';

// --- Styled Components ---

const TabsContainer = styled.div`
  width: 100%;
`;

const TabList = styled.div`
  display: flex;
  border-bottom: 2px solid var(--color-border);
  /* Allows tabs to be scrollable on small screens if they overflow */
  overflow-x: auto;

  /* Hide scrollbar for a cleaner look, but keep functionality */
  &::-webkit-scrollbar {
    height: 2px;
  }
  &::-webkit-scrollbar-thumb {
    background: var(--color-border);
  }
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
  white-space: nowrap; /* Prevents tab names from wrapping */

  &:hover {
    color: var(--color-text-primary);
  }

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

const TabContentContainer = styled.div`
  padding: 2rem 0;
`;

// This is the intelligent wrapper that hides inactive tabs instead of destroying them.
const TabPanelWrapper = styled.div`
  display: ${({ active }) => (active ? 'block' : 'none')};
`;


// --- THIS IS THE NEW, ROBUST, AND PROFESSIONALLY ARCHITECTED TABS COMPONENT ---
const Tabs = ({ children }) => {
  // --- THIS IS THE CRITICAL FIX ---
  
  // 1. We use React's built-in 'Children.toArray' and 'isValidElement' utilities.
  // This is the professional way to handle 'children' props. It automatically
  // filters out any null, false, or undefined values that result from
  // conditional rendering (like our `{chartAnalysisData && <TabPanel.../>}`).
  const validChildren = Children.toArray(children).filter(isValidElement);

  // 2. We can now safely get the label of the *first valid* child to set our
  // initial active tab. This prevents the "Cannot read properties of undefined" crash.
  const [activeTab, setActiveTab] = useState(validChildren[0]?.props.label);

  const handleClick = (e, newActiveTab) => {
    e.preventDefault();
    setActiveTab(newActiveTab);
  };

  return (
    <TabsContainer>
      <TabList>
        {/* We map over our new, clean array of only valid <TabPanel> components */}
        {validChildren.map(child => (
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
        {/* We map over the children again and wrap each one in our intelligent wrapper */}
        {/* The wrapper uses CSS 'display: none' to hide inactive tabs, preserving their state. */}
        {validChildren.map(child => (
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

// The TabPanel component remains a simple "dummy" component whose only job
// is to hold a 'label' prop and its own children.
const TabPanel = ({ label, children }) => {
  return <div label={label}>{children}</div>;
};

export { Tabs, TabPanel };