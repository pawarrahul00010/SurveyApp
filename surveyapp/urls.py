"""surveyapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from rest_framework import routers
from django.contrib import admin
from django.conf.urls import include
from django.contrib.auth import views as auth_views
#from survey import views as survey_views  
#from django.urls import path  
from survey import views 
from survey.views import SurveyViewSet
 

# router = routers.DefaultRouter()
# router.register(r'get', views.SurveyViewSet.as_view(), basename='Survey')

urlpatterns = [
    url(r'/', include('survey.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', 'myapp.views.index'),
    url(r'^admin/', admin.site.urls),
    url('admin/', admin.site.urls),  
    url('emp', views.emp),  
    url('show',views.show),  
    url('edit/([0-9]+)$', views.edit),  
    url('update/([0-9]+)$', views.update),  
    url('delete/([0-9]+)$', views.destroy),
    
    url('getsurvey', views.SurveyViewSet.as_view(), name='survey-list'),
    url('getcoordinators', views.SurveyCoordinatorViewSet.as_view(), name='surveyCoordinator-list'),  
    url('getquestion', views.QuestionViewSet.as_view(), name='question-list'),
    url('getanswer', views.AnswerViewSet.as_view(), name='answer-list'), 
    url('getrespondants', views.SurveyRespondantViewSet.as_view(), name='surveyRespondant-list'),  
    url('getcoordbyid/([0-9]+)$', views.getcoordinator),  
    url('getsurvbyid/([0-9]+)$', views.getsurveybyid),
    url('getrespbyid/([0-9]+)$', views.getRespondantbyid),
    url('closeSurveybyid/([0-9]+)$', views.getCloseSurveybyid),
    url('openSurveybyid/([0-9]+)$', views.getOpenSurveybyid), 
    url('updateSurveybyid/([0-9]+)$', views.updateSurveybyid), 
    url('getSurveyResultbyid/([0-9]+)$', views.getSurveyResultbyid),
    url('getSurveyChoicecount/([0-9]+)$', views.getSurveyCount),
    url('getResponses', views.ResponseViewSet.as_view(), name='response-list'),
    url('login', views.login),
    url('loginCoordinator', views.loginCoordinator),
   
#    url('get', views.get), 
]

