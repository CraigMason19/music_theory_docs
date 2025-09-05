# docs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.bake_view, name='bake_view'),
]