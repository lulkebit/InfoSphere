from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('news/<int:news_id>/comment/', views.add_comment, name='add_comment'),
    path('news/<int:news_id>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('preferences/', views.user_preferences, name='preferences'),
    path('categories/', views.categories, name='categories'),
    path('sources/', views.sources, name='sources'),
] 