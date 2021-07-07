from django.urls import path, include
from . import views

app_name = 'account'
urlpatterns = [
    path('edit-profil/', views.EditProfile, name='edit-profile'),
    path('edit-respo/', views.ChangeResponsable, name='edit-respo'),
    path('ajouter-utilisateur/', views.AddUser, name='add-user'),
]