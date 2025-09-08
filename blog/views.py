from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from meta.views import Meta
from .models import Article, Recipe, Region, Category, Tag, ContactSubmission
from .forms import ContactSubmissionForm


def home(request):
    """Главная страница"""
    # Последние статьи и рецепты
    featured_articles = Article.objects.filter(is_published=True, featured=True)[:3]
    latest_recipes = Recipe.objects.filter(is_published=True)[:6]
    latest_articles = Article.objects.filter(is_published=True)[:4]
    
    meta = Meta(
        title="Mesa Global - International Food & Culture Blog",
        description="Discover authentic recipes, cultural stories, and culinary traditions from around the world. Join our global community celebrating the diversity of international cuisine.",
        keywords=["international recipes", "cultural food", "global cuisine", "traditional recipes", "food culture"],
        image="/static/images/mesa-global-logo.jpg"
    )
    
    context = {
        'featured_articles': featured_articles,
        'latest_recipes': latest_recipes,
        'latest_articles': latest_articles,
        'meta': meta,
    }
    return render(request, 'blog/home.html', context)


def about(request):
    """О проекте"""
    meta = Meta(
        title="About Mesa Global - Our Mission & Story",
        description="Learn about Mesa Global's mission to celebrate diverse culinary traditions and connect people through food stories from around the world.",
        keywords=["about mesa global", "food culture mission", "culinary diversity"],
    )
    
    context = {'meta': meta}
    return render(request, 'blog/about.html', context)


def recipes(request):
    """Список рецептов с фильтрами"""
    recipes_list = Recipe.objects.filter(is_published=True)
    
    # Фильтры
    region_slug = request.GET.get('region')
    category_slug = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    search = request.GET.get('search')
    
    if region_slug:
        recipes_list = recipes_list.filter(region__slug=region_slug)
    if category_slug:
        recipes_list = recipes_list.filter(category__slug=category_slug)
    if difficulty:
        recipes_list = recipes_list.filter(difficulty=difficulty)
    if search:
        recipes_list = recipes_list.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search) |
            Q(ingredients__icontains=search)
        )
    
    # Пагинация
    paginator = Paginator(recipes_list, 12)
    page_number = request.GET.get('page')
    recipes_page = paginator.get_page(page_number)
    
    # Данные для фильтров
    regions = Region.objects.all()
    categories = Category.objects.all()
    difficulties = Recipe._meta.get_field('difficulty').choices
    
    meta = Meta(
        title="International Recipes from Around the World",
        description="Explore authentic recipes from different cultures and regions. Find traditional dishes, cooking techniques, and cultural stories behind every meal.",
        keywords=["international recipes", "traditional cooking", "global cuisine", "authentic recipes"],
    )
    
    context = {
        'recipes': recipes_page,
        'regions': regions,
        'categories': categories,
        'difficulties': difficulties,
        'current_region': region_slug,
        'current_category': category_slug,
        'current_difficulty': difficulty,
        'search_query': search,
        'meta': meta,
    }
    return render(request, 'blog/recipes.html', context)


def recipe_detail(request, slug):
    """Детальная страница рецепта"""
    recipe = get_object_or_404(Recipe, slug=slug, is_published=True)
    related_recipes = Recipe.objects.filter(
        region=recipe.region, is_published=True
    ).exclude(id=recipe.id)[:4]
    
    context = {
        'recipe': recipe,
        'related_recipes': related_recipes,
        'meta': recipe.as_meta(request),
    }
    return render(request, 'blog/recipe_detail.html', context)


def articles(request):
    """Список статей"""
    article_type = request.GET.get('type', 'all')
    search = request.GET.get('search')
    
    articles_list = Article.objects.filter(is_published=True)
    
    if article_type != 'all':
        articles_list = articles_list.filter(article_type=article_type)
    
    if search:
        articles_list = articles_list.filter(
            Q(title__icontains=search) | 
            Q(excerpt__icontains=search) |
            Q(content__icontains=search)
        )
    
    # Пагинация
    paginator = Paginator(articles_list, 10)
    page_number = request.GET.get('page')
    articles_page = paginator.get_page(page_number)
    
    article_types = Article.ARTICLE_TYPES
    
    meta = Meta(
        title="Cultural Stories & Food Articles",
        description="Read inspiring stories about food culture, interviews with chefs, and articles about culinary traditions from around the world.",
        keywords=["food stories", "culinary culture", "chef interviews", "food traditions"],
    )
    
    context = {
        'articles': articles_page,
        'article_types': article_types,
        'current_type': article_type,
        'search_query': search,
        'meta': meta,
    }
    return render(request, 'blog/articles.html', context)


def article_detail(request, slug):
    """Детальная страница статьи"""
    article = get_object_or_404(Article, slug=slug, is_published=True)
    related_articles = Article.objects.filter(
        article_type=article.article_type, is_published=True
    ).exclude(id=article.id)[:3]
    
    context = {
        'article': article,
        'related_articles': related_articles,
        'meta': article.as_meta(request),
    }
    return render(request, 'blog/article_detail.html', context)


def region_detail(request, slug):
    """Страница региона с рецептами и статьями"""
    region = get_object_or_404(Region, slug=slug)
    recipes = Recipe.objects.filter(region=region, is_published=True)[:8]
    articles = Article.objects.filter(region=region, is_published=True)[:4]
    
    meta = Meta(
        title=f"{region.name} - Recipes & Cultural Stories",
        description=f"Discover authentic recipes and cultural stories from {region.name}. Explore traditional cuisine and food heritage.",
        keywords=[region.name, "recipes", "traditional food", "culture"],
    )
    
    context = {
        'region': region,
        'recipes': recipes,
        'articles': articles,
        'meta': meta,
    }
    return render(request, 'blog/region_detail.html', context)


def contact(request):
    """Страница контактов и формы для отправки рецептов"""
    if request.method == 'POST':
        form = ContactSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save()
            
            # Отправка уведомления администратору
            try:
                send_mail(
                    f'Новая заявка: {submission.title}',
                    f'Получена новая заявка от {submission.name} ({submission.email})\n\n'
                    f'Тип: {submission.get_submission_type_display()}\n'
                    f'Название: {submission.title}\n'
                    f'Регион: {submission.region}\n\n'
                    f'Описание: {submission.description}',
                    settings.DEFAULT_FROM_EMAIL,
                    ['admin@mesaglobal.com'],
                    fail_silently=True,
                )
            except:
                pass
            
            messages.success(request, 'Спасибо за вашу заявку! Мы свяжемся с вами в ближайшее время.')
            return redirect('contact')
    else:
        form = ContactSubmissionForm()
    
    meta = Meta(
        title="Contact Mesa Global - Share Your Recipe or Story",
        description="Have a recipe or food story to share? Contact Mesa Global and become part of our global culinary community.",
        keywords=["contact", "submit recipe", "share food story", "culinary community"],
    )
    
    context = {
        'form': form,
        'meta': meta,
    }
    return render(request, 'blog/contact.html', context)


def search(request):
    """Поиск по сайту"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Поиск в рецептах
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(ingredients__icontains=query),
            is_published=True
        )
        
        # Поиск в статьях
        articles = Article.objects.filter(
            Q(title__icontains=query) | 
            Q(excerpt__icontains=query) |
            Q(content__icontains=query),
            is_published=True
        )
        
        results = list(recipes) + list(articles)
    
    meta = Meta(
        title=f"Search Results for '{query}'" if query else "Search Mesa Global",
        description="Search for recipes, articles, and cultural stories on Mesa Global.",
        keywords=["search", "recipes", "articles", "food culture"],
    )
    
    context = {
        'query': query,
        'results': results,
        'meta': meta,
    }
    return render(request, 'blog/search.html', context)
