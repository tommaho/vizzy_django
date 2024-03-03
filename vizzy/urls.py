"""Vizzy app routes."""

from django.urls import path

from . import views

app_name = "vizzy"

urlpatterns = [
    # Home
    path('', views.index, name='index'),
    # Create Dataset
    path('create/', views.create, name='create'),
    # Datasets
    path('datasets/', views.datasets, name='datasets'),
    # Visualize
     path('visualize/<int:dataset_id>/', views.visualize, name='visualize'),

]


