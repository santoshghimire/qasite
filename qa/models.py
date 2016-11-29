from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField
from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel
from ckeditor_uploader.fields import RichTextUploadingField

import os

from .managers import (
    CategoryManager, ArticleManager, QuestionManager,
    QuizManager, QuestionAttemptManager
)
from .validators import (
    validate_image, validate_audio, validate_video
)
from .tts import convert_tts


class Grade(models.Model):
    """
    The grade of the students.
    """

    # Attributes
    name = models.CharField(
        max_length=10,
        verbose_name=_("name"),
        help_text=_("Enter the grade name")
    )

    def __str__(self):
        """Method to return object name in string."""
        return self.name


class Level(models.Model):
    """
    The level of the students. There can be multiple levels
    in one grade.
    """

    # Attributes
    name = models.IntegerField(
        verbose_name=_("name"),
        help_text=_("Enter the level name")
    )
    grade = models.ForeignKey(
        Grade, blank=True, null=True,
        related_name='level'
    )
    threshold = models.IntegerField(
        verbose_name=_("threshold"),
        help_text=_("Enter the threshold in percentage (max 100)")
    )

    class Meta:
        """Class Meta."""
        unique_together = ('name', 'grade')

    def __str__(self):
        """Method to return object name in string."""
        return str(self.name)


class Category(models.Model):
    """
    The category of the articles.
    """

    # Attributes
    title = models.CharField(
        max_length=100,
        verbose_name=_("title"),
        help_text=_("Enter the article category")
    )
    slug = AutoSlugField(populate_from='title', unique=True)
    # Object Manager
    objects = CategoryManager()

    # Meta and String
    class Meta:
        """Meta class."""
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("title",)

    def __str__(self):
        """Method to return object name in string."""
        return self.title


class Article(TimeStampedModel):
    """
    This module contains the information about the Article in a subject.

    """
    title = models.CharField(
        max_length=200,
        verbose_name=_("title"),
        help_text=_("Enter the article title.")
    )
    image = models.ImageField(
        upload_to='article',
        null=True,
        blank=True,
        validators=[validate_image],
        help_text='Maximum file size allowed is 2Mb'
    )
    category = models.ForeignKey(
        Category, blank=True, null=True,
        related_name='topic'
    )
    audio = models.FileField(
        upload_to='article',
        null=True,
        blank=True,
        validators=[validate_audio],
        help_text='Maximum file size allowed is 5Mb'
    )
    level = models.ForeignKey(
        Level,
        null=True, blank=True,
        related_name='topic'
    )
    content_formatted = RichTextUploadingField(null=True, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    active = models.BooleanField(default=False)

    # Object Managers
    objects = ArticleManager()

    # Meta and String
    class Meta:
        """Class Meta."""

        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ("title",)
        unique_together = ('title', 'level', 'category')

    def __str__(self):
        """Str function."""
        return self.title

    def save(self, *args, **kwargs):
        # create directory
        super(Article, self).save(*args, **kwargs)
        try:
            interview_dir_path = '/media/article/'
            full_path = settings.MEDIA_FULL_ROOT + interview_dir_path
            if not os.path.exists(full_path):
                os.makedirs(full_path)
            content_audio_file_path = full_path + '/' + str(self.id) + '.wav'
            content_audio_mp3_file_path = full_path + '/' + str(self.id) + '.mp3'
            convert_tts(
                text='content_audio_text',
                file_path=content_audio_file_path,
                mp3_file_path=content_audio_mp3_file_path
            )
        except:
            pass


class Question(TimeStampedModel):
    """
    Stores a single Question entry along with its answers and other details.

    """

    # question fields
    text = models.TextField()
    image = models.ImageField(
        upload_to='questionImages',
        null=True,
        blank=True,
        validators=[validate_image],
        help_text='Maximum file size allowed is 2Mb'
    )
    audio = models.FileField(
        upload_to='questionAudio',
        null=True,
        blank=True,
        validators=[validate_audio],
        help_text='Maximum file size allowed is 5Mb'
    )
    video = models.FileField(
        upload_to='questionVideo',
        null=True,
        blank=True,
        validators=[validate_video],
        help_text='Maximum file size allowed is 10Mb'
    )

    question_type_choices = (
        ('objective', 'Objective'),
        ('subjective', 'Categoryive'),
    )
    question_type = models.CharField(
        max_length=20,
        choices=question_type_choices,
        default='objective'
    )

    correct = models.CharField(
        max_length=1,
        null=True
    )
    marks = models.FloatField(null=True, blank=True)
    difficulty = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    is_verified = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name="createdby"
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="updatedby"
    )

    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="verifiedby"
    )

    # Object Manager
    objects = QuestionManager()

    # Meta and String
    class Meta:
        """Class Meta."""

        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ("article",)

    def __str__(self):
        """Str function."""
        return self.text

    def delete(self):
        for opt in self.option_set.all():
            opt.delete()
        super(Question, self).delete()


class Option(models.Model):
    """Option for a question"""
    name = models.CharField(
        max_length=1,
        help_text=_("Enter option name e.g. a")
    )
    text = models.TextField(null=True)
    image = models.ImageField(
        upload_to='answerImages',
        null=True,
        blank=True,
        validators=[validate_image],
        help_text='Maximum file size allowed is 2Mb'
    )
    question = models.ForeignKey(Question)

    def __str__(self):
        """Str magic function."""
        return "Q{0} - Option {1}: {2}".format(
            self.question.id, self.name, self.text)


class Quiz(TimeStampedModel):
    """
    Stores a exam given by a User. Quizs are unique to each of the Users.
    """

    questions = models.ManyToManyField(Question)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name="user"
    )

    category = models.ForeignKey(Category, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    # Object Manager
    objects = QuizManager()

    # Meta and String
    class Meta:
        """Class Meta."""

        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizs")

    def __str__(self):
        """Str magic function."""
        return "%s Quiz - %s - %s" % (
            self.category.title, self.user.username, self.id)


class QuizResult(TimeStampedModel):
    """
    Stores a exam given by a User. Quizs are unique to each of the Users.
    """

    quiz = models.OneToOneField(Quiz)
    obtained_score = models.IntegerField(null=True, blank=True)
    total_score = models.IntegerField(null=True, blank=True)

    # Meta and String
    class Meta:
        """Class Meta."""
        verbose_name = _("Quiz Result")
        verbose_name_plural = _("Quiz Results")

    def __str__(self):
        """Str magic function."""
        return "{0} Quiz Result - {1} - {2} of {3}".format(
            self.quiz.article.title, str(self.quiz.user),
            self.obtained_score, self.total_score)


class QuestionAttempt(TimeStampedModel):
    """Stores the question, attempt_time and given_answer by user."""

    question = models.ForeignKey(Question)
    given_answer = models.CharField(max_length=8000)
    is_correct = models.BooleanField()
    attempted = models.BooleanField(default=False)
    point = models.IntegerField(null=True, blank=True)
    quiz = models.ForeignKey(Quiz)

    # Object Manager
    objects = QuestionAttemptManager()

    # Meta and String
    class Meta:
        """Class meta."""

        verbose_name = _("QuestionAttempt")
        verbose_name_plural = _("QuestionAttempts")

    def __str__(self):
        """Magic function for string."""
        return self.given_answer + ': ' + self.question.text[:20]


class QuestionAttemptPoint(models.Model):
    """
    The point for multiple question attempts.
    """

    # Attributes
    first = models.IntegerField(blank=True, null=True)
    second = models.IntegerField(blank=True, null=True)
    third = models.IntegerField(blank=True, null=True)
    fourth = models.IntegerField(blank=True, null=True)


class ArticleHistory(models.Model):
    """
    The history of article for each user.
    """

    # Attributes
    reading = models.BooleanField(default=False)
    listening = models.BooleanField(default=False)
    quiz = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    article = models.ForeignKey(Article, related_name='history')

    def __str__(self):
        """Magic function for string."""
        return "{0} - {1}".format(
            self.user.username, self.article.title
        )
