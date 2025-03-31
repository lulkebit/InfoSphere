# InfoSphere - News Aggregator

InfoSphere is a web-based news aggregator that collects news from various sources and presents them in a user-friendly interface. Built with Django and PostgreSQL, this application demonstrates a full relational database implementation with a modern web frontend.

## Features

- Browse news articles from various sources
- Filter news by categories and sources
- Search functionality for finding specific news
- User authentication system
- Personal bookmarks for saving articles
- Commenting system for user engagement
- User preferences for customization (dark mode, preferred categories and sources)

## Tech Stack

- **Backend**: Django 5.1
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript

## Database Schema

The application uses a relational database model with the following tables:

- **Categories**: Stores news categories
- **Sources**: Information about news sources
- **News**: The main news articles
- **News_Categories**: Many-to-many relationship between news and categories
- **Users**: User account information (uses Django's built-in User model)
- **User_News**: Relationship between users and news
- **Comments**: User comments on news articles
- **Bookmarks**: User's saved articles
- **User_Preferences**: User customization settings

## Installation and Setup

### Prerequisites

- Python 3.8+
- PostgreSQL 13+
- pip (Python package manager)

### Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/infosphere.git
   cd infosphere
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a PostgreSQL database:
   ```
   createdb infosphere_db
   ```

5. Configure the database in `settings.py` (already done if using the provided code)

6. Run migrations:
   ```
   python manage.py migrate
   ```

7. Populate the database with sample data:
   ```
   python manage.py populate_db
   ```

8. Create a superuser (admin):
   ```
   python manage.py createsuperuser
   ```

9. Run the development server:
   ```
   python manage.py runserver
   ```

10. Access the application at http://127.0.0.1:8000/

## Sample Login

After running the `populate_db` command, you can log in with:
- Username: `testuser`
- Password: `testpassword`

## SQL Queries

The `sql_queries.sql` file contains various SQL queries that demonstrate the relational aspects of the database, including:

- Table creation statements
- Basic SELECT queries
- Advanced queries with JOINs and aggregations
- Search operations
- INSERT, UPDATE, DELETE examples
- Transaction examples
- Views and indexes

## Screenshots

(Screenshots would be added here)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributors

- Your Name 