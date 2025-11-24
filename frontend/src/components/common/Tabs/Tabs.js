import React, { useState, useRef, Children, isValidElement } from 'react';
import styled from 'styled-components';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa';

// --- Styled Components ---

const TabsContainer = styled.div`
  width: 100%;
  position: relative; /* Needed for absolute positioning of arrows */
`;

const TabListWrapper = styled.div`
  position: relative;
  display: flex;
  align-items: center;
  border-bottom: 2px solid var(--color-border);
`;

const TabList = styled.div`
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  width: 100%;
  
  /* Hide scrollbar for a clean, native-app feel */
  &::-webkit-scrollbar {
    display: none;
  }
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
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
  white-space: nowrap; /* Critical: prevents text from wrapping */
  flex-shrink: 0; /* Critical: prevents buttons from squishing */

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

// --- The Scroll Arrow Buttons ---
const ScrollButton = styled.button`
  position: absolute;
  top: 0;
  bottom: 0;
  width: 40px;
  border: none;
  cursor: pointer;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
  font-size: 1rem;
  transition: opacity 0.2s;
  
  /* High-end gradient effect to fade content behind the arrow */
  &.left {
    left: 0;
    background: linear-gradient(to right, var(--color-background) 40%, transparent 100%);
  }
  
  &.right {
    right: 0;
    background: linear-gradient(to left, var(--color-background) 40%, transparent 100%);
  }

  &:hover {
    color: var(--color-text-primary);
  }

  /* Only show arrows on devices where scrolling might be needed */
  @media (min-width: 768px) {
     /* Optional: You can hide them on large desktop if you prefer, 
        but keeping them ensures usability everywhere */
  }
`;

const TabContentContainer = styled.div`
  padding: 2rem 0;
`;

const TabPanelWrapper = styled.div`
  display: ${({ active }) => (active ? 'block' : 'none')};
`;


// --- The Logic ---

const Tabs = ({ children }) => {
  const validChildren = Children.toArray(children).filter(isValidElement);
  const [activeTab, setActiveTab] = useState(validChildren[0]?.props.label);
  const scrollRef = useRef(null);

  const handleClick = (e, newActiveTab) => {
    e.preventDefault();
    setActiveTab(newActiveTab);
    
    // Optional: Auto-scroll the active tab into view
    e.target.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
  };

  const scroll = (direction) => {
    if (scrollRef.current) {
      const { current } = scrollRef;
      const scrollAmount = 200; // Adjust scroll speed
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
        {/* Left Arrow */}
        <ScrollButton className="left" onClick={() => scroll('left')} aria-label="Scroll Left">
          <FaChevronLeft />
        </ScrollButton>

        <TabList ref={scrollRef}>
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

        {/* Right Arrow */}
        <ScrollButton className="right" onClick={() => scroll('right')} aria-label="Scroll Right">
          <FaChevronRight />
        </ScrollButton>
      </TabListWrapper>

      <TabContentContainer>
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

const TabPanel = ({ label, children }) => {
  return <div label={label}>{children}</div>;
};

export { Tabs, TabPanel };