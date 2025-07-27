# docs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.docs_view, name='documentation_home'),
    path("notes/", views.notes_view, name="notes"),
]