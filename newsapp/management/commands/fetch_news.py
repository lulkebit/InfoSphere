import requests
import json
import logging
import os
import pytz
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from newsapp.models import Category, Source, News, NewsCategory, UserNews

# Set up logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetches news from public APIs and stores them in the database'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=10, help='Limit the number of articles to fetch per source')
        parser.add_argument('--mock', action='store_true', help='Use mock data instead of real API calls')

    def handle(self, *args, **options):
        self.stdout.write('Fetching news from APIs...')
        self.limit = options['limit']
        self.use_mock = options['mock']
        
        # If not using mock data, we need API keys
        if not self.use_mock:
            # In production, these would be stored in environment variables or Django settings
            self.news_api_key = os.environ.get('NEWS_API_KEY', '')
            self.gnews_api_key = os.environ.get('GNEWS_API_KEY', '')
            
            if not self.news_api_key or not self.gnews_api_key:
                self.stdout.write(self.style.WARNING('API keys not found. Using mock data instead.'))
                self.use_mock = True
        
        # Fetch from NewsAPI
        try:
            self.fetch_from_newsapi()
        except Exception as e:
            logger.error(f"Error fetching from NewsAPI: {str(e)}")
            self.stdout.write(self.style.ERROR(f"Error fetching from NewsAPI: {str(e)}"))
        
        # Fetch from GNews
        try:
            self.fetch_from_gnews()
        except Exception as e:
            logger.error(f"Error fetching from GNews: {str(e)}")
            self.stdout.write(self.style.ERROR(f"Error fetching from GNews: {str(e)}"))
        
        # Cleanup old news (optional - removes news older than 30 days)
        # self.cleanup_old_news()
        
        self.stdout.write(self.style.SUCCESS('News fetch completed!'))

    def fetch_from_newsapi(self):
        """Fetch news from NewsAPI and save to database"""
        self.stdout.write("Fetching from NewsAPI...")
        
        api_endpoint = "https://newsapi.org/v2/top-headlines"
        
        # Define sources to be created if they don't exist
        sources = {
            "bbc-news": {
                "name": "BBC News",
                "website_url": "https://www.bbc.co.uk/news",
                "country": "United Kingdom"
            },
            "cnn": {
                "name": "CNN",
                "website_url": "https://www.cnn.com",
                "country": "United States"
            },
            "the-washington-post": {
                "name": "The Washington Post",
                "website_url": "https://www.washingtonpost.com",
                "country": "United States"
            },
            "reuters": {
                "name": "Reuters",
                "website_url": "https://www.reuters.com",
                "country": "International"
            },
            "associated-press": {
                "name": "Associated Press",
                "website_url": "https://apnews.com",
                "country": "United States"
            }
        }
        
        if self.use_mock:
            articles = self.get_mock_newsapi_data()
        else:
            # Make real API calls for each source
            articles = []
            for source_id in sources.keys():
                try:
                    response = requests.get(
                        api_endpoint,
                        params={
                            "apiKey": self.news_api_key,
                            "sources": source_id,
                            "pageSize": self.limit
                        },
                        timeout=10  # Set timeout for the request
                    )
                    
                    # Check response status
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("status") == "ok":
                            articles.extend(data.get("articles", []))
                        else:
                            self.stdout.write(self.style.WARNING(f"NewsAPI returned error: {data.get('message', 'Unknown error')}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"NewsAPI returned status code {response.status_code}"))
                
                except requests.RequestException as e:
                    self.stdout.write(self.style.ERROR(f"Request failed for source {source_id}: {str(e)}"))
        
        # Process and save articles
        count = 0
        for article in articles:
            try:
                # Skip articles without title or content
                if not article.get("title") or not (article.get("content") or article.get("description")):
                    continue
                
                # Get or create source
                source_id = article.get("source", {}).get("id", "unknown")
                source_name = article.get("source", {}).get("name", "Unknown Source")
                
                source_data = sources.get(source_id, {
                    "name": source_name,
                    "website_url": f"https://{source_name.lower().replace(' ', '')}.com",
                    "country": "Unknown"
                })
                
                source, created = Source.objects.get_or_create(
                    name=source_data["name"],
                    defaults={
                        "website_url": source_data["website_url"],
                        "country": source_data["country"]
                    }
                )
                
                if created:
                    self.stdout.write(f"Created source: {source.name}")
                
                # Parse date
                published_at = timezone.now()
                if article.get("publishedAt"):
                    try:
                        published_at = datetime.strptime(
                            article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
                        )
                        published_at = published_at.replace(tzinfo=pytz.UTC)
                    except ValueError:
                        pass
                
                # Get or create article
                news, created = News.objects.get_or_create(
                    title=article.get("title", "Untitled"),
                    defaults={
                        "content": self.clean_content(article.get("content") or article.get("description", "No content available")),
                        "author": article.get("author", "Unknown"),
                        "image_url": article.get("urlToImage", ""),
                        "published_at": published_at,
                        "source": source,
                        "is_read": False,
                        "url": article.get("url", "")
                    }
                )
                
                if created:
                    count += 1
                    self.stdout.write(f"Created news article: {news.title}")
                    
                    # Categorize news based on content keywords
                    self.categorize_news(news)
            
            except Exception as e:
                logger.error(f"Error processing article: {str(e)}")
                self.stdout.write(self.style.ERROR(f"Error processing article: {str(e)}"))
        
        self.stdout.write(f"Added {count} new articles from NewsAPI")
    
    def fetch_from_gnews(self):
        """Fetch news from GNews API and save to database"""
        self.stdout.write("Fetching from GNews...")
        
        api_endpoint = "https://gnews.io/api/v4/top-headlines"
        
        if self.use_mock:
            articles = self.get_mock_gnews_data()
        else:
            # Make real API call to GNews
            try:
                response = requests.get(
                    api_endpoint,
                    params={
                        "token": self.gnews_api_key,
                        "lang": "en",
                        "max": self.limit
                    },
                    timeout=10  # Set timeout for the request
                )
                
                # Check response status
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get("articles", [])
                else:
                    self.stdout.write(self.style.WARNING(f"GNews API returned status code {response.status_code}"))
                    articles = []
            
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Request failed for GNews: {str(e)}"))
                articles = []
        
        # Process and save articles
        count = 0
        for article in articles:
            try:
                # Skip articles without title or content
                if not article.get("title") or not (article.get("content") or article.get("description")):
                    continue
                
                # Get or create source
                source_data = article.get("source", {})
                source_name = source_data.get("name", "Unknown Source")
                source_url = source_data.get("url", f"https://{source_name.lower().replace(' ', '')}.com")
                
                source, created = Source.objects.get_or_create(
                    name=source_name,
                    defaults={
                        "website_url": source_url,
                        "country": "Unknown"  # GNews doesn't provide country info
                    }
                )
                
                if created:
                    self.stdout.write(f"Created source: {source.name}")
                
                # Parse date
                published_at = timezone.now()
                if article.get("publishedAt"):
                    try:
                        published_at = datetime.strptime(
                            article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
                        )
                        published_at = published_at.replace(tzinfo=pytz.UTC)
                    except ValueError:
                        pass
                
                # Get or create article - use URL to avoid duplicates with NewsAPI
                news, created = News.objects.get_or_create(
                    url=article.get("url", ""),
                    defaults={
                        "title": article.get("title", "Untitled"),
                        "content": self.clean_content(article.get("content") or article.get("description", "No content available")),
                        "author": "GNews",  # GNews API doesn't provide author
                        "image_url": article.get("image", ""),
                        "published_at": published_at,
                        "source": source,
                        "is_read": False
                    }
                )
                
                if created:
                    count += 1
                    self.stdout.write(f"Created news article: {news.title}")
                    
                    # Categorize news based on content keywords
                    self.categorize_news(news)
            
            except Exception as e:
                logger.error(f"Error processing article: {str(e)}")
                self.stdout.write(self.style.ERROR(f"Error processing article: {str(e)}"))
        
        self.stdout.write(f"Added {count} new articles from GNews")
    
    def categorize_news(self, news):
        """Automatically categorize news based on content keywords"""
        # Define category keywords
        category_keywords = {
            "Politics": ["government", "election", "political", "policy", "president", "vote", "democracy", "parliament"],
            "Technology": ["tech", "technology", "digital", "computer", "software", "hardware", "AI", "artificial intelligence", "app"],
            "Business": ["business", "economy", "market", "stock", "company", "economic", "finance", "trade", "investor"],
            "Science": ["science", "scientific", "research", "study", "discovery", "researcher", "laboratory", "experiment"],
            "Health": ["health", "medical", "doctor", "patient", "disease", "treatment", "hospital", "medicine", "vaccine"],
            "Entertainment": ["entertainment", "movie", "film", "actor", "actress", "celebrity", "star", "music", "concert"],
            "Sports": ["sport", "team", "player", "game", "match", "tournament", "championship", "athlete", "coach"],
            "World": ["world", "international", "global", "foreign", "country", "nation", "worldwide"],
            "Environment": ["environment", "climate", "pollution", "environmental", "renewable", "sustainable", "ecology", "green"],
            "Education": ["education", "school", "university", "student", "teacher", "academic", "learning", "college", "classroom"]
        }
        
        # Combine title and content for searching
        search_text = f"{news.title} {news.content}".lower()
        
        # Check each category
        found_category = False
        for category_name, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword.lower() in search_text:
                    # Category matches, add it
                    category, created = Category.objects.get_or_create(name=category_name)
                    NewsCategory.objects.get_or_create(news=news, category=category)
                    self.stdout.write(f"  - Added to category: {category_name}")
                    found_category = True
                    break  # No need to check other keywords for this category
        
        # If no categories were found, add to "Uncategorized"
        if not found_category:
            category, created = Category.objects.get_or_create(name="Uncategorized")
            NewsCategory.objects.get_or_create(news=news, category=category)
            self.stdout.write(f"  - Added to category: Uncategorized")
    
    def cleanup_old_news(self):
        """Remove old news articles to keep the database size manageable"""
        # Remove news older than 30 days
        threshold_date = timezone.now() - timezone.timedelta(days=30)
        old_news = News.objects.filter(published_at__lt=threshold_date)
        count = old_news.count()
        
        if count > 0:
            old_news.delete()
            self.stdout.write(f"Removed {count} old news articles")
    
    def get_mock_newsapi_data(self):
        """Return mock data in NewsAPI format for prototype"""
        return [
            {
                "source": {"id": "bbc-news", "name": "BBC News"},
                "author": "BBC News",
                "title": "Climate Change Report: Countries Must Cut Emissions Faster",
                "description": "A new UN climate report warns countries must speed up efforts to reduce carbon emissions.",
                "url": "https://www.bbc.co.uk/news/world-58073318",
                "urlToImage": "https://ichef.bbci.co.uk/news/1024/branded_news/83B3/production/_120301100_gettyimages-1325888288.jpg",
                "publishedAt": "2023-05-01T12:30:45Z",
                "content": "Countries must accelerate their emissions cuts to avoid catastrophic climate change, according to a new UN report released today. The study found the world is on track for 2.7C of warming this century, far above the 1.5C target."
            },
            {
                "source": {"id": "cnn", "name": "CNN"},
                "author": "Jane Smith",
                "title": "Tech Giants Announce AI Ethics Coalition",
                "description": "Major tech companies form alliance to address ethical concerns in artificial intelligence development.",
                "url": "https://www.cnn.com/2023/05/02/tech/ai-ethics-coalition/index.html",
                "urlToImage": "https://cdn.cnn.com/cnnnext/dam/assets/230502104530-ai-ethics-meeting-super-tease.jpg",
                "publishedAt": "2023-05-02T10:45:30Z",
                "content": "Leading technology companies have announced a new coalition focused on ethical AI development. The group aims to create industry standards for responsible AI, addressing concerns about bias, privacy, and safety."
            },
            {
                "source": {"id": "the-washington-post", "name": "The Washington Post"},
                "author": "Michael Johnson",
                "title": "New Breakthrough in Quantum Computing",
                "description": "Scientists achieve quantum advantage with new 100-qubit processor.",
                "url": "https://www.washingtonpost.com/technology/2023/05/01/quantum-computing-breakthrough/",
                "urlToImage": "https://www.washingtonpost.com/wp-apps/imrs.php?src=https://arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/5YZKTIVCAEI6XMLXVUP7CMNWSY.jpg",
                "publishedAt": "2023-05-01T15:20:10Z",
                "content": "Researchers have announced a major breakthrough in quantum computing with a new 100-qubit processor that demonstrates quantum advantage. The system solved complex calculations in minutes that would take conventional supercomputers thousands of years."
            },
            {
                "source": {"id": "bbc-news", "name": "BBC News"},
                "author": "BBC Health",
                "title": "New Treatment Shows Promise for Alzheimer's Disease",
                "description": "Clinical trials of a new drug show significant slowing of cognitive decline in patients.",
                "url": "https://www.bbc.co.uk/news/health-58072145",
                "urlToImage": "https://ichef.bbci.co.uk/news/1024/branded_news/6759/production/_120300145_brain_scan.jpg",
                "publishedAt": "2023-05-03T09:15:30Z",
                "content": "A new treatment for Alzheimer's disease has shown promising results in clinical trials, researchers report. The drug, which targets amyloid protein buildup in the brain, slowed cognitive decline by 27% in patients with early-stage disease."
            },
            {
                "source": {"id": "reuters", "name": "Reuters"},
                "author": "Sarah Thompson",
                "title": "Global Stock Markets Hit New Highs on Economic Recovery Hopes",
                "description": "Global shares reach record levels as recovery gains momentum.",
                "url": "https://www.reuters.com/business/global-markets-stocks-2023-05-04/",
                "urlToImage": "https://www.reuters.com/resizer/example-image.jpg",
                "publishedAt": "2023-05-04T08:25:15Z",
                "content": "Global stock markets hit record highs on Thursday as investors grew increasingly confident about the strength of the economic recovery. Positive manufacturing data and strong corporate earnings have fueled optimism about global growth prospects."
            },
            {
                "source": {"id": "associated-press", "name": "Associated Press"},
                "author": "James Wilson",
                "title": "Scientists Discover New Species in Amazon Rainforest",
                "description": "Researchers identify dozens of previously unknown plant and animal species.",
                "url": "https://apnews.com/article/amazon-rainforest-new-species-discovery-science",
                "urlToImage": "https://storage.googleapis.com/afs-prod/media/example-image/1000.jpeg",
                "publishedAt": "2023-05-03T14:10:05Z",
                "content": "Scientists on a recent expedition to the Amazon rainforest have discovered over 50 species previously unknown to science, including 10 new types of orchids and several amphibian species. The findings highlight the incredible biodiversity of this threatened ecosystem."
            }
        ]
    
    def get_mock_gnews_data(self):
        """Return mock data in GNews API format for prototype"""
        return [
            {
                "title": "Global Economic Forum Announces Recovery Plan",
                "description": "The Global Economic Forum has released a comprehensive plan to boost post-pandemic recovery.",
                "content": "The Global Economic Forum today unveiled a comprehensive plan aimed at accelerating economic recovery worldwide. The initiative includes recommendations for infrastructure investment, digital transformation, and workforce development. 'This framework provides a roadmap for sustainable and inclusive growth,' said the Forum's president at today's announcement.",
                "url": "https://www.econews.com/global-forum-recovery-plan",
                "image": "https://www.econews.com/images/recovery-plan.jpg",
                "publishedAt": "2023-05-02T14:25:10Z",
                "source": {
                    "name": "Economic News",
                    "url": "https://www.econews.com"
                }
            },
            {
                "title": "Major Medical Breakthrough in Cancer Treatment",
                "description": "Scientists announce promising results from trials of new immunotherapy approach.",
                "content": "Medical researchers have reported a significant breakthrough in cancer treatment using a novel immunotherapy approach. The technique, which enhances the body's natural immune response to cancer cells, showed an 85% response rate in patients with advanced forms of the disease. Clinical trials are now moving to the next phase with expanded patient groups.",
                "url": "https://www.healthnews.org/cancer-breakthrough",
                "image": "https://www.healthnews.org/images/cancer-research.jpg",
                "publishedAt": "2023-05-03T11:40:15Z",
                "source": {
                    "name": "Health News",
                    "url": "https://www.healthnews.org"
                }
            },
            {
                "title": "New Educational App Helps Students Master Mathematics",
                "description": "Innovative application uses AI to personalize math learning for K-12 students.",
                "content": "A new educational application is transforming how students learn mathematics. The app uses artificial intelligence to identify each student's strengths and weaknesses, creating personalized learning paths. Early testing in schools shows significant improvement in math scores after just three months of use. The app is now available free of charge to public schools nationwide.",
                "url": "https://www.edtech.com/math-app-launch",
                "image": "https://www.edtech.com/images/math-app.jpg",
                "publishedAt": "2023-05-01T16:35:20Z",
                "source": {
                    "name": "EdTech Today",
                    "url": "https://www.edtech.com"
                }
            },
            {
                "title": "Record-Breaking Summer Temperatures Expected Worldwide",
                "description": "Climate scientists predict hottest summer on record for many regions.",
                "content": "Climate researchers are warning that this summer could break temperature records across multiple continents. Using advanced climate models, scientists project that regions in North America, Europe, and Asia will experience temperatures 2-4°C above historical averages. 'These projections are consistent with accelerating climate change patterns we've observed over the past decade,' explained Dr. Sarah Reynolds, lead climatologist at the Global Climate Institute.",
                "url": "https://www.climatereport.org/summer-forecast",
                "image": "https://www.climatereport.org/images/heatwave.jpg",
                "publishedAt": "2023-05-04T08:50:40Z",
                "source": {
                    "name": "Climate Report",
                    "url": "https://www.climatereport.org"
                }
            },
            {
                "title": "Space Tourism Company Announces First Commercial Flight",
                "description": "Private space company schedules inaugural tourist mission to orbit.",
                "content": "A leading space tourism company has announced that its first commercial flight to orbit will launch next month. The mission will carry six civilians on a three-day journey around Earth, reaching altitudes of up to 500 kilometers. Tickets for the historic flight reportedly sold for $28 million each, with the company already having a waitlist for future missions.",
                "url": "https://www.spacetoday.com/first-tourist-flight",
                "image": "https://www.spacetoday.com/images/space-capsule.jpg",
                "publishedAt": "2023-05-04T12:15:30Z",
                "source": {
                    "name": "Space Today",
                    "url": "https://www.spacetoday.com"
                }
            },
            {
                "title": "New Renewable Energy Project Will Power Millions of Homes",
                "description": "Construction begins on massive offshore wind farm that will be world's largest.",
                "content": "Construction has started on what will become the world's largest offshore wind farm, capable of providing clean energy to over 4.5 million homes. The project, located 75 kilometers from shore, will feature 300 turbines and is expected to be operational by 2025. Government officials called it a 'landmark achievement' in the transition to renewable energy sources.",
                "url": "https://www.energynews.net/mega-wind-project",
                "image": "https://www.energynews.net/images/wind-farm.jpg",
                "publishedAt": "2023-05-02T09:20:15Z",
                "source": {
                    "name": "Energy News Network",
                    "url": "https://www.energynews.net"
                }
            }
        ] 

    def clean_content(self, content):
        """Remove the truncation marker from content if present."""
        import re
        # Remove [+1234 chars] pattern from the end of content
        return re.sub(r'\s*\[\+\d+ chars\]$', '', content) 