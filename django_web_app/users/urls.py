# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_user_view, name='create_user'),
]
