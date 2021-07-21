from django.urls import path
from . import views

app_name = 'predict'

urlpatterns = [
    path('', views.prediction, name='index'),
]
