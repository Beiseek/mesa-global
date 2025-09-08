from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from meta.models import ModelMeta


class Region(models.Model):
    """Модель для регионов/стран"""
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='regions/', blank=True, verbose_name="Изображение")
    
    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    """Модель для категорий блюд"""
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Модель для тегов"""
    name = models.CharField(max_length=50, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Recipe(ModelMeta, models.Model):
    """Модель для рецептов"""
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Регион")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")
    
    # Основная информация
    description = models.TextField(verbose_name="Краткое описание")
    history = RichTextUploadingField(verbose_name="История блюда")
    cultural_context = RichTextUploadingField(verbose_name="Культурный контекст")
    
    # Рецепт
    ingredients = RichTextUploadingField(verbose_name="Ингредиенты")
    instructions = RichTextUploadingField(verbose_name="Пошаговый рецепт")
    prep_time = models.PositiveIntegerField(verbose_name="Время подготовки (мин)")
    cook_time = models.PositiveIntegerField(verbose_name="Время готовки (мин)")
    servings = models.PositiveIntegerField(verbose_name="Количество порций")
    difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ], default='medium', verbose_name="Сложность")
    
    # Изображения
    featured_image = models.ImageField(upload_to='recipes/', verbose_name="Главное изображение")
    gallery_image_1 = models.ImageField(upload_to='recipes/', blank=True, verbose_name="Доп. изображение 1")
    gallery_image_2 = models.ImageField(upload_to='recipes/', blank=True, verbose_name="Доп. изображение 2")
    gallery_image_3 = models.ImageField(upload_to='recipes/', blank=True, verbose_name="Доп. изображение 3")
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True, verbose_name="SEO заголовок")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="SEO описание")
    
    # Даты
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    
    _metadata = {
        'title': 'get_meta_title',
        'description': 'get_meta_description',
        'keywords': 'get_meta_keywords',
        'image': 'get_meta_image',
    }
    
    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title[:60]
        if not self.meta_description:
            self.meta_description = self.description[:160]
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'slug': self.slug})
    
    def get_meta_title(self):
        return self.meta_title or self.title
    
    def get_meta_description(self):
        return self.meta_description or self.description
    
    def get_meta_keywords(self):
        keywords = [self.title, self.region.name, self.category.name]
        keywords.extend([tag.name for tag in self.tags.all()])
        return keywords
    
    def get_meta_image(self):
        return self.featured_image.url if self.featured_image else None
    
    def total_time(self):
        return self.prep_time + self.cook_time


class Article(ModelMeta, models.Model):
    """Модель для статей и историй"""
    ARTICLE_TYPES = [
        ('story', 'Story'),
        ('interview', 'Interview'),
        ('blog', 'Blog'),
        ('culture', 'Culture'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    article_type = models.CharField(max_length=20, choices=ARTICLE_TYPES, verbose_name="Тип статьи")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Регион")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")
    
    # Контент
    excerpt = models.TextField(verbose_name="Краткое описание")
    content = RichTextUploadingField(verbose_name="Содержание")
    
    # Изображения
    featured_image = models.ImageField(upload_to='articles/', verbose_name="Главное изображение")
    gallery_image_1 = models.ImageField(upload_to='articles/', blank=True, verbose_name="Доп. изображение 1")
    gallery_image_2 = models.ImageField(upload_to='articles/', blank=True, verbose_name="Доп. изображение 2")
    
    # Автор (для интервью)
    author_name = models.CharField(max_length=100, blank=True, verbose_name="Имя автора/интервьюируемого")
    author_bio = models.TextField(blank=True, verbose_name="Биография автора")
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True, verbose_name="SEO заголовок")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="SEO описание")
    
    # Даты
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    featured = models.BooleanField(default=False, verbose_name="Рекомендуемая")
    
    _metadata = {
        'title': 'get_meta_title',
        'description': 'get_meta_description',
        'keywords': 'get_meta_keywords',
        'image': 'get_meta_image',
    }
    
    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title[:60]
        if not self.meta_description:
            self.meta_description = self.excerpt[:160]
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})
    
    def get_meta_title(self):
        return self.meta_title or self.title
    
    def get_meta_description(self):
        return self.meta_description or self.excerpt
    
    def get_meta_keywords(self):
        keywords = [self.title, self.article_type]
        if self.region:
            keywords.append(self.region.name)
        keywords.extend([tag.name for tag in self.tags.all()])
        return keywords
    
    def get_meta_image(self):
        return self.featured_image.url if self.featured_image else None


class ContactSubmission(models.Model):
    """Модель для заявок на публикацию рецептов/историй"""
    SUBMISSION_TYPES = [
        ('recipe', 'Recipe'),
        ('story', 'Story'),
    ]
    
    submission_type = models.CharField(max_length=20, choices=SUBMISSION_TYPES, verbose_name="Тип заявки")
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    region = models.CharField(max_length=100, verbose_name="Страна/Регион")
    content = models.TextField(verbose_name="Содержание")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Получено")
    processed = models.BooleanField(default=False, verbose_name="Обработано")
    
    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.title}"
