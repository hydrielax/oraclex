from django.urls import path
from . import views

# app_name = 'app'
urlpatterns = [
    path('', views.recherche),
    path('recherche/', views.recherche, name='recherche'),
    path('resultat/', views.resultat, name='resultat'),
    path('ajouts/', views.ajouts, name='ajouts'),
    path('infos/', views.infos, name='infos'),
    path('infos/responsable/', views.responsable, name='respo'),
]
