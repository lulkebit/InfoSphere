import re
from django.core.management.base import BaseCommand
from newsapp.models import News

class Command(BaseCommand):
    help = 'Cleans existing news content by removing [+X chars] markers'

    def handle(self, *args, **options):
        self.stdout.write('Cleaning news content...')
        
        # Get all news articles
        news_articles = News.objects.all()
        
        # Counter for modified articles
        modified_count = 0
        
        for news in news_articles:
            original_content = news.content
            cleaned_content = self.clean_content(original_content)
            
            # Only update if content was changed
            if original_content != cleaned_content:
                news.content = cleaned_content
                news.save()
                modified_count += 1
                self.stdout.write(f'Cleaned content for: {news.title}')
        
        self.stdout.write(self.style.SUCCESS(f'Content cleaned for {modified_count} news articles'))
    
    def clean_content(self, content):
        """Remove the truncation marker from content if present."""
        # Remove [+1234 chars] pattern from the end of content
        return re.sub(r'\s*\[\+\d+ chars\]$', '', content) 