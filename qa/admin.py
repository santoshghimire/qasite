from django.contrib import admin

# Register your models here.
from .models import (
    Category, Article, Question, Option,
    QuestionAttempt, Level, Grade, QuestionAttemptPoint,
    Quiz, QuizResult
)

admin.site.register(Option)
admin.site.register(QuestionAttempt)
admin.site.register(QuestionAttemptPoint)
admin.site.register(Level)
admin.site.register(Grade)
admin.site.register(Quiz)
admin.site.register(QuizResult)


@admin.register(Category)
class CertificateAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'level', 'slug', 'created', 'active'
    )
    search_fields = [
        'title', 'slug', 'level__name'
    ]
    list_editable = ('active', )


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
