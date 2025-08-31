# docs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.documentation_view, name='documentation'),
    path("examples/", views.examples_view, name="examples"),
    path("tools/", views.tools_view, name="tools"),
    path("<str:module_name>/", views.module_view, name="module_docs"),
]