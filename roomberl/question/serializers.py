from question.models import Category
from question.models import Option
from question.models import Question
from rest_framework import serializers


exclude = ["is_deleted", "created_at", "updated_at"]


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        exclude = exclude


class QuestionSerializer(serializers.ModelSerializer):
    option = OptionSerializer(many=True, read_only=True, source="option_set")

    class Meta:
        model = Question
        exclude = exclude


class CategorySerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True, read_only=True, source="question_set")

    class Meta:
        model = Category
        exclude = exclude
