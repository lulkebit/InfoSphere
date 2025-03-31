from django.core.management.base import BaseCommand
from newsapp.models import News
import os

class Command(BaseCommand):
    help = 'Checks the length of content in news articles to identify potential truncation issues'

    def handle(self, *args, **options):
        self.stdout.write('Checking news content length...')
        
        # Create a log file
        log_file_path = 'content_analysis.txt'
        
        with open(log_file_path, 'w') as log_file:
            # Get all news articles
            news_articles = News.objects.all()
            
            # Counters for statistics
            total = news_articles.count()
            short_content_count = 0
            long_content_count = 0
            
            # Define thresholds (characters)
            short_threshold = 200  # Less than this is considered short
            
            # Sample display
            log_file.write("Sample content lengths:\n")
            for i, news in enumerate(news_articles[:10]):  # Show first 10 articles
                content_length = len(news.content)
                log_file.write(f"{i+1}. {news.title} ({content_length} chars)\n")
                if content_length < 100:  # Show very short content for inspection
                    log_file.write(f"   Content: {news.content}\n")
            
            # Count statistics
            for news in news_articles:
                content_length = len(news.content)
                if content_length < short_threshold:
                    short_content_count += 1
                else:
                    long_content_count += 1
            
            # Display statistics
            log_file.write("\nContent Length Statistics:\n")
            log_file.write(f"Total articles: {total}\n")
            log_file.write(f"Articles with short content (<{short_threshold} chars): {short_content_count} ({short_content_count/total*100:.1f}%)\n")
            log_file.write(f"Articles with longer content: {long_content_count} ({long_content_count/total*100:.1f}%)\n")
            
            # Display API source article content
            log_file.write("\nFull content of external API articles (up to 5):\n")
            api_articles = news_articles.filter(source__name__in=["GNews", "BBC News", "CNN", "Reuters"])[:5]
            for i, article in enumerate(api_articles):
                log_file.write(f"\n{i+1}. {article.title} (Source: {article.source.name})\n")
                log_file.write(f"Length: {len(article.content)} chars\n")
                log_file.write("Content:\n")
                log_file.write(f"{article.content}\n")
        
        self.stdout.write(f"Analysis complete. Results saved to {os.path.abspath(log_file_path)}") 