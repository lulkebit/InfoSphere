from django.core.management.base import BaseCommand
from messages_api.services import NewsService

class Command(BaseCommand):
    help = 'Fetches latest news articles from NewsAPI'

    def handle(self, *args, **options):
        self.stdout.write('Fetching news articles...')
        news_service = NewsService()
        news_service.update_news()
        self.stdout.write(self.style.SUCCESS('Successfully updated news articles')) 