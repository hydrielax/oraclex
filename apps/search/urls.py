from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('', views.searchview, name='index'),
    #path('#resultats', views.searchview, name='results'),
    path('fichiers_illisibles', views.unreadables, name='unreadables'),
]
