from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('', views.recherche, name='index'),
    path('resultats/', views.resultat, name='results'),
]
