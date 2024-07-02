from django.shortcuts import render
from django.http import HttpResponse
from django.urls import get_resolver, URLResolver, URLPattern

# Create your views here.
def index(request):
    urls = []
    def collect_urls(url_patterns, prefix=''):
        for pattern in url_patterns:
            if isinstance(pattern, URLResolver):
                collect_urls(pattern.url_patterns, prefix + str(pattern.pattern))
            elif isinstance(pattern, URLPattern):
                urls.append(prefix + str(pattern.pattern))

    resolver = get_resolver()
    collect_urls(resolver.url_patterns)
    return render(request, "safglobalapp/index.html", {"url_patterns": urls})