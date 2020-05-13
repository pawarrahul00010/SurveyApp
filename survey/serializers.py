from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator




class SurveyRespondantSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=SurveyRespondant.objects.all())]
            )
    password = serializers.CharField(min_length=6)
    class Meta:
        model=SurveyRespondant
        fields = "__all__"

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Answer
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True,)
    class Meta:
        model=Question
        fields = "__all__"
        extra_kwargs = {
            'id': {
                'read_only': False, 
                'required': False
             }
        } #very important
    def create(self, validated_data):
        answers = validated_data.pop('answers', [])
        instance = Question.objects.create(**validated_data)
        for answer_data in answers:
            answer = Answer.objects.get(pk=answer_data.get('id'))
            instance.answers.add(answer)
        return instance 

    def update(self, instance, validated_data):
        answers = validated_data.pop('answers', [])
        instance = super().update(instance, validated_data)
        for answer_data in answers:
            answer = Question.objects.get(pk=answer_data.get('id'))
            instance.answers.add(answer)
        return instance 

class ResponseSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True,)
    class Meta:
        model=Response
        fields = "__all__"
        extra_kwargs = {
            'id': {
                'read_only': False, 
                'required': False
             }
        } #very important
    def create(self, validated_data):
        questions = validated_data.pop('questions', [])
        response = Response.objects.create(**validated_data)
        for question_data in questions:
            answers = question_data.pop('answers', [])
            question = Question.objects.create(response = response, **question_data)
            for answer_data in answers:
                answer = Answer.objects.create(question=question, **answer_data)
                question.answers.add(answer)
            response.questions.add(question)
        return response 

    def update(self, instance, validated_data):
        questions = validated_data.pop('questions', [])
        instance = super().update(instance, validated_data)
        for question_data in questions:
            question = Question.objects.get(pk=question_data.get('id'))
            instance.questions.add(question)
        return instance 



class SurveySerializer(serializers.ModelSerializer):
    responses = ResponseSerializer(many=True,)
    class Meta:
        model=Survey
        fields = "__all__"

class SurveywithoutAnsSerializer(serializers.ModelSerializer):

    class Meta:
        model=Survey
        fields = "__all__"

class SurveyCoordinatorSerializer(serializers.ModelSerializer):
    surveys = SurveywithoutAnsSerializer(many=True, )
    class Meta:
        model=SurveyCoordinator
        fields = "__all__"

class SurveyCoordinatorWithoutSurveySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=SurveyCoordinator.objects.all())]
            )
    password = serializers.CharField(min_length=6)
    class Meta:
        model=SurveyCoordinator
        fields = "__all__"

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model=Result
        fields = "__all__"


