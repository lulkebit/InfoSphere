from django.contrib import admin
from .models import (
    Category, Source, News, NewsCategory, UserNews,
    Comment, Bookmark, UserPreference
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url', 'country')
    search_fields = ('name', 'country')
    list_filter = ('country',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'source', 'published_at', 'is_read')
    search_fields = ('title', 'content', 'author')
    list_filter = ('source', 'published_at', 'is_read')
    date_hierarchy = 'published_at'

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('news', 'category')
    list_filter = ('category',)

@admin.register(UserNews)
class UserNewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'news')
    list_filter = ('user',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'created_at')
    search_fields = ('content',)
    list_filter = ('user', 'created_at')
    date_hierarchy = 'created_at'

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'saved_at')
    list_filter = ('user', 'saved_at')
    date_hierarchy = 'saved_at'

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'dark_mode')
    list_filter = ('dark_mode', 'preferred_categories', 'preferred_sources')
