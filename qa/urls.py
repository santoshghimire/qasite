# -*- coding: utf-8 -*-
"""Urls for entrance."""
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from .question_entry import (
    QuestionCreateView, QuestionUpdateView,
    QuestionDeleteView, QuestionListView
)
from .views import ArticleListView
from .quiz import QuizView
from .api import (
    StartQuizApi, QuestionApi,
    QuestionAttemptCreate
)

urlpatterns = [
    url(
        regex=r'^$',
        view=ArticleListView.as_view(),
        name='home'
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
        regex=r'^quiz/(?P<article_id>[-\w]+)/$',
        view=QuizView.as_view(),
        name='start-quiz'
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
