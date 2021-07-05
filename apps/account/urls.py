from django.urls import path, include
from . import views

app_name = 'account'
urlpatterns = [
    path('<slug:username>/edit', views.EditProfile, name='edit-profile'),
    path('edit-respo/', views.ChangeResponsable, name='edit-respo'),
    path('ajouter-utilisateur', views.AddUser, name='add-user'),
    path('utilisateur-cree/', views.ProfileCreated, name='profile-created')
]