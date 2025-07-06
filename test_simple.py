#!/usr/bin/env python3
import os
import sys
import django
from django.http import HttpResponse
from django.conf import settings

# Simple test view
def simple_view(request):
    return HttpResponse("<h1>Django is working!</h1><p>Server is running successfully.</p>")

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    django.setup()
    
    from django.core.management import execute_from_command_line
    from django.urls import path
    from django.conf.urls import include
    
    # Override URL patterns temporarily
    import urls
    test_patterns = [
        path('test/', simple_view, name='test'),
        path('', simple_view, name='home'),  # Override homepage
    ]
    urls.urlpatterns = test_patterns + urls.urlpatterns[1:]  # Keep admin URLs
    
    print("Starting test server...")
    execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8004'])