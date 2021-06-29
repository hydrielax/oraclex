from django.urls import path, include
from . import views

app_name = 'account'
urlpatterns = [
    path('registration/', include('django.contrib.auth.urls')),
]
