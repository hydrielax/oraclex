from django.urls import path, include
from . import views

app_name = 'account'
urlpatterns = [
    path('registration/', include('django.contrib.auth.urls')),
    path('<slug:username>/edit', views.EditProfile.as_view(), name='edit-profile'),
]