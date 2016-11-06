from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from .models import Article, Level


class ArticleListView(LoginRequiredMixin, ListView):
    """ View to list all articles."""

    model = Article
    template_name = 'home.html'

    def get_queryset(self):
        level = self.request.user.level
        queryset = Article.objects.filter(level=level)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            ArticleListView, self).get_context_data(**kwargs)
        return context


class LevelUpView(LoginRequiredMixin, View):
    """ View to list all articles."""

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(
            ArticleListView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # check if threshold is met
        lvl_name = int(request.user.level.name) + 1
        try:
            next_level = Level.objects.get(name=str(lvl_name))
        except Level.DoesNotExist:
            next_level = None
        if next_level:
            request.user.level = next_level
            request.user.save()
        return HttpResponseRedirect(reverse_lazy('qa:home'))
