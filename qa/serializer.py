"""Serializers for viewsets... part of api."""
from django.http import Http404
from rest_framework import serializers

from .models import (
    QuestionAttempt, Question, Quiz, QuestionAttemptPoint,
    QuizResult
)


class QuestionAttemptSerializer(serializers.Serializer):
    """
    Serializer for saving question attempts.

    Return question attempt information.
    """

    question_id = serializers.IntegerField(required=False)
    quiz_id = serializers.IntegerField(required=False)
    given_answer = serializers.CharField(required=False)
    attempt_count = serializers.CharField(required=False)

    def __init__(self, request=None, *args, **kwargs):
        """Constructor."""
        self.request = request
        return super(QuestionAttemptSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        """Create QuestionAttempt object with the data."""
        # TO DO: Calculate if given answer is correct or not.
        try:
            points = QuestionAttemptPoint.objects.all()[0]
        except:
            points = None
        try:
            question = Question.objects.get(
                id=int(validated_data['question_id'])
            )
        except Question.DoesNotExist:
            raise Http404
        point = 0
        total_points = 0
        if points:
            total_points = points.first
        if question.correct.lower() == validated_data['given_answer'].lower():
            is_correct = True
            if points:
                attempt_count = int(validated_data['attempt_count'])
                if attempt_count == 1:
                    point = points.first
                elif attempt_count == 2:
                    point = points.second
                elif attempt_count == 3:
                    point = points.third
                else:
                    point = points.fourth
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
            question_attempt.point = point
            question_attempt.given_answer = validated_data['given_answer']
            question_attempt.is_correct = is_correct
            question_attempt.save()
        except QuestionAttempt.DoesNotExist:
            question_attempt = QuestionAttempt(
                question=question,
                given_answer=validated_data['given_answer'],
                is_correct=is_correct,
                attempted=True,
                point=point,
                quiz=quiz
            )
            question_attempt.save()

        # save quiz result
        quiz_result, created = QuizResult.objects.get_or_create(
            quiz=quiz
        )
        all_question_attempts = QuestionAttempt.objects.filter(
            quiz=quiz
        )
        full_marks = total_points * len(quiz.questions.all())
        obtained_marks = sum([i.point for i in all_question_attempts])
        quiz_result.total_score = full_marks
        quiz_result.obtained_score = obtained_marks
        quiz_result.save()

        data = {
            'correct': is_correct,
            'correct_option': question.correct,
            'point': point,
            'total_points': total_points
        }
        data.update(validated_data)
        return data
