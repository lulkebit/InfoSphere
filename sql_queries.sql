-- InfoSphere News Aggregator - SQL Queries
-- This file contains SQL queries for the InfoSphere application database operations

-- =============================================
-- TABLE CREATION QUERIES
-- =============================================

-- Create Category table
CREATE TABLE IF NOT EXISTS "Category" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Create Source table
CREATE TABLE IF NOT EXISTS "Source" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    website_url VARCHAR(200) NOT NULL,
    country VARCHAR(100) NOT NULL
);

-- Create News table
CREATE TABLE IF NOT EXISTS "News" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(100),
    image_url VARCHAR(200),
    published_at TIMESTAMP NOT NULL,
    source_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    url VARCHAR(200) NOT NULL,
    FOREIGN KEY (source_id) REFERENCES "Source" (id) ON DELETE CASCADE
);

-- Create NewsCategory table (many-to-many relationship)
CREATE TABLE IF NOT EXISTS "NewsCategory" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    news_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (news_id) REFERENCES "News" (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES "Category" (id) ON DELETE CASCADE,
    UNIQUE (news_id, category_id)
);

-- Create UserNews table (many-to-many relationship)
CREATE TABLE IF NOT EXISTS "UserNews" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    news_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES "auth_user" (id) ON DELETE CASCADE,
    FOREIGN KEY (news_id) REFERENCES "News" (id) ON DELETE CASCADE,
    UNIQUE (user_id, news_id)
);

-- Create Comment table
CREATE TABLE IF NOT EXISTS "Comment" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    news_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES "auth_user" (id) ON DELETE CASCADE,
    FOREIGN KEY (news_id) REFERENCES "News" (id) ON DELETE CASCADE
);

-- Create Bookmark table
CREATE TABLE IF NOT EXISTS "Bookmark" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    news_id INTEGER NOT NULL,
    saved_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES "auth_user" (id) ON DELETE CASCADE,
    FOREIGN KEY (news_id) REFERENCES "News" (id) ON DELETE CASCADE,
    UNIQUE (user_id, news_id)
);

-- Create UserPreference table
CREATE TABLE IF NOT EXISTS "UserPreference" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    dark_mode BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES "auth_user" (id) ON DELETE CASCADE
);

-- Create UserPreferenceSource table (many-to-many relationship)
CREATE TABLE IF NOT EXISTS "UserPreferenceSource" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userpreference_id INTEGER NOT NULL,
    source_id INTEGER NOT NULL,
    FOREIGN KEY (userpreference_id) REFERENCES "UserPreference" (id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES "Source" (id) ON DELETE CASCADE,
    UNIQUE (userpreference_id, source_id)
);

-- Create UserPreferenceCategory table (many-to-many relationship)
CREATE TABLE IF NOT EXISTS "UserPreferenceCategory" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userpreference_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (userpreference_id) REFERENCES "UserPreference" (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES "Category" (id) ON DELETE CASCADE,
    UNIQUE (userpreference_id, category_id)
);

-- =============================================
-- INDEX CREATION QUERIES
-- =============================================

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_news_published_at ON "News" (published_at);
CREATE INDEX IF NOT EXISTS idx_news_source_id ON "News" (source_id);
CREATE INDEX IF NOT EXISTS idx_newscategory_news_id ON "NewsCategory" (news_id);
CREATE INDEX IF NOT EXISTS idx_newscategory_category_id ON "NewsCategory" (category_id);
CREATE INDEX IF NOT EXISTS idx_comment_news_id ON "Comment" (news_id);
CREATE INDEX IF NOT EXISTS idx_bookmark_user_id ON "Bookmark" (user_id);
CREATE INDEX IF NOT EXISTS idx_bookmark_news_id ON "Bookmark" (news_id);

-- =============================================
-- BASIC SELECT QUERIES
-- =============================================

-- Get all news articles ordered by publication date (descending)
-- Used in the home view to display the latest news
SELECT n.id, n.title, n.content, n.author, n.published_at, s.name AS source_name
FROM "News" n
JOIN "Source" s ON n.source_id = s.id
ORDER BY n.published_at DESC;

-- Get all categories
-- Used in the home view to populate category filters
SELECT id, name FROM "Category";

-- Get all news sources
-- Used in the home view to populate source filters
SELECT id, name, website_url, country FROM "Source";

-- =============================================
-- FILTERING QUERIES
-- =============================================

-- Filter news by category
-- Used when users select category filters on the home page
SELECT DISTINCT n.id, n.title, n.content, n.published_at, s.name AS source_name
FROM "News" n
JOIN "Source" s ON n.source_id = s.id
JOIN "NewsCategory" nc ON n.id = nc.news_id
WHERE nc.category_id = ?
ORDER BY n.published_at DESC;

-- Filter news by source
-- Used when users select source filters on the home page
SELECT n.id, n.title, n.content, n.published_at, s.name AS source_name
FROM "News" n
JOIN "Source" s ON n.source_id = s.id
WHERE n.source_id = ?
ORDER BY n.published_at DESC;

-- Filter news by multiple categories
-- Used when users select multiple category filters
SELECT DISTINCT n.id, n.title, n.content, n.published_at, s.name AS source_name
FROM "News" n
JOIN "Source" s ON n.source_id = s.id
JOIN "NewsCategory" nc ON n.id = nc.news_id
WHERE nc.category_id IN (?, ?, ?)  -- Parameter values will be category IDs
ORDER BY n.published_at DESC;

-- Filter news by multiple sources
-- Used when users select multiple source filters
SELECT n.id, n.title, n.content, n.published_at, s.name AS source_name
FROM "News" n
JOIN "Source" s ON n.source_id = s.id
WHERE n.source_id IN (?, ?, ?)  -- Parameter values will be source IDs
ORDER BY n.published_at DESC;

-- =============================================
-- SEARCH QUERIES
-- =============================================

-- Search news by keyword (in title, content, or author)
-- Used when users enter search terms in the search box
SELECT n.id, n.title, n.content, n.published_at, s.name AS source_name
FROM "News" n
JOIN "Source" s ON n.source_id = s.id
WHERE n.title LIKE '%?%' OR n.content LIKE '%?%' OR n.author LIKE '%?%'  -- Parameter value will be the search keyword
ORDER BY n.published_at DESC;

-- =============================================
-- JOIN QUERIES
-- =============================================

-- Get a single news article with its categories
-- Used in the news_detail view
SELECT n.id, n.title, n.content, n.author, n.image_url, n.published_at, n.url, 
       s.id AS source_id, s.name AS source_name, s.website_url,
       GROUP_CONCAT(c.name) AS categories
FROM "News" n
JOIN "Source" s ON n.source_id = s.id
LEFT JOIN "NewsCategory" nc ON n.id = nc.news_id
LEFT JOIN "Category" c ON nc.category_id = c.id
WHERE n.id = ?  -- Parameter value will be the news ID
GROUP BY n.id;

-- Get comments for a news article
-- Used in the news_detail view to display comments
SELECT c.id, c.content, c.created_at, u.username
FROM "Comment" c
JOIN "auth_user" u ON c.user_id = u.id
WHERE c.news_id = ?  -- Parameter value will be the news ID
ORDER BY c.created_at DESC;

-- Get bookmarked news for a user
-- Used in the bookmarks view
SELECT n.id, n.title, n.content, n.published_at, s.name AS source_name, b.saved_at
FROM "News" n
JOIN "Source" s ON n.source_id = s.id
JOIN "Bookmark" b ON n.id = b.news_id
WHERE b.user_id = ?  -- Parameter value will be the user ID
ORDER BY b.saved_at DESC;

-- =============================================
-- AGGREGATION QUERIES
-- =============================================

-- Count news articles per category
-- Used in the categories view
SELECT c.id, c.name, COUNT(nc.news_id) AS news_count
FROM "Category" c
LEFT JOIN "NewsCategory" nc ON c.id = nc.category_id
GROUP BY c.id
ORDER BY c.name;

-- Count news articles per source
-- Used in the sources view
SELECT s.id, s.name, COUNT(n.id) AS news_count
FROM "Source" s
LEFT JOIN "News" n ON s.id = n.source_id
GROUP BY s.id
ORDER BY s.name;

-- =============================================
-- INSERT QUERIES
-- =============================================

-- Insert a new category
INSERT INTO "Category" (name)
VALUES (?);  -- Parameter value will be the category name

-- Insert a new source
INSERT INTO "Source" (name, website_url, country)
VALUES (?, ?, ?);  -- Parameter values will be the source name, website URL, and country

-- Insert a new news article
INSERT INTO "News" (title, content, author, image_url, published_at, source_id, created_at, updated_at, is_read, url)
VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE, ?);

-- Add a category to a news article
INSERT INTO "NewsCategory" (news_id, category_id)
VALUES (?, ?);  -- Parameter values will be the news ID and category ID

-- =============================================
-- UPDATE QUERIES
-- =============================================

-- Mark a news article as read
-- Used when a user views a news article
UPDATE "News"
SET is_read = TRUE
WHERE id = ?;  -- Parameter value will be the news ID

-- Update user preferences
-- Used in the user_preferences view
UPDATE "UserPreference"
SET dark_mode = ?
WHERE user_id = ?;  -- Parameter values will be the dark_mode boolean and user ID

-- =============================================
-- DELETE QUERIES
-- =============================================

-- Remove a bookmark
-- Used in the toggle_bookmark view when removing a bookmark
DELETE FROM "Bookmark"
WHERE user_id = ? AND news_id = ?;  -- Parameter values will be the user ID and news ID

-- Delete a comment
DELETE FROM "Comment"
WHERE id = ? AND user_id = ?;  -- Parameter values will be the comment ID and user ID (to ensure users can only delete their own comments)

-- =============================================
-- TRANSACTION EXAMPLES
-- =============================================

-- Example of a transaction for adding a news article with categories
BEGIN TRANSACTION;

-- Insert the news article
INSERT INTO "News" (title, content, author, image_url, published_at, source_id, created_at, updated_at, is_read, url)
VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE, ?);

-- Get the ID of the newly inserted news article
-- SQLite-specific way to get the last inserted ID
-- For PostgreSQL, this would be: SELECT lastval();
SET @news_id = LAST_INSERT_ID();

-- Add categories to the news article
INSERT INTO "NewsCategory" (news_id, category_id)
VALUES (@news_id, ?);  -- First category

INSERT INTO "NewsCategory" (news_id, category_id)
VALUES (@news_id, ?);  -- Second category

COMMIT;

-- =============================================
-- VIEW CREATION
-- =============================================

-- Create a view for the latest news with categories
CREATE VIEW IF NOT EXISTS "LatestNews" AS
SELECT n.id, n.title, n.content, n.author, n.published_at, 
       s.name AS source_name, GROUP_CONCAT(c.name) AS categories
FROM "News" n
JOIN "Source" s ON n.source_id = s.id
LEFT JOIN "NewsCategory" nc ON n.id = nc.news_id
LEFT JOIN "Category" c ON nc.category_id = c.id
GROUP BY n.id
ORDER BY n.published_at DESC
LIMIT 50;

-- Create a view for popular categories (most used)
CREATE VIEW IF NOT EXISTS "PopularCategories" AS
SELECT c.id, c.name, COUNT(nc.news_id) AS news_count
FROM "Category" c
JOIN "NewsCategory" nc ON c.id = nc.category_id
GROUP BY c.id
ORDER BY news_count DESC;

-- =============================================
-- COMPLEX QUERIES
-- =============================================

-- Get news recommendations based on user preferences
-- Used to recommend news to users based on their preferred categories and sources
SELECT DISTINCT n.id, n.title, n.content, n.published_at, s.name AS source_name
FROM "News" n
JOIN "Source" s ON n.source_id = s.id
LEFT JOIN "NewsCategory" nc ON n.id = nc.news_id
WHERE s.id IN (
    SELECT source_id 
    FROM "UserPreferenceSource" 
    WHERE userpreference_id = (
        SELECT id FROM "UserPreference" WHERE user_id = ?
    )
)
OR nc.category_id IN (
    SELECT category_id 
    FROM "UserPreferenceCategory" 
    WHERE userpreference_id = (
        SELECT id FROM "UserPreference" WHERE user_id = ?
    )
)
ORDER BY n.published_at DESC;

-- Get unread news articles for a user
SELECT n.id, n.title, n.content, n.published_at, s.name AS source_name
FROM "News" n
JOIN "Source" s ON n.source_id = s.id
LEFT JOIN "UserNews" un ON n.id = un.news_id AND un.user_id = ?
WHERE n.is_read = FALSE OR n.is_read IS NULL
ORDER BY n.published_at DESC;

-- Get trending news (most commented)
SELECT n.id, n.title, COUNT(c.id) AS comment_count
FROM "News" n
LEFT JOIN "Comment" c ON n.id = c.news_id
GROUP BY n.id
ORDER BY comment_count DESC
LIMIT 10;

-- Get news statistics by source and category
SELECT s.name AS source_name, c.name AS category_name, COUNT(DISTINCT n.id) AS news_count
FROM "Source" s
JOIN "News" n ON s.id = n.source_id
JOIN "NewsCategory" nc ON n.id = nc.news_id
JOIN "Category" c ON nc.category_id = c.id
GROUP BY s.id, c.id
ORDER BY news_count DESC;
