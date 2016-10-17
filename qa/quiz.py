"""View for exam."""
from braces.views import LoginRequiredMixin

from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Article, Question


class QuizView(LoginRequiredMixin, TemplateView):
    """View for quiz page."""

    template_name = 'quiz.html'

    def get(self, request, article_id, *args, **kwargs):
        """Method for get request of quiz page."""
        try:
            article = Article.objects.get(
                id=article_id,
            )
        except Article.DoesNotExist:
            raise Http404
        context = {'article': article}
        context['questions'] = Question.objects.filter(article=article)
        return render(request, self.template_name, context)
