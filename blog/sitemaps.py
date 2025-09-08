from django.contrib.sitemaps import Sitemap
from .models import Article, Recipe


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    
    def items(self):
        return Article.objects.filter(is_published=True)
    
    def lastmod(self, obj):
        return obj.updated_at


class RecipeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    
    def items(self):
        return Recipe.objects.filter(is_published=True)
    
    def lastmod(self, obj):
        return obj.updated_at
