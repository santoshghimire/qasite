#!/usr/bin/python

"""Module for apis."""
from braces.views import LoginRequiredMixin
from django.http import Http404
# import environ
# import os
# from pdf_parser import get_pages
from rest_framework.views import APIView
# from rest_framework.renderers import JSONRenderer

from rest_framework import generics, status
from rest_framework.response import Response

from .models import Article, Quiz, Question
from .serializer import QuestionAttemptSerializer


def serialize_question(question_obj):
    options = []
    for option_obj in question_obj.option_set.all().order_by('name'):
        option = {
            'id': option_obj.id,
            'name': option_obj.name,
            'text': option_obj.text,
        }
        if option_obj.image:
            option['image'] = option_obj.image.url
        options.append(option)
    question = {
        'id': question_obj.id,
        'text': question_obj.text,
        'question_type': question_obj.question_type,
        'correct': question_obj.correct,
        'marks': question_obj.marks,
        'difficulty': question_obj.difficulty,
        'is_verified': question_obj.is_verified,
        'category': str(question_obj.category),
        'article': str(question_obj.article)
    }
    if question_obj.image:
        question['image'] = question_obj.image.url
    if question_obj.audio:
        question['audio'] = question_obj.audio.url
    if question_obj.video:
        question['video'] = question_obj.video.url
    data = {
        'question': question,
        'options': options
    }
    return data


class QuestionApi(APIView):
    """Api to get a question."""

    def get(self, request, id, *args, **kwargs):
        """Return results list."""
        try:
            question_obj = Question.objects.get(id=id)
        except:
            raise Http404
        data = serialize_question(question_obj)
        return Response(data)


class StartQuizApi(APIView):
    """List of questions and fields required for an exam."""

    def get(self, request, slug, *args, **kwargs):
        """Return an exam object."""
        try:
            article = Article.objects.get(
                slug=slug
            )
        except:
            raise Http404
        quiz = Quiz(
            article=article, category=article.category,
            user=self.request.user
        )
        # set questions
        quiz.save()
        for i in article.question_set.all():
            quiz.questions.add(i)

        if not quiz.questions.all():
            quiz.delete()
            raise Http404

        data = {
            'id': quiz.id,
            'questions': [serialize_question(q) for q in quiz.questions.all()],
            'article': str(quiz.article),
            'category': str(quiz.article.category)
        }
        return Response(data)


class QuestionAttemptCreate(LoginRequiredMixin, generics.CreateAPIView):
    """Post a question attempt."""

    serializer_class = QuestionAttemptSerializer

    def post(self, request, format=None, *args, **kwargs):
        """Method to post question attempt data."""
        # TODO: Justify who can post attempts: access mgmt
        # check user who posts this request is the same user
        # who started the exam.
        serializer = QuestionAttemptSerializer(
            data=request.data,
            request=request
        )
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailViewAPI(APIView):
    """List of questions and fields required for an exam."""

    def get(self, request, article_id, *args, **kwargs):
        """Return an exam object."""
        try:
            article = Article.objects.get(
                id=article_id
            )
        except:
            raise Http404
        data = {
            'id': article.id,
            'title': article.title,
            'category': article.category.title
        }
        if article.level:
            data['grade'] = article.level.grade.name,

        if article.audio:
            data['audio'] = article.audio.url
        # if article.content:
        #     content_path = str(article.content.url)
        #     root_dir = str(environ.Path(__file__) - 2)
        #     root_dir = os.path.join(root_dir, 'qasite')
        #     content_full_path = root_dir + content_path
        #     images_folder = root_dir + '/media/article/images/'
        #     pages = get_pages(content_full_path, images_folder=images_folder)
        #     new_pages = []
        #     for page in pages:
        #         page = page.decode('utf8')
        #         # image is present
        #         page = page.replace(
        #             '<img', '<img style="float: right; margin-left: 20px;max-width:400px;"'
        #         )
        #         page = page.replace(images_folder, '/media/article/images/')
        #         new_pages.append(page)
        #     data['pages'] = new_pages
        if article.content_formatted:
            split = article.content_formatted.split('<hr />')
            # data['pages'] = [article.content_formatted]
            data['pages'] = split
        return Response(data)
