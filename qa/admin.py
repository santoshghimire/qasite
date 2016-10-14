from django.contrib import admin

# Register your models here.
from .models import (
    Category, Article, Question, Option
)

admin.site.register(Option)


@admin.register(Category)
class CertificateAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'grade', 'slug'
    )
    search_fields = [
        'title', 'slug', 'grade'
    ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'difficulty', 'category', 'article',
        'is_verified'
    )
    search_fields = [
        'text'
    ]
    list_filter = ('difficulty', 'category', 'article', 'is_verified')
