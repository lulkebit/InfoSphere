from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from .models import News, Category, Source, Comment, Bookmark
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.management import call_command
from django.contrib.auth.models import User
from django.contrib.auth import login

def home(request):
    """Home page view displaying latest news."""
    # Check if refresh_news parameter is present and user is staff
    if request.GET.get('refresh_news') and request.user.is_staff:
        try:
            # Call the fetch_news command
            call_command('fetch_news')
            messages.success(request, 'News successfully fetched from APIs!')
        except Exception as e:
            messages.error(request, f'Error fetching news: {str(e)}')
    
    news_list = News.objects.select_related('source').prefetch_related('categories').order_by('-published_at')
    categories = Category.objects.all()
    
    # Filter by category if specified
    category_id = request.GET.get('category')
    if category_id:
        news_list = news_list.filter(categories__id=category_id)
    
    # Filter by source if specified
    source_id = request.GET.get('source')
    if source_id:
        news_list = news_list.filter(source_id=source_id)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        news_list = news_list.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(author__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    news_items = paginator.get_page(page_number)
    
    sources = Source.objects.all()
    
    context = {
        'news_items': news_items,
        'categories': categories,
        'sources': sources,
        'selected_category': category_id,
        'selected_source': source_id,
        'query': query,
    }
    return render(request, 'newsapp/home.html', context)

def news_detail(request, news_id):
    """View for displaying a single news article and its comments."""
    news = get_object_or_404(News, id=news_id)
    comments = Comment.objects.filter(news=news).select_related('user').order_by('-created_at')
    
    # Mark as read
    if request.user.is_authenticated:
        news.is_read = True
        news.save()
        
        # Check if bookmarked
        is_bookmarked = Bookmark.objects.filter(user=request.user, news=news).exists()
    else:
        is_bookmarked = False
    
    context = {
        'news': news,
        'comments': comments,
        'is_bookmarked': is_bookmarked,
    }
    return render(request, 'newsapp/news_detail.html', context)

@login_required
def add_comment(request, news_id):
    """Add a comment to a news article."""
    news = get_object_or_404(News, id=news_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                user=request.user,
                news=news,
                content=content,
                created_at=timezone.now()
            )
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Comment cannot be empty!')
    
    return redirect('news_detail', news_id=news_id)

@login_required
def toggle_bookmark(request, news_id):
    """Toggle bookmark status for a news article."""
    news = get_object_or_404(News, id=news_id)
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        news=news,
        defaults={'saved_at': timezone.now()}
    )
    
    if not created:
        bookmark.delete()
        messages.success(request, 'Bookmark removed')
    else:
        messages.success(request, 'News bookmarked')
    
    return redirect('news_detail', news_id=news_id)

@login_required
def bookmarks(request):
    """Display user's bookmarked news articles."""
    bookmarked_news = News.objects.filter(
        bookmark__user=request.user
    ).select_related('source').prefetch_related('categories').order_by('-bookmark__saved_at')
    
    context = {
        'bookmarked_news': bookmarked_news,
    }
    return render(request, 'newsapp/bookmarks.html', context)

@login_required
def user_preferences(request):
    """View and update user preferences."""
    from .models import UserPreference
    
    preference, created = UserPreference.objects.get_or_create(user=request.user)
    categories = Category.objects.all()
    sources = Source.objects.all()
    
    if request.method == 'POST':
        dark_mode = request.POST.get('dark_mode') == 'on'
        preferred_categories = request.POST.getlist('preferred_categories')
        preferred_sources = request.POST.getlist('preferred_sources')
        
        preference.dark_mode = dark_mode
        preference.save()
        
        preference.preferred_categories.clear()
        for category_id in preferred_categories:
            preference.preferred_categories.add(category_id)
        
        preference.preferred_sources.clear()
        for source_id in preferred_sources:
            preference.preferred_sources.add(source_id)
        
        messages.success(request, 'Preferences updated successfully!')
    
    context = {
        'preference': preference,
        'categories': categories,
        'sources': sources,
    }
    return render(request, 'newsapp/preferences.html', context)

def categories(request):
    """View all categories and their news counts."""
    categories = Category.objects.annotate(news_count=Count('news')).order_by('name')
    
    context = {
        'categories': categories,
    }
    return render(request, 'newsapp/categories.html', context)

def sources(request):
    """View all news sources."""
    sources = Source.objects.annotate(news_count=Count('news')).order_by('name')
    
    context = {
        'sources': sources,
    }
    return render(request, 'newsapp/sources.html', context)

def register(request):
    """Register a new user."""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validate form data
        if not all([username, email, password, password_confirm]):
            messages.error(request, 'All fields are required.')
            return render(request, 'newsapp/register.html')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'newsapp/register.html')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'newsapp/register.html')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'newsapp/register.html')
        
        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Log the user in
        login(request, user)
        messages.success(request, f'Account created successfully! Welcome, {username}!')
        return redirect('home')
    
    return render(request, 'newsapp/register.html')
