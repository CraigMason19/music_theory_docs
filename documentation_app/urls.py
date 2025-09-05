# docs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.documentation_view, name='documentation_view'),
    path("examples/", views.examples_view, name="examples_view"),
    path("tools/", views.tools_view, name="tools_view"),
    path("<str:module_name>/", views.module_view, name="module_view"),
]