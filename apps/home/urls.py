from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('responsable/', views.responsable, name='respo'),
    path('legal_mentions/', views.legal_mentions, name='legal_mentions'),
    path('politics/', views.politics, name='politics'),
    path('', views.home, name="home"),
]
