"""Vizzy app routes."""

from django.urls import path

from . import views

app_name = "vizzy"

urlpatterns = [
    # Home
    path('', views.index, name='index'),
    # Datasets
    path('datasets/', views.datasets, name='datasets'),
    # Visualize
     path('visualize/', views.visualize, name='visualize'),

]


