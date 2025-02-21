import requests
from datetime import datetime
from django.conf import settings
from .models import Message
from dateutil import parser

class NewsService:
    def __init__(self):
        self.api_key = settings.MEDIASTACK_API_KEY
        self.base_url = "http://api.mediastack.com/v1"

    def fetch_news(self, categories=None, countries='de', limit=100):
        """Fetch news from Mediastack API"""
        endpoint = f"{self.base_url}/news"
        params = {
            'access_key': self.api_key,
            'countries': countries,
            'limit': limit,
            'sort': 'published_desc'
        }
        if categories:
            params['categories'] = ','.join(categories)

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
            return None

    def save_articles(self, articles, category=None):
        """Save articles to database"""
        for article in articles:
            try:
                # Verwenden Sie dateutil.parser für flexibles Datum-Parsing
                published_at = parser.parse(article.get('published_at')) if article.get('published_at') else None
                
                # Set priority based on category
                priority = 'HIGH' if category in ['business', 'technology'] else 'MEDIUM'
                
                Message.objects.create(
                    title=article.get('title', ''),
                    content=article.get('description', ''),
                    source_name=article.get('source', ''),
                    author=article.get('author', ''),
                    url=article.get('url', ''),
                    image_url=article.get('image', ''),
                    published_at=published_at,
                    category=category or article.get('category', ''),
                    priority=priority
                )
            except Exception as e:
                print(f"Error saving article: {e}")

    def update_news(self):
        """Fetch and save news articles"""
        # Mediastack categories: general, business, technology, science, health, sports, entertainment
        categories = ['business', 'technology', 'science', 'health']
        
        # Fetch news for all categories at once (Mediastack supports this)
        data = self.fetch_news(categories=categories)
        if data and 'data' in data:
            self.save_articles(data['data']) 