from django.shortcuts import render
from django.http import HttpResponse
from django.urls import get_resolver

# Create your views here.
def index(request):
    url_patterns = []
    resolver = get_resolver()
    for url_pattern in resolver.url_patterns:
        url_patterns.append(url_pattern.pattern)
    return render(request, "safglobalapp/index.html", {"url_patterns": url_patterns})