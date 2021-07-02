from django.urls import path, include
from . import views

app_name = 'account'
urlpatterns = [
    path('<slug:username>/edit', views.EditProfile.as_view(), name='edit-profile'),
]