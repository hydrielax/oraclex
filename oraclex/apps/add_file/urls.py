from django.urls import path
from . import views

app_name = 'add_file'
urlpatterns = [
    path('', views.ajouts, name='index'),
]
