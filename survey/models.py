# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.db import models

# Create your models here.
 
class SurveyCoordinator(models.Model): 
    firstname = models.CharField(max_length=100) 
    lastname =  models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100) 
    created_at = models.DateTimeField(auto_now_add=True, null=True) 
     
    class Meta:  
        db_table = "surveycoordinator" 

    def __str__(self):
        return self.firstname

class SurveyRespondant(models.Model):  
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email =  models.CharField(max_length=100)
    password =  models.CharField(max_length=100) 
    created_at = models.DateTimeField(auto_now_add=True, null=True) 
    
    def __str__(self):
        return self.firstname
    class Meta:  
        db_table = "surveyrespondant" 
    

class Survey(models.Model):   
    status = models.CharField(max_length=100, default='open',)  
    surveyCoordinator = models.ForeignKey(SurveyCoordinator, related_name='surveys', db_column='coordinator_id', on_delete=models.CASCADE, default=5,)
    surveyjson = models.CharField(max_length=9000)  
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:  
        db_table = "survey" 
   

class Question(models.Model):    
    Question = models.CharField(max_length=100)
    type = models.CharField(max_length=100, default=1,) 
    response = models.ForeignKey('Response', on_delete=models.CASCADE, related_name='questions', default=1,)  
    created_at = models.DateTimeField(auto_now_add=True, null=True) 

    class Meta:  
        db_table = "question"

class Response(models.Model):    
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE, related_name='responses', default=1,) 
    respondant = models.ForeignKey('SurveyRespondant', on_delete=models.CASCADE, default=1) 
    created_at = models.DateTimeField(auto_now_add=True, null=True) 
    


    class Meta:  
        db_table = "response"
  
class Answer(models.Model):  
    choice = models.CharField(max_length=100)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers', default=1,)    
    class Meta:  
        db_table = "answer"   

class Result(models.Model):  
    choice = models.CharField(max_length=100) 
    question = models.CharField(max_length=100)
    totalchoice = models.CharField(max_length=100)     
    
