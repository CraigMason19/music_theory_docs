# docs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.documentation_view, name='documentation'),
    path("notes/", views.notes_view, name="notes"),
    path("scales/", views.scales_view, name="scales"),
    path("examples/", views.examples_view, name="examples"),
    path("tools/", views.tools_view, name="tools"),
]