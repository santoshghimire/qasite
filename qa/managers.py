# -*- coding: utf-8 -*-
from django.db import models


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super(CategoryManager, self).get_queryset()


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super(ArticleManager, self).get_queryset()

    def active(self):
        return self.filter(active=True)


class QuestionManager(models.Manager):
    def get_queryset(self):
        return super(QuestionManager, self).get_queryset()


class QuizManager(models.Manager):
    def get_queryset(self):
        return super(QuizManager, self).get_queryset()


class QuestionAttemptManager(models.Manager):
    def get_queryset(self):
        return super(QuestionAttemptManager, self).get_queryset()
