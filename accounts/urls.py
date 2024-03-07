"""URL patterns for accounts."""

from django.urls import path, include


app_name = 'accounts'
urlpatterns = [
    # Default auth urls.
    path('', include('django.contrib.auth.urls')),
]