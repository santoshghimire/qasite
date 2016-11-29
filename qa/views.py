from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from .models import Article, Level, QuizResult


def get_level_percent(user):
    level_obtained_score = 0
    level_total_score = 0
    articles = Article.objects.filter(level=user.level)
    for article in articles:
        quiz_results = QuizResult.objects.filter(quiz__article=article)
        obs = [i.obtained_score for i in quiz_results]
        obtained_score = max(obs) if obs else 0
        ts = [i.total_score for i in quiz_results]
        total_score = max(ts) if ts else 0
        level_obtained_score += obtained_score
        level_total_score += total_score
    try:
        level_percent = int(level_obtained_score / float(level_total_score) * 100.0)
    except:
        level_percent = 0
    passes_threshold = level_percent >= user.level.threshold
    return passes_threshold


class ArticleListView(LoginRequiredMixin, ListView):
    """ View to list all articles."""

    model = Article
    template_name = 'home.html'

    def get_queryset(self):
        if not self.request.user.level:
            level = Level.objects.get(name='1')
            self.request.user.level = level
        user_level = self.request.user.level.name
        level = self.request.GET.get('level', user_level)
        # set level to user's current level if it is higher
        level = user_level if int(level) > user_level else int(level)
        queryset = Article.objects.active().filter(level=level)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            ArticleListView, self).get_context_data(**kwargs)
        passes_threshold = get_level_percent(self.request.user)
        if passes_threshold:
            context['passes_threshold'] = True
        total_data = []
        for article in self.object_list:
            try:
                history = article.history.get(user=self.request.user)
                reading = history.reading
                listening = history.listening
                quiz = history.quiz
            except:
                reading, listening, quiz = False, False, False
            data = {
                'obj': article,
                'reading': reading,
                'listening': listening,
                'quiz': quiz
            }
            total_data.append(data)
        context['articles'] = total_data
        levels = list(Level.objects.all().order_by('name'))

        user_level = self.request.user.level.level
        level = self.request.GET.get('level', user_level)
        # set level to user's current level if it is higher
        level = user_level if int(level) > user_level else int(level)

        total_levels = []
        for lvl in levels:
            lvl_item = {'level': lvl}
            if (
                lvl.name == self.request.user.level.name + 1 and
                passes_threshold
            ):
                lvl_item['up'] = True
            else:
                lvl_item['up'] = False
            if lvl.name <= user_level.name:
                lvl_item['link'] = True
            else:
                lvl_item['link'] = False
            total_levels.append(lvl_item)
        context['selected_level'] = int(level)
        context['levels'] = total_levels
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
        passes_threshold = get_level_percent(request.user)
        if passes_threshold:
            lvl_name = int(request.user.level.name) + 1
            try:
                next_level = Level.objects.get(name=str(lvl_name))
            except Level.DoesNotExist:
                next_level = None
            if next_level:
                request.user.level = next_level
                request.user.save()
        return HttpResponseRedirect(reverse_lazy('qa:home'))
