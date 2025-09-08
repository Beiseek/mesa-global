from django.contrib import admin
from .models import Region, Category, Tag, Recipe, Article, ContactSubmission


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'region', 'category', 'difficulty', 'is_published', 'created_at')
    list_filter = ('region', 'category', 'difficulty', 'is_published', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'region', 'category', 'tags', 'description')
        }),
        ('Содержание', {
            'fields': ('history', 'cultural_context', 'ingredients', 'instructions')
        }),
        ('Параметры рецепта', {
            'fields': ('prep_time', 'cook_time', 'servings', 'difficulty')
        }),
        ('Изображения', {
            'fields': ('featured_image', 'gallery_image_1', 'gallery_image_2', 'gallery_image_3')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Публикация', {
            'fields': ('is_published',)
        }),
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'article_type', 'region', 'is_published', 'featured', 'created_at')
    list_filter = ('article_type', 'region', 'is_published', 'featured', 'created_at')
    search_fields = ('title', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'article_type', 'region', 'tags', 'excerpt')
        }),
        ('Содержание', {
            'fields': ('content',)
        }),
        ('Автор (для интервью)', {
            'fields': ('author_name', 'author_bio'),
            'classes': ('collapse',)
        }),
        ('Изображения', {
            'fields': ('featured_image', 'gallery_image_1', 'gallery_image_2')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Публикация', {
            'fields': ('is_published', 'featured')
        }),
    )


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'submission_type', 'region', 'created_at', 'processed')
    list_filter = ('submission_type', 'processed', 'created_at')
    search_fields = ('name', 'title', 'email')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Контактная информация', {
            'fields': ('name', 'email')
        }),
        ('Заявка', {
            'fields': ('submission_type', 'title', 'description', 'region', 'content')
        }),
        ('Статус', {
            'fields': ('processed', 'created_at')
        }),
    )
    
    actions = ['mark_as_processed']
    
    def mark_as_processed(self, request, queryset):
        queryset.update(processed=True)
    mark_as_processed.short_description = "Отметить как обработанные"


# Настройка админ-панели
admin.site.site_header = "Mesa Global - Панель управления"
admin.site.site_title = "Mesa Global Admin"
admin.site.index_title = "Добро пожаловать в панель управления Mesa Global"
