from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('', views.searchview, name='index'),
    path('fichiers_illisibles', views.unreadables, name='unreadables'),
    path('file/<int:id>', views.detailsview, name='details'),
    path('file/temp/<int:id>', views.detailstempview, name='details_temp'),
]
