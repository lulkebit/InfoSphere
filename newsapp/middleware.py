import time
import threading
import logging
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.management import call_command

logger = logging.getLogger(__name__)

class NewsRefreshThread(threading.Thread):
    """Thread to periodically refresh news data"""
    
    def __init__(self, interval=3600):  # Default: refresh every hour
        super().__init__(daemon=True)  # Run as daemon thread
        self.interval = interval
        self.last_refresh = None
        self.stop_event = threading.Event()
    
    def run(self):
        """Run the thread, fetching news at specified intervals"""
        while not self.stop_event.is_set():
            now = timezone.now()
            
            # Check if it's time to refresh
            if self.last_refresh is None or (now - self.last_refresh).total_seconds() >= self.interval:
                try:
                    logger.info("Starting scheduled news refresh...")
                    call_command('fetch_news', mock=True)  # Use mock=True for development
                    self.last_refresh = now
                    logger.info(f"Scheduled news refresh completed at {now.strftime('%Y-%m-%d %H:%M:%S')}")
                except Exception as e:
                    logger.error(f"Error during scheduled news refresh: {str(e)}")
            
            # Sleep for 60 seconds before checking again
            self.stop_event.wait(60)
    
    def stop(self):
        """Stop the thread"""
        self.stop_event.set()


class NewsRefreshMiddleware:
    """Middleware to start the news refresh thread"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.refresh_thread = None
    
    def __call__(self, request):
        # Start the refresh thread if it's not running
        if self.refresh_thread is None or not self.refresh_thread.is_alive():
            self.refresh_thread = NewsRefreshThread()
            self.refresh_thread.start()
            logger.info("News refresh thread started")
        
        response = self.get_response(request)
        return response 