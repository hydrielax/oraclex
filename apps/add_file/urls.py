from django.urls import path
from . import views

app_name = 'add_file'
urlpatterns = [
    path('', views.ajout, name='index'),
    path('history', views.send_history, name='table'),
    path('doublons', views.gestion_doublons, name='doublons'),
    path('doublons/<int:id>/conserve_ancien', views.keep_old, name='keep_old'),
    path('doublons/<int:id>/conserve_nouveau', views.keep_new, name='keep_new'),
    path('doublons/<int:id>/conserve_deux', views.keep_both, name='keep_both'),
]
