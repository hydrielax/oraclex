from django.urls import path
from . import views
from django.conf.urls import url
from .views import ChartData
app_name = 'predict'
urlpatterns = [
    path('', views.prediction, name='index'),
    url('', ChartData.as_view()),
    #url(r'^api/data/',views.get_data, name='api-data') #api endpoint 
] #api/data/
