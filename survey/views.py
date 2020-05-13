# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Sum, Count
from django.shortcuts import render, redirect
from rest_framework.views import APIView, Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.template import RequestContext
from django.shortcuts import render_to_response
from survey.forms import SurveyForm   
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .serializers import *
from django.db import connection, transaction
import json
from django.db.models.expressions import RawSQL
from itertools import izip
from .models import *



def index(request):
    return render_to_response('index.html')

# Create your views here.



# Create your views here. 

@csrf_exempt 
def emp(request):  
    if request.method == "POST":  
        form = SurveyForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/show')  
            except:  
                pass  
    else:  
        form = SurveyForm()  
    return render(request,'index.html',{'form':form})  
def show(request):  
    surveys = Survey.objects.all()  
    return render(request,"show.html",{'surveys':surveys})  
def edit(request, id):  
    survey = Survey.objects.get(id=id)  
    return render(request,'edit.html', {'survey':survey})  
def update(request, id):  
    survey = Survey.objects.get(id=id)  
    form = SurveyForm(request.POST, instance = survey)  
    if form.is_valid():  
        form.save()  
        return redirect("/show")  
    return render(request, 'edit.html', {'survey': survey})  
def destroy(request, id):  
    survey = Survey.objects.get(id=id)  
    survey.delete()  
    return redirect("/show") 

# class SurveyViewSet(generics.ListCreateAPIView):
#     queryset = Survey.objects.all()
#     serializer_class = SurveySerializer

class SurveyViewSet(generics.ListCreateAPIView):
    queryset = Survey.objects.select_related('surveyCoordinator')
    #queryset = Survey.objects.all()
    serializer_class = SurveywithoutAnsSerializer
    
class SurveyRespondantViewSet(generics.ListCreateAPIView):
    #queryset = SurveyCoordinator.objects.all()
    queryset = SurveyRespondant.objects.all()
    serializer_class = SurveyRespondantSerializer
    

class SurveyCoordinatorViewSet(generics.ListCreateAPIView):
    #queryset = SurveyCoordinator.objects.all()
    queryset = SurveyCoordinator.objects.all()
    serializer_class = SurveyCoordinatorWithoutSurveySerializer

class QuestionViewSet(generics.ListCreateAPIView):
    queryset = Question.objects.select_related('survey')
    serializer_class = QuestionSerializer

class AnswerViewSet(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
 
class ResponseViewSet(generics.ListCreateAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer 


    
def getcoordinator(self, id):  
    coord = SurveyCoordinator.objects.get(id=id)
    response = SurveyCoordinatorWithoutSurveySerializer(coord) 
    return JsonResponse(response.data)

def getsurveybyid(self, id):  
    survey = Survey.objects.get(id=id)
    response = SurveySerializer(survey) 
    return JsonResponse(response.data)

def getRespondantbyid(self, id):  
    respondant = SurveyRespondant.objects.get(id=id)
    response = SurveyRespondantSerializer(respondant) 
    return JsonResponse(response.data)


def getCloseSurveybyid(self, id):  
    survey = Survey.objects.get(id=id)
    #obj = Product.objects.get(pk=pk)
    survey.status = "close"
    survey.save()
    response = SurveySerializer(survey) 
    return JsonResponse(response.data)
    
def getCloseSurveybyid(self, id):  
    survey = Survey.objects.get(id=id)
    #obj = Product.objects.get(pk=pk)
    survey.status = "close"
    survey.save()
    response = SurveySerializer(survey) 
    return JsonResponse(response.data)

def getOpenSurveybyid(self, id):  
    survey = Survey.objects.get(id=id)
    survey.status = "open"
    survey.save()
    response = SurveySerializer(survey) 
    return JsonResponse(response.data)

@api_view(["PUT"])
@csrf_exempt
def updateSurveybyid( request, id):
    payload = json.loads(request.body)
    # survey = Survey.objects.get(id=id)
    survey = Survey.objects.filter(id=id)
    survey.update(**payload)
    # response = SurveySerializer(survey) 
    response = SurveywithoutAnsSerializer(survey, many=True) 
    return JsonResponse({'book': response.data}, safe=False, status=status.HTTP_200_OK)
    # return JsonResponse(response.data)

  
def getSurveyResultbyid(request, id):
    survey = Survey.objects.filter(id=id)
    response = SurveySerializer(survey, many=True)
    return JsonResponse(response.data, safe=False)

def getSurveyResultCountbyid(request,id):
    survey = Survey.objects.filter(id=id)
    response = SurveySerializer(survey, many=True)
    return JsonResponse(response.data, safe=False)

def getSurveyCount(request,id):
    cursor = connection.cursor()
    cursor.execute("SELECT \
                    question,type, choice, COUNT(*) AS choicecount \
                    FROM survey INNER JOIN  response ON survey.id=response.survey_id \
                    INNER JOIN question ON response.id=question.response_id \
                    INNER JOIN answer ON question.id=answer.question_id WHERE survey.Id=1 GROUP BY answer.choice ORDER BY question")

    columns = [col[0] for col in cursor.description]
    print(columns)
    return JsonResponse( [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ],safe=False)

@csrf_exempt
def login(request):
        if request.POST:
            email = request.POST['email']
            print(email)
            password = request.POST['password']

            real_passwd = get_RespondantPassword(email)
            if real_passwd == "ERROR":
                return JsonResponse({"ERROR":"Wrong email please check"}) 

            if password ==  real_passwd:
                respondant = SurveyRespondant.objects.get(email=email)
                response = SurveyRespondantSerializer(respondant) 
                return JsonResponse(response.data) 
            else:
                return JsonResponse({"ERROR":"wrong password"}) 
        else:
            return JsonResponse({"ERROR":"Please check email and password"})

def get_RespondantPassword(email):
        cursor = connection.cursor()
        sql = 'select password from surveyrespondant where email = "{}"'.format(email)
        sql_return = cursor.execute(sql)

        if sql_return == 0:
            return "ERROR"
        elif sql_return==1:
            passwd = cursor.fetchone() 
            return passwd[0]  
@csrf_exempt
def loginCoordinator(request):
        if request.POST:
            email = request.POST['email']
            print(email)
            password = request.POST['password']

            # 验证用户名
            real_passwd = get_CoordinatorPassword(email)
            if real_passwd == "ERROR":
                return JsonResponse({"ERROR":"Wrong email please check"}, safe=False) 

            if password ==  real_passwd:
                coordinator = SurveyCoordinator.objects.get(email=email)
                response = SurveyCoordinatorWithoutSurveySerializer(coordinator) 
                return JsonResponse(response.data, safe=False) 
            else:
                return JsonResponse({"ERROR":"wrong password"}, safe=False) 
        else:
            return JsonResponse({"ERROR":"Please check email and password"})


def get_CoordinatorPassword(email):
        cursor = connection.cursor()
        sql = 'select password from SurveyCoordinator where email = "{}"'.format(email)
        sql_return = cursor.execute(sql)

        if sql_return == 0:
            return "ERROR"
        elif sql_return==1:
            passwd = cursor.fetchone() 
            return passwd[0]  