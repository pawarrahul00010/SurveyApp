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
from django.contrib import admin
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from survey import views as myapp_views  
#from django.urls import path  
from survey import views 
from rest_framework import routers
from survey.views import SurveyViewSet
from survey import views 

#router = routers.DefaultRouter()

#router.register('get', SurveyViewSet, name='survey-list')
#urlpatterns = router.urls

urlpatterns = [
    #url(r'^$', myapp_views.index, name='index'),
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', 'myapp.views.index'),
    url(r'^admin/', admin.site.urls),
    url('admin/', admin.site.urls),  
    url('emp', views.emp),  
    url('show',views.show),  
    url('edit/([0-9]+)$', views.edit),  
    url('update/([0-9]+)$', views.update),  
    url('delete/([0-9]+)$', views.destroy), 
    url('getcoordinator/([0-9]+)$', views.getcoordinator),
    url('getsurvbyid/([0-9]+)$', views.getsurveybyid), 
    #url('get', views.SurveyViewSet.as_view(), name='survey-list'), 
]

