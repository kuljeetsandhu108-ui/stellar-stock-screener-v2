import React, { useState, useRef } from 'react';
import styled from 'styled-components';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa';

// --- Styled Components ---

const TabsContainer = styled.div`
  width: 100%;
  position: relative;
`;

const TabListWrapper = styled.div`
  position: relative;
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--color-border);
  margin-bottom: 2rem;
`;

const TabList = styled.div`
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  width: 100%;
  
  &::-webkit-scrollbar {
    display: none;
  }
  -ms-overflow-style: none;
  scrollbar-width: none;
`;

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
  margin-bottom: -1px;
  border: 1px solid transparent;
  white-space: nowrap; /* Critical for scrolling */
  flex-shrink: 0;      /* Critical for scrolling */

  &:hover {
    background-color: var(--color-secondary);
  }

  ${({ active }) => active && `
    background-color: var(--color-secondary);
    border-color: var(--color-border) var(--color-border) transparent var(--color-border);
  `}
`;

// Reusing the same arrow logic for consistency
const ScrollButton = styled.button`
  position: absolute;
  top: 0;
  bottom: 0;
  width: 30px; /* Slightly smaller for nested tabs */
  border: none;
  cursor: pointer;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-secondary);
  font-size: 0.8rem;
  transition: opacity 0.2s;
  
  &.left {
    left: 0;
    background: linear-gradient(to right, var(--color-secondary) 40%, transparent 100%);
  }
  
  &.right {
    right: 0;
    background: linear-gradient(to left, var(--color-secondary) 40%, transparent 100%);
  }

  &:hover {
    color: var(--color-primary);
  }
`;

const TabContent = styled.div`
  padding: 1rem 0;
`;

// --- The Logic ---

const NestedTabs = ({ children }) => {
  const [activeTab, setActiveTab] = useState(children[0].props.label);
  const scrollRef = useRef(null);

  const handleClick = (e, newActiveTab) => {
    e.preventDefault();
    setActiveTab(newActiveTab);
    e.target.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
  };

  const scroll = (direction) => {
    if (scrollRef.current) {
      const { current } = scrollRef;
      const scrollAmount = 150;
      if (direction === 'left') {
        current.scrollLeft -= scrollAmount;
      } else {
        current.scrollLeft += scrollAmount;
      }
    }
  };

  return (
    <TabsContainer>
      <TabListWrapper>
        <ScrollButton className="left" onClick={() => scroll('left')}><FaChevronLeft /></ScrollButton>
        
        <TabList ref={scrollRef}>
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

        <ScrollButton className="right" onClick={() => scroll('right')}><FaChevronRight /></ScrollButton>
      </TabListWrapper>

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

const NestedTabPanel = ({ label, children }) => {
  return <div label={label}>{children}</div>;
};

export { NestedTabs, NestedTabPanel };