from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Article


class ArticleListView(LoginRequiredMixin, ListView):
    """ View to list all articles."""

    model = Article
    template_name = 'home.html'

    def get_queryset(self):
        queryset = Article.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            ArticleListView, self).get_context_data(**kwargs)
        return context
