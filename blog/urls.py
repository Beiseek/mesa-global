from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),
    
    # Статические страницы
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Рецепты
    path('recipes/', views.recipes, name='recipes'),
    path('recipe/<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    
    # Статьи
    path('stories/', views.articles, name='articles'),
    path('story/<slug:slug>/', views.article_detail, name='article_detail'),
    
    # Регионы
    path('region/<slug:slug>/', views.region_detail, name='region_detail'),
    
    # Поиск
    path('search/', views.search, name='search'),
]
