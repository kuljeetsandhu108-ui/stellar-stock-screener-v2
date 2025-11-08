import React from 'react';
import styled from 'styled-components';
import Card from '../common/Card';

// --- Styled Components ---

const NewsListContainer = styled.ul`
  list-style-type: none;
  padding: 0;
  margin: 0;
  /* Allows the list to scroll if it's too long */
  max-height: 500px;
  overflow-y: auto;
`;

const NewsItem = styled.li`
  padding: 1rem 0.5rem;
  border-bottom: 1px solid var(--color-border);
  
  &:last-child {
    border-bottom: none; /* Remove border for the last item */
  }
`;

const NewsLink = styled.a`
  text-decoration: none;
  color: var(--color-text-primary);
  transition: color 0.2s ease;

  &:hover {
    color: var(--color-primary);
  }
`;

const NewsTitle = styled.h4`
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
`;

const NewsMeta = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: var(--color-text-secondary);
`;

// --- Helper Function ---

// Formats the ISO date string into a more readable format, e.g., "Nov 08, 2025"
const formatDate = (isoString) => {
  if (!isoString) return '';
  const date = new Date(isoString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: '2-digit',
    year: 'numeric',
  });
};


// --- React Component ---

const NewsList = ({ newsArticles }) => {

  // Defensive check: If there are no articles, show a message.
  if (!newsArticles || !Array.isArray(newsArticles) || newsArticles.length === 0) {
    return (
      <Card title="Latest News">
        <p>No recent news found for this company.</p>
      </Card>
    );
  }

  return (
    <Card title="Latest News">
      <NewsListContainer>
        {/* We'll show the top 15 articles */}
        {newsArticles.slice(0, 15).map((article, index) => (
          <NewsItem key={index}>
            <NewsLink href={article.url} target="_blank" rel="noopener noreferrer">
              <NewsTitle>{article.title}</NewsTitle>
              <NewsMeta>
                <span>{article.source.name}</span>
                <span>{formatDate(article.publishedAt)}</span>
              </NewsMeta>
            </NewsLink>
          </NewsItem>
        ))}
      </NewsListContainer>
    </Card>
  );
};

export default NewsList;