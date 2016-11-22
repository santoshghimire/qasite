# -*- coding: utf-8 -*-
"""Urls for entrance."""
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from .question_entry import (
    QuestionCreateView, QuestionUpdateView,
    QuestionDeleteView, QuestionListView,
    QuestionFormatExport
)
from .views import ArticleListView, LevelUpView
from .quiz import QuizView
from .api import (
    StartQuizApi, QuestionApi,
    QuestionAttemptCreate, ArticleDetailViewAPI,
    ArticleHistoryCreate
)

urlpatterns = [
    url(
        regex=r'^$',
        view=ArticleListView.as_view(),
        name='home'
    ),
    url(
        regex=r'^api/article/(?P<article_id>[-\d]+)/$',
        view=ArticleDetailViewAPI.as_view(),
        name='article-detail'
    ),
    url(
        regex=r'^question/create/$',
        view=QuestionCreateView.as_view(),
        name='question-create'
    ),
    url(
        regex=r'^question/update/(?P<id>[-\d]+)/$',
        view=QuestionUpdateView.as_view(),
        name='question-update'
    ),
    url(
        regex=r'^question/delete/(?P<id>[-\w]+)/$',
        view=QuestionDeleteView.as_view(),
        name='question-delete'
    ),
    url(
        regex=r'^question/list/$',
        view=QuestionListView.as_view(),
        name='qlist'
    ),
    url(
        regex=r'^question/format/export/$',
        view=QuestionFormatExport.as_view(),
        name='question-format-export'
    ),
    url(
        regex=r'^quiz/(?P<article_id>[-\w]+)/$',
        view=QuizView.as_view(),
        name='start-quiz'
    ),
    url(
        regex=r'^level/up/$',
        view=LevelUpView.as_view(),
        name='level-up'
    ),
    url(
        regex=r'^api/quiz/start/(?P<slug>[-\w]+)/$',
        view=StartQuizApi.as_view(),
        name='start_quiz_api'
    ),
    url(
        regex=r'^api/question/(?P<id>[-\d]+)/$',
        view=QuestionApi.as_view(),
        name='question_api'
    ),
    url(
        regex=r'^api/question/attempt/$',
        view=QuestionAttemptCreate.as_view(),
        name='question_attempt_create'
    ),
    url(
        regex=r'^api/article-history/(?P<article_id>[-\d]+)/$',
        view=ArticleHistoryCreate.as_view(),
        name='article_history'
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
