# docs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.docs_view, name='docs_home'),
]