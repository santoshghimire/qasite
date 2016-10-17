"""Serializers for viewsets... part of api."""
from django.http import Http404
from rest_framework import serializers

from .models import (
    QuestionAttempt, Question, Quiz
)


class QuestionAttemptSerializer(serializers.Serializer):
    """
    Serializer for saving question attempts.

    Return question attempt information.
    """

    question_id = serializers.IntegerField(required=False)
    quiz_id = serializers.IntegerField(required=False)
    given_answer = serializers.CharField(required=False)

    def __init__(self, request=None, *args, **kwargs):
        """Constructor."""
        self.request = request
        return super(QuestionAttemptSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        """Create QuestionAttempt object with the data."""
        # TO DO: Calculate if given answer is correct or not.
        try:
            question = Question.objects.get(
                id=int(validated_data['question_id'])
            )
        except Question.DoesNotExist:
            raise Http404
        if question.correct.lower() == validated_data['given_answer'].lower():
            is_correct = True
        else:
            is_correct = False
        try:
            quiz = Quiz.objects.get(
                id=int(validated_data['quiz_id'])
            )
        except Quiz.DoesNotExist:
            raise Http404
        try:
            # get attempt if by any chance already exists
            question_attempt = QuestionAttempt.objects.get(
                quiz=quiz, question=question
            )
        except QuestionAttempt.DoesNotExist:
            question_attempt = QuestionAttempt(
                question=question,
                given_answer=validated_data['given_answer'],
                is_correct=is_correct,
                attempted=True,
                quiz=quiz
            )
            question_attempt.save()
        data = {
            'correct': is_correct,
            'correct_option': question.correct
        }
        data.update(validated_data)
        return data
        # return question_attempt
