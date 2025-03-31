-- SQL Queries for InfoSphere News Aggregator

-- 1. Create tables based on the relational model
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE sources (
    source_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    website_url VARCHAR(255) NOT NULL,
    country VARCHAR(100) NOT NULL
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) NOT NULL,
    password VARCHAR(128) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE news (
    news_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(100),
    image_url VARCHAR(255),
    published_at TIMESTAMP WITH TIME ZONE NOT NULL,
    source_id INTEGER REFERENCES sources(source_id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    url VARCHAR(255) NOT NULL
);

CREATE TABLE news_categories (
    news_id INTEGER REFERENCES news(news_id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(category_id) ON DELETE CASCADE,
    PRIMARY KEY (news_id, category_id)
);

CREATE TABLE user_news (
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    news_id INTEGER REFERENCES news(news_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, news_id)
);

CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    news_id INTEGER REFERENCES news(news_id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE bookmarks (
    bookmark_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    news_id INTEGER REFERENCES news(news_id) ON DELETE CASCADE,
    saved_at TIMESTAMP WITH TIME ZONE NOT NULL,
    UNIQUE (user_id, news_id)
);

CREATE TABLE user_preferences (
    pref_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE UNIQUE,
    dark_mode BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE user_preferred_sources (
    pref_id INTEGER REFERENCES user_preferences(pref_id) ON DELETE CASCADE,
    source_id INTEGER REFERENCES sources(source_id) ON DELETE CASCADE,
    PRIMARY KEY (pref_id, source_id)
);

CREATE TABLE user_preferred_categories (
    pref_id INTEGER REFERENCES user_preferences(pref_id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(category_id) ON DELETE CASCADE,
    PRIMARY KEY (pref_id, category_id)
);

-- 2. Basic SELECT queries

-- Get all news articles with their source and categories
SELECT n.news_id, n.title, n.content, n.author, n.published_at, s.name AS source_name, 
       STRING_AGG(c.name, ', ') AS categories
FROM news n
JOIN sources s ON n.source_id = s.source_id
LEFT JOIN news_categories nc ON n.news_id = nc.news_id
LEFT JOIN categories c ON nc.category_id = c.category_id
GROUP BY n.news_id, n.title, n.content, n.author, n.published_at, s.name
ORDER BY n.published_at DESC;

-- Get all news articles for a specific category
SELECT n.news_id, n.title, n.content, n.author, n.published_at, s.name AS source_name
FROM news n
JOIN sources s ON n.source_id = s.source_id
JOIN news_categories nc ON n.news_id = nc.news_id
JOIN categories c ON nc.category_id = c.category_id
WHERE c.name = 'Technology'
ORDER BY n.published_at DESC;

-- Get all news articles from a specific source
SELECT n.news_id, n.title, n.content, n.author, n.published_at
FROM news n
JOIN sources s ON n.source_id = s.source_id
WHERE s.name = 'BBC News'
ORDER BY n.published_at DESC;

-- Get all bookmarks for a specific user with news details
SELECT b.bookmark_id, n.title, n.content, n.author, s.name AS source_name, b.saved_at
FROM bookmarks b
JOIN news n ON b.news_id = n.news_id
JOIN sources s ON n.source_id = s.source_id
WHERE b.user_id = 1
ORDER BY b.saved_at DESC;

-- Get all comments for a specific news article with user details
SELECT c.comment_id, u.username, c.content, c.created_at
FROM comments c
JOIN users u ON c.user_id = u.user_id
WHERE c.news_id = 1
ORDER BY c.created_at;

-- 3. Advanced queries

-- Count news by category
SELECT c.name, COUNT(nc.news_id) AS news_count
FROM categories c
LEFT JOIN news_categories nc ON c.category_id = nc.category_id
GROUP BY c.name
ORDER BY news_count DESC;

-- Count news by source
SELECT s.name, COUNT(n.news_id) AS news_count
FROM sources s
LEFT JOIN news n ON s.source_id = n.source_id
GROUP BY s.name
ORDER BY news_count DESC;

-- Get news with their comment counts
SELECT n.news_id, n.title, COUNT(c.comment_id) AS comment_count
FROM news n
LEFT JOIN comments c ON n.news_id = c.news_id
GROUP BY n.news_id, n.title
ORDER BY comment_count DESC;

-- Get users with their bookmark counts
SELECT u.username, COUNT(b.bookmark_id) AS bookmark_count
FROM users u
LEFT JOIN bookmarks b ON u.user_id = b.user_id
GROUP BY u.username
ORDER BY bookmark_count DESC;

-- Find news articles that match user's preferred categories
SELECT DISTINCT n.news_id, n.title, n.content, n.published_at
FROM news n
JOIN news_categories nc ON n.news_id = nc.news_id
JOIN user_preferred_categories upc ON nc.category_id = upc.category_id
JOIN user_preferences up ON upc.pref_id = up.pref_id
WHERE up.user_id = 1
ORDER BY n.published_at DESC;

-- Find news articles that match user's preferred sources
SELECT n.news_id, n.title, n.content, n.published_at
FROM news n
JOIN sources s ON n.source_id = s.source_id
JOIN user_preferred_sources ups ON s.source_id = ups.source_id
JOIN user_preferences up ON ups.pref_id = up.pref_id
WHERE up.user_id = 1
ORDER BY n.published_at DESC;

-- 4. Search queries

-- Search for news by keyword in title or content
SELECT n.news_id, n.title, n.content, n.published_at, s.name AS source_name
FROM news n
JOIN sources s ON n.source_id = s.source_id
WHERE n.title ILIKE '%climate%' OR n.content ILIKE '%climate%'
ORDER BY n.published_at DESC;

-- Search for news by author
SELECT n.news_id, n.title, n.content, n.published_at, s.name AS source_name
FROM news n
JOIN sources s ON n.source_id = s.source_id
WHERE n.author ILIKE '%Johnson%'
ORDER BY n.published_at DESC;

-- 5. Insert examples

-- Insert a new category
INSERT INTO categories (name) VALUES ('Science Fiction');

-- Insert a new source
INSERT INTO sources (name, website_url, country) 
VALUES ('CNN', 'https://cnn.com', 'United States');

-- Insert a new news article
INSERT INTO news (title, content, author, image_url, published_at, source_id, created_at, updated_at, is_read, url)
VALUES (
    'New Discovery on Mars',
    'Scientists have found evidence of ancient rivers on Mars, suggesting the planet once had a much wetter climate.',
    'John Smith',
    'https://example.com/images/mars_discovery.jpg',
    NOW(),
    1,
    NOW(),
    NOW(),
    FALSE,
    'https://example.com/news/mars-discovery'
);

-- Associate the news article with categories
INSERT INTO news_categories (news_id, category_id)
VALUES 
    (CURRVAL('news_news_id_seq'), (SELECT category_id FROM categories WHERE name = 'Science')),
    (CURRVAL('news_news_id_seq'), (SELECT category_id FROM categories WHERE name = 'Science Fiction'));

-- 6. Update examples

-- Update a news article
UPDATE news
SET 
    title = 'Updated: New Discovery on Mars',
    content = 'Updated content about the discovery on Mars.',
    updated_at = NOW()
WHERE news_id = CURRVAL('news_news_id_seq');

-- Mark a news article as read
UPDATE news
SET is_read = TRUE
WHERE news_id = 1;

-- 7. Delete examples

-- Delete a bookmark
DELETE FROM bookmarks
WHERE user_id = 1 AND news_id = 5;

-- Delete a comment
DELETE FROM comments
WHERE comment_id = 3;

-- 8. Transaction example

-- Create a new user with preferences in a transaction
BEGIN;

INSERT INTO users (username, email, password, is_active, date_joined)
VALUES ('newuser', 'newuser@example.com', 'hashed_password', TRUE, NOW());

INSERT INTO user_preferences (user_id, dark_mode)
VALUES (CURRVAL('users_user_id_seq'), TRUE);

INSERT INTO user_preferred_categories (pref_id, category_id)
VALUES
    (CURRVAL('user_preferences_pref_id_seq'), (SELECT category_id FROM categories WHERE name = 'Technology')),
    (CURRVAL('user_preferences_pref_id_seq'), (SELECT category_id FROM categories WHERE name = 'Science'));

INSERT INTO user_preferred_sources (pref_id, source_id)
VALUES
    (CURRVAL('user_preferences_pref_id_seq'), (SELECT source_id FROM sources WHERE name = 'BBC News'));

COMMIT;

-- 9. Views

-- Create a view for the most popular news articles (by comment count)
CREATE VIEW popular_news AS
SELECT n.news_id, n.title, n.content, n.published_at, s.name AS source_name, COUNT(c.comment_id) AS comment_count
FROM news n
JOIN sources s ON n.source_id = s.source_id
LEFT JOIN comments c ON n.news_id = c.news_id
GROUP BY n.news_id, n.title, n.content, n.published_at, s.name
ORDER BY comment_count DESC;

-- Create a view for user activity
CREATE VIEW user_activity AS
SELECT 
    u.user_id, 
    u.username,
    COUNT(DISTINCT b.news_id) AS bookmark_count,
    COUNT(DISTINCT c.comment_id) AS comment_count
FROM users u
LEFT JOIN bookmarks b ON u.user_id = b.user_id
LEFT JOIN comments c ON u.user_id = c.user_id
GROUP BY u.user_id, u.username;

-- 10. Indexes

-- Create indexes for performance optimization
CREATE INDEX idx_news_published_at ON news(published_at);
CREATE INDEX idx_news_title ON news(title);
CREATE INDEX idx_news_author ON news(author);
CREATE INDEX idx_comments_created_at ON comments(created_at);
CREATE INDEX idx_bookmarks_saved_at ON bookmarks(saved_at);
CREATE INDEX idx_news_categories_category_id ON news_categories(category_id);
CREATE INDEX idx_news_source_id ON news(source_id); 