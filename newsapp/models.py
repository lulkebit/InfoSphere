from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Source(models.Model):
    name = models.CharField(max_length=100)
    website_url = models.URLField()
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    published_at = models.DateTimeField()
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    url = models.URLField()
    categories = models.ManyToManyField(Category, through='NewsCategory')
    users = models.ManyToManyField(User, through='UserNews')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "News"

class NewsCategory(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('news', 'category')
        verbose_name_plural = "News Categories"

class UserNews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'news')
        verbose_name_plural = "User News"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.news.title}"

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'news')
    
    def __str__(self):
        return f"Bookmark by {self.user.username} for {self.news.title}"

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_sources = models.ManyToManyField(Source, blank=True)
    preferred_categories = models.ManyToManyField(Category, blank=True)
    dark_mode = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Preferences for {self.user.username}"
